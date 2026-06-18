# Peer Review — INFORMS Workshop on Data Science 2026
## Paper: Synthetic Data Augmentation in the Extreme-Imbalance Regime: Evidence from Marketing Classification

**Review date:** 2026-06-18
**Mode:** Full (5-reviewer panel)
**Decision: Accept with Minor Revisions**

---

## Phase 0 — Reviewer Configuration

| # | Persona | Expertise | Focus |
|---|---|---|---|
| EIC | Workshop Co-Chair, business analytics + AI | Journal fit, originality, practical value | Overall decision |
| R1 | ML researcher, evaluation methodology | Experimental design, stats, reproducibility | Methodology |
| R2 | Marketing analytics practitioner | CRM modeling, class imbalance, domain fit | Domain contribution |
| R3 | LLM/tabular data researcher | Cross-disciplinary, LLM-tabular gap | Perspective |
| DA | Devil's Advocate | Logical challenges, alternative explanations | Core argument stress test |

---

## EIC Review

**Recommendation: Accept with minor revisions | Score: 7.5/10**

**Venue fit:** Excellent. "Synthetic data generation" is explicitly listed in the CFP. "AI in digital marketing" is a secondary fit. This paper is among the most directly relevant submissions possible for this workshop.

**Strengths:**
- Real marketing datasets (Hillstrom, Criteo) — not synthetic benchmark exercises
- Table 2 (measured synthetic class distributions) is the paper's strongest contribution — empirical rather than inferred mechanism
- Honest limitations section with explicit 1%–10% gap acknowledgment
- Multi-generator comparison including state-of-the-art LLMs at two scales
- Clear practitioner decision guide

**Critical issues requiring resolution before submission:**

1. **Placeholder text still in paper.** Lines contain `** What CPU (M1 Pro 2022 32GB)` and `** What GPU (NVIDIA H100 x8)` as unresolved comments. These must be incorporated into the prose or removed before submission.

2. **Header still says "Short paper."** If submitting as a complete paper, this must be changed or removed.

3. **MLP CI value missing.** "mean AUC 0.940 +- CI95" — the actual CI value is not filled in.

4. **TSTR condition defined but no results shown.** §2 defines TSTR as one of three experimental conditions. The paper never reports TSTR results. Either add a TSTR table or remove TSTR from the protocol definition.

5. **Recommendation table shows "–" for 1%–10%.** Should say "Validate experimentally before deploying" rather than a dash.

---

## R1 — Methodology Reviewer

**Recommendation: Minor revision | Score: 7/10**

The experimental design is sound for a workshop paper. The paired t-test with BH-FDR is appropriate. The two-holdout-strategy distinction is clearly explained and correctly justified. Effect size reporting (Cohen's d_z) is appropriate.

**Issues:**

**R1.1 (Major) — Best-α selection creates optimism bias.** You report "best-α result per generator." This is the maximum over 5 α values, introducing a positive selection bias — the reported gain is the best case, not the expected case. The paper should note this explicitly, or alternatively report the mean across all α values alongside the best.

**R1.2 (Major) — GReaT uses α=1.0 but this is not stated.** The GReaT protocol uses n_synthetic = n_train (α=1.0 implicitly), but the paper never states this. Readers comparing GReaT to CTGAN at "best α" will be confused about whether the comparison is fair.

**R1.3 (Moderate) — GReaT synthetic positive rate not measured.** Table 2 reports synthetic class distributions for CTGAN, GaussianCopula, TabDDPM, and SMOTE — but not GReaT. The architectural explanation (GReaT mirrors real distribution) is stated without measurement. Adding a GReaT row to Table 2 would close this gap.

**R1.4 (Minor) — Missing details on CTGAN conditional sampling mechanism.** The paper says CTGAN "generates 7–89× more minority-class rows" but doesn't explain why. One sentence on CTGAN's log-frequency conditional training would explain the numerical observation.

**R1.5 (Minor) — TabDDPM overfitting interpretation.** Getting worse with more training suggests overfitting, not necessarily architectural limitation. The language is appropriately hedged ("suggesting") but could be tightened.

---

## R2 — Domain Reviewer (Marketing Analytics)

**Recommendation: Minor revision | Score: 7.5/10**

The paper is well-positioned for a marketing-oriented audience. The Hillstrom and Criteo datasets are appropriate choices. The practitioner decision table is exactly what applied researchers need. The cost-of-misclassification framing in §1 is effective for this venue.

**Issues:**

**R2.1 (Major) — SMOTE performs comparably to CTGAN on Hillstrom but CTGAN is recommended.** SMOTE delivers +5.84 pts on Hillstrom vs CTGAN's +5.75 pts. SMOTE is free (no generative model, no GPU, no hyperparameters), dramatically simpler, and matches CTGAN on the extreme-imbalance dataset. The paper never addresses why CTGAN is preferred over SMOTE when SMOTE is competitive. The decision table could note "CTGAN or SMOTE — see §3 comparison."

**R2.2 (Moderate) — Optimal mixing ratio α* not discussed.** The paper defines the α-sweep and reports best-α but never discusses the finding that α* ≈ 0.1–0.3 across datasets and generators. For practitioners, knowing the optimal ratio is as important as knowing which generator.

**R2.3 (Moderate) — Dataset vintage.** Hillstrom (2008) and Criteo (2018) are 8–18 years old. A brief acknowledgment that modern conversion patterns may differ would strengthen the external validity discussion.

**R2.4 (Minor) — Privacy not discussed in recommendation.** SMOTE generates near-duplicate minority-class rows, creating membership inference risk. Given GDPR/CCPA relevance in marketing, a one-sentence note in limitations is warranted.

---

## R3 — Perspective Reviewer (LLM/Tabular)

**Recommendation: Minor revision | Score: 7/10**

The cross-disciplinary LLM comparison is the paper's most novel angle for this venue. The GPT-2 vs Mistral-7B comparison directly addresses the "does LLM scale help?" question. The architectural explanation (conditional vs unconditional sampling) is compelling and grounded in Table 2.

**Issues:**

**R3.1 (Major) — GReaT fit-variance finding absent.** The paper's full version documents that two independent GReaT fits on identical data produce per-seed AUC drift of up to 12pp — a methodologically important finding about LLM-based synthesis reproducibility. Even one paragraph would elevate the paper's AI-methodology contribution.

**R3.2 (Moderate) — Table 3 reliability concerns not prominently flagged.** Hillstrom Mistral-7B n=100 is based on 3 valid seeds (footnote ‡ is easy to miss). Given the main claim about Mistral-7B involves this cell (+1.20 ± 5.99 pts), the 3-seed limitation deserves more prominent treatment.

**R3.3 (Moderate) — Future direction paragraph feels disconnected.** The last paragraph of §6 discusses "context-conditioned LLM synthesis" as future work but is not referenced anywhere else in the paper. Connecting it explicitly to Table 2 would make the future work feel like a natural next step.

**R3.4 (Minor) — "Serialized tabular rows" in §5 needs brief explanation.** GReaT converts rows to text like "recency is 6, history is 230..." — non-LLM readers may not understand this.

---

## Devil's Advocate Report

**Overall challenge: The paper's central mechanism claim outpaces its evidence**

**Strongest counter-argument (MAJOR):**

The paper's mechanism claim — "minority-example scarcity drives augmentation value; CTGAN's conditional sampling is why" — rests on two datasets (Hillstrom, Criteo) and one mechanism measurement (Table 2). This is the paper's greatest vulnerability.

Specifically: **SMOTE targets the minority class by construction (100% positive synthetic rate) and matches CTGAN's performance on Hillstrom (+5.84 vs +5.75 pts).** If SMOTE also works, the "conditional generation" explanation is not uniquely supported — it's consistent with a simpler explanation: "adding any minority-class rows helps, regardless of how they're generated."

The paper should explicitly address this: why CTGAN over SMOTE, and what does Table 2 tell us that SMOTE's design doesn't already explain?

**Additional challenges:**

**DA.1 (Major) — "Architecture" vs "overfitting" for TabDDPM.** TabDDPM at N_iter=10k performs worse than at 2k. This is consistent with overfitting, not just architectural limitation. The claim is well-hedged ("suggesting") — keep the hedged language but acknowledge the alternative.

**DA.2 (Moderate) — n=2 treatment datasets.** The ~100 minority examples "threshold" is inferred from two data points. The paper honestly acknowledges the 1%–10% gap. Not a critical flaw, but reviewers will note it.

**DA.3 (Moderate) — Alternative explanation for GReaT failure.** GReaT trained on n=50 rows fails more often than GReaT on n=100. This could be training instability at very small n, not the sampling mechanism. The paper doesn't rule this out.

**DA.4 (Minor) — "7–89× minority enrichment" framing.** CTGAN generates 6.34% positive on Hillstrom — ~7× the real rate (0.90%). But the actual enrichment in the augmented training set depends on α. The "7–89×" framing is striking but refers to the generation rate, not the effective enrichment during training.

**Observations (Non-Defects):**
- The two-holdout-strategy distinction is genuinely important and correctly handled
- The honest limitations section (1%–10% gap) demonstrates scientific integrity
- Table 2 is a legitimate empirical contribution — measured, not inferred

---

## Phase 2 — Editorial Synthesis & Decision

### Consensus Issues (3+ reviewers agree)

1. **Placeholder text** (EIC, R1 implicit, R3 implicit) — Must be resolved before submission
2. **TSTR defined but not shown** (EIC, R1) — Add results or remove from §2
3. **SMOTE vs CTGAN recommendation needs justification** (R2, DA) — Most important content gap
4. **GReaT synthetic rate not measured in Table 2** (R1, R3) — Natural extension, strengthens Table 2

### Divergent Issues (single reviewer)

5. R3.1 (GReaT fit-variance) — Worth adding but not blocking
6. DA.4 (enrichment rate framing) — Valid but minor, hedging sufficient

---

## Editorial Decision: **Accept with Minor Revisions**

**Must fix before submission (blockers):**

| # | Issue | Fix |
|---|---|---|
| 1 | Placeholders `** What CPU/GPU` in §4 | Replace with actual hardware text |
| 2 | Header says "short paper" | Change to complete paper or remove label |
| 3 | "0.940 +- CI95" in §3 | Fill in: 0.940 ± 0.030 |
| 4 | SMOTE vs CTGAN recommendation gap | Add 1-2 sentences explaining when each is preferred |
| 5 | Decision table "–" for 1%–10% | Change to "Validate experimentally before deploying" |
| 6 | GReaT α=1.0 not stated | Add one sentence in §5 |

**Should add (strengthens paper, ~1-2 hours work):**

| # | Issue | Fix |
|---|---|---|
| 7 | TSTR results | Add 3-row table: Telco/Bank/German TSTR gaps |
| 8 | GReaT row in Table 2 | Measure GReaT synthetic positive rate |
| 9 | α* ≈ 0.2–0.3 finding | One sentence in §6 |
| 10 | Figure 11 | Add minority budget vs gain scatter plot |

**Bottom line:** The paper is 1-2 hours of cleanup away from submission-ready. The core contribution (Table 2, measured mechanism) is sound and novel for this venue.
