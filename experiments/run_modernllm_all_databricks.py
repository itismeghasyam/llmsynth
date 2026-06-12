%python
# Modern LLM tabular synthesis — all three GReaT datasets
#
# Identical protocol to the three original GReaT scripts:
#   run_great_databricks.py          → German Credit
#   run_great_hillstrom_databricks.py → Hillstrom
#   run_great_telco_databricks.py    → Telco Churn
#
# Only change: llm="gpt2" (117M, 2019) → LLM_MODEL (7B+, 2024)
#
# Per-dataset config matches original GReaT scripts exactly:
#   German Credit: SMALL_NS=[50,100,200,500],        HOLDOUT_N=200
#   Hillstrom:     SMALL_NS=[50,100,200,500,1000,2000], HOLDOUT_N=10000
#   Telco Churn:   SMALL_NS=[50,100,200,500,1000,2000], HOLDOUT_N=2000
#
# Output files (same naming pattern as original GReaT results):
#   {WORK_DIR}/modernllm_german_results.csv
#   {WORK_DIR}/modernllm_hillstrom_results.csv
#   {WORK_DIR}/modernllm_telco_results.csv
#
# SETUP (run once):
#   %pip install be_great transformers accelerate
#   dbutils.library.restartPython()
#
# GPU requirements (fp16):
#   mistralai/Mistral-7B-v0.1   → A10G (24GB) recommended
#   EleutherAI/gpt-j-6b         → A10G (16GB) or T4 (tight)
#   EleutherAI/gpt-neo-2.7B     → T4 (16GB) safe fallback

import warnings, os, shutil, random
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from scipy import stats
from be_great import GReaT
from transformers import set_seed as _hf_set_seed

# ── Config ────────────────────────────────────────────────────────────────────
LLM_MODEL = os.environ.get("LLMSYNTH_LLM_MODEL", "mistralai/Mistral-7B-v0.1")
WORK_DIR  = os.environ.get("LLMSYNTH_WORK_DIR", "/Workspace/Users/<your-username>/Temp")
SEEDS     = [42, 123, 7, 2024, 999]
BATCH_SIZE = 4   # reduced from 32 (GPT-2) for larger models

print(f"Model : {LLM_MODEL}", flush=True)
print(f"GPU   : {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}", flush=True)

# Per-dataset config — matches original GReaT scripts exactly
DATASETS = [
    {
        "name":       "German Credit",
        "data_path":  f"{WORK_DIR}/credit_default.csv",
        "out_path":   f"{WORK_DIR}/modernllm_german_results.csv",
        "holdout_n":  200,
        "small_ns":   [50, 100, 200, 500],
        "pos_rate_pct": 30.0,
    },
    {
        "name":       "Hillstrom Email",
        "data_path":  f"{WORK_DIR}/hillstrom.csv",
        "out_path":   f"{WORK_DIR}/modernllm_hillstrom_results.csv",
        "holdout_n":  10000,
        "small_ns":   [50, 100, 200, 500, 1000, 2000],
        "pos_rate_pct": 0.9,
    },
    {
        "name":       "Telco Churn",
        "data_path":  f"{WORK_DIR}/telco_churn.csv",
        "out_path":   f"{WORK_DIR}/modernllm_telco_results.csv",
        "holdout_n":  2000,
        "small_ns":   [50, 100, 200, 500, 1000, 2000],
        "pos_rate_pct": 26.6,
    },
]

TARGET = "target"


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    _hf_set_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"


def ci95(values):
    arr = np.array([v for v in values if not np.isnan(v)])
    if len(arr) < 2:
        return float(np.mean(arr)), float("nan")
    se = stats.sem(arr)
    return float(np.mean(arr)), float(se * stats.t.ppf(0.975, df=len(arr)-1))


def run_dataset(cfg):
    name      = cfg["name"]
    data_path = cfg["data_path"]
    out_path  = cfg["out_path"]
    holdout_n = cfg["holdout_n"]
    small_ns  = cfg["small_ns"]

    print(f"\n{'='*64}", flush=True)
    print(f"Dataset: {name}  ({cfg['pos_rate_pct']}% positive rate)", flush=True)
    print(f"{'='*64}", flush=True)

    if not os.path.exists(data_path):
        print(f"  [skip] {data_path} not found — upload to WORK_DIR first.", flush=True)
        return

    df = pd.read_csv(data_path)
    print(f"Loaded: {df.shape}, positive rate: {df[TARGET].mean()*100:.2f}%", flush=True)

    _, df_holdout = train_test_split(df, test_size=holdout_n, random_state=42,
                                      stratify=df[TARGET])
    X_ho = df_holdout.drop(columns=[TARGET]).values.astype(float)
    y_ho = df_holdout[TARGET].values
    df_pool = df.drop(df_holdout.index).reset_index(drop=True)
    pos_pool = df_pool[df_pool[TARGET] == 1]
    neg_pool = df_pool[df_pool[TARGET] == 0]

    # Resume
    if os.path.exists(out_path):
        rows = pd.read_csv(out_path).to_dict("records")
        done = {(r["n"], r["seed"]) for r in rows if r["method"] == "Baseline"}
        print(f"Resuming — {len(done)} (n, seed) pairs done", flush=True)
    else:
        rows, done = [], set()

    for n_train in small_ns:
        print(f"\n  n={n_train}:", flush=True)
        for seed in SEEDS:
            if (n_train, seed) in done:
                print(f"    seed={seed} skip", flush=True)
                continue

            seed_everything(seed)

            # Stratified small-n sample
            n_pos = max(1, int(round(n_train * len(pos_pool) / len(df_pool))))
            n_neg = n_train - n_pos
            df_tr = pd.concat([
                pos_pool.sample(n_pos, random_state=seed),
                neg_pool.sample(n_neg, random_state=seed)
            ]).sample(frac=1, random_state=seed).reset_index(drop=True)
            X_tr = df_tr.drop(columns=[TARGET]).values.astype(float)
            y_tr = df_tr[TARGET].values

            # Baseline
            clf = GradientBoostingClassifier(n_estimators=100, max_depth=4,
                                             random_state=seed)
            clf.fit(X_tr, y_tr)
            base_auc = roc_auc_score(y_ho, clf.predict_proba(X_ho)[:, 1])
            rows.append({"n": n_train, "seed": seed, "method": "Baseline",
                         "auc": base_auc, "error": "", "model": "—"})
            print(f"    seed={seed}  Baseline={base_auc:.4f}", end="", flush=True)

            # Modern LLM via GReaT
            try:
                epochs = 100 if n_train <= 100 else 50
                ckpt_dir = f"/tmp/great_ckpt_{name.split()[0].lower()}"
                if os.path.exists(ckpt_dir):
                    shutil.rmtree(ckpt_dir)

                model = GReaT(
                    llm=LLM_MODEL,
                    batch_size=BATCH_SIZE,
                    epochs=epochs,
                    fp16=True,
                    experiment_dir=ckpt_dir,
                    logging_steps=1,
                    logging_strategy="epoch",
                )
                print(f"  [fit]", end="", flush=True)
                model.fit(df_tr)
                print(f"  [sample]", end="", flush=True)
                df_syn = model.sample(n_train, guided_sampling=True, max_length=2000)

                if len(df_syn) == 0:
                    raise ValueError("Empty sample returned")
                df_syn.columns = df_tr.columns
                df_syn[TARGET] = pd.to_numeric(df_syn[TARGET],
                                               errors="coerce").fillna(0).astype(int)
                X_aug = np.vstack([X_tr,
                                   df_syn.drop(columns=[TARGET]).values.astype(float)])
                y_aug = np.concatenate([y_tr, df_syn[TARGET].values])
                clf2 = GradientBoostingClassifier(n_estimators=100, max_depth=4,
                                                  random_state=seed)
                clf2.fit(X_aug, y_aug)
                auc = roc_auc_score(y_ho, clf2.predict_proba(X_ho)[:, 1])
                rows.append({"n": n_train, "seed": seed, "method": "ModernLLM",
                             "auc": auc, "error": "", "model": LLM_MODEL})
                print(f"  ModernLLM={auc:.4f}", flush=True)

            except Exception as e:
                err = str(e)[:200]
                rows.append({"n": n_train, "seed": seed, "method": "ModernLLM",
                             "auc": float("nan"), "error": err, "model": LLM_MODEL})
                print(f"  ModernLLM=FAIL({err[:60]})", flush=True)

            pd.DataFrame(rows).to_csv(out_path, index=False)

    # Summary
    df_out = pd.DataFrame(rows)
    print(f"\n  {name} — {LLM_MODEL} vs Baseline (mean ± 95% CI):", flush=True)
    print(f"  {'n':>5}  {'Method':<12}  {'AUC':>10}  {'±CI95':>8}  {'vs Baseline':>12}")
    print(f"  {'-'*52}")
    for n in small_ns:
        sub = df_out[df_out["n"] == n]
        if sub.empty: continue
        bm, _ = ci95(sub[sub["method"] == "Baseline"]["auc"].values)
        for meth in ["Baseline", "ModernLLM"]:
            vals = sub[sub["method"] == meth]["auc"].values
            if len(vals) == 0: continue
            m, h = ci95(vals)
            gain = m - bm if meth != "Baseline" else 0.0
            print(f"  {n:>5}  {meth:<12}  {m:>10.4f}  {h:>8.4f}  {gain:>+12.4f}")

    print(f"\n  Saved: {out_path}", flush=True)


# ── Run all datasets ──────────────────────────────────────────────────────────
if __name__ == "__main__" or True:
    for cfg in DATASETS:
        run_dataset(cfg)
    print("\nAll datasets done.", flush=True)
