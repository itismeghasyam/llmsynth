# Peer Review Panel — Fourth Re-Review of `paper2-empirical.md`

**Manuscript:** *When Class Imbalance Dominates: A Controlled Empirical Study of Synthetic Data Augmentation for Marketing Classification*
**Re-review date:** 2026-06-08
**Previous reviews:** v1 (`paper2-empirical.review.md`) · v2 (`paper2-empirical.rereview.md`) · v3 (`paper2-empirical.rereview-v3.md`)
**Mode:** Re-review v4 — final pass after all 9 polish fixes applied

---

## EDITORIAL ASSESSMENT — Editor-in-Chief

**Verdict: Accept after prose rewrite.** All previously-identified critical and minor issues are resolved within the scope of what can be done without new experiments. The paper is now methodologically defensible and reviewer-ready. The single remaining gating item is the prose rewrite, which is the author's responsibility and outside the scope of peer review.

**Score progression across four reviews:**

| Pass | Score | Verdict | Major change |
|---|---|---|---|
| v1 (first draft) | 4/10 | Major revision | Baseline state |
| v2 (after MLP fix + figures) | 5/10 | Major revision | Cosmetic + 1 critical fix |
| v3 (after stats + TabDDPM 10k) | 6.5–7/10 | Conditional accept | Methodological revisions |
| **v4 (after 9 polish fixes)** | **7.5–8/10** | **Accept after prose rewrite** | All review items closed |

**Status of all previously-flagged issues:**

| Issue family | Origin | v3 status | v4 status |
|---|---|---|---|
| Statistical apparatus | R1 v1 | Resolved v3 | ✅ Stable |
| TabDDPM training budget | R2 v1 | Resolved v3 | ✅ Stable |
| §3.3 / §4.2 labeling | R1 v2 | Resolved v3 | ✅ Stable |
| MLP Criteo diagnosis | DA v1, R2 v2 | Resolved v2 | ✅ Stable |
| Tautology framing (DA.1) | DA v1 | Resolved v3 | ✅ Stable |
| Prior-art search (DA.6) | DA v1 | Resolved v3 | ✅ Stable |
| Reference verification | R2 v2 | Resolved v3 | ✅ Stable |
| MLP rescue in abstract (R2.6) | R2 v2 | Partial | ✅ Resolved (finding #4) |
| Cost-sensitive baseline (R3.1) | R3 v1 | Open | ✅ Acknowledged in §5.4 + §6 |
| Overfitting interpretation (R2.7, DA.8) | R2/DA v3 | Open | ✅ Hedged in §4.5 |
| GReaT scope to GPT-2 (DA.3) | DA v1 | Partial | ✅ Scoped in §4.7 and contribution #4 |
| n_real scope to §6 rule (DA.4) | DA v1 | Open | ✅ Scoped in §6 |
| Figure 1 caption with takeaway (R3.6) | R3 v2 | Open | ✅ Rewritten with headline |
| Privacy/operational concerns (R2.5, R3.5) | R2/R3 v1 | Open | ✅ Three new limitation paragraphs in §5.4 |
| n=2 marketing dataset gap (R2.2, R3.2) | R2/R3 v1 | Partial | ✅ Acknowledged in §3.1 + §5.4 |
| Per-seed pairing verification (R1.7) | R1 v3 | Open | ✅ Programmatically verified |

**Sixteen issues raised across three review rounds. Sixteen issues closed.**

The remaining issues from the v3 synthesis (items 16–20: TSTR multi-seed CIs, cost-sensitive empirical comparison, TabSyn, ablation, uplift) are all acknowledged as limitations and natural future work. The author has stated no further experiments will be run; the limitation section honestly carries the resulting scope of claims.

---

## REVIEWER 1 — Statistical Methods (Re-Review v4)

**Summary:** The statistical reporting is now appropriate for the sample sizes available. R1.7 (the only open R1 issue from v3) was verified programmatically: seeds {7, 42, 123, 999, 2024} match exactly across `ci_hillstrom.csv`, `ci_criteo.csv`, `ci_tabddpm_hillstrom_10000.csv`, and `ci_tabddpm_criteo_10000.csv`. Per-seed pairing is correctly preserved.

**Final R1 status:**

- R1.1 (paired tests): ✅ §4.8
- R1.2 (FDR correction): ✅ BH q=0.10 over 12 tests
- R1.3 (formal hypothesis test): ✅ Cross-dataset regression R²=0.92, p=0.0023
- R1.4 (§4.2 labels): ✅ Resolved
- R1.5 (TSTR multi-seed CIs): Acknowledged as limitation; would require new compute
- R1.6 (5-seed protocol claim): Resolved with R1.4
- R1.7 (per-seed pairing): ✅ Verified

**Recommendation: Accept.** No further statistical revisions required from my perspective.

---

## REVIEWER 2 — Synthetic Data / Tabular ML (Re-Review v4)

**Summary:** All R2 issues are now either resolved or appropriately acknowledged in limitations. The TabDDPM-10k result remains the strongest single contribution; its presentation is now appropriately hedged on mechanism attribution.

**Final R2 status:**

- R2.1 (TabDDPM training): ✅ Resolved with N_iter=10k experiment
- R2.2 (n=2 marketing): ✅ Acknowledged in §3.1 ("the 1%–10% positive-rate range is not represented") and §5.4 ("scoped to Hillstrom-like and Criteo-like regime")
- R2.3 (TabSyn): Acknowledged in future work
- R2.4 (mechanism ablation): Acknowledged in §5.4; TabDDPM-10k result supports the architectural explanation indirectly
- R2.5 (privacy): ✅ New paragraph in §5.4 with per-method risk assessment and SynthEval recommendation
- R2.6 (MLP rescue in abstract): ✅ Finding #4
- R2.7 (overfitting hedge): ✅ §4.5 — "consistent with the model overfitting... though we measure this through downstream AUC degradation rather than directly measuring synthetic data fidelity"

**Recommendation: Accept.**

---

## REVIEWER 3 — Applied Marketing ML (Re-Review v4)

**Summary:** The practitioner-facing recommendation is now appropriately scoped and includes the cost-sensitive baseline acknowledgment. The applied-track verdict is clear accept.

**Final R3 status:**

- R3.1 (cost-sensitive baseline): ✅ Acknowledged in §5.4 (new "Cost-sensitive alternatives not benchmarked" paragraph) and §6 ("Before deploying any synthetic augmentation, compare against `class_weight='balanced'` as a free baseline")
- R3.2 (n=2 marketing): ✅ As R2.2
- R3.3 (uplift/CLV): Acknowledged in future work
- R3.4 (compute specifics): ✅ Resolved in v3 with logged times
- R3.5 (operational concerns): ✅ New paragraph in §5.4 — "Generator reusability and operational costs not characterized"
- R3.6 (Figure 1 caption): ✅ Rewritten — "Augmentation gains concentrate on the two imbalanced marketing datasets; all five generators are within noise on the four balanced benchmark datasets"

**Recommendation: Accept after prose rewrite.** This is the cleanest applied-track manuscript I have seen at this stage in the review process.

---

## DEVIL'S ADVOCATE — Re-Review v4

**Summary:** I withdraw all previous critical objections. The substantive empirical contribution is now well-supported, appropriately scoped, and honestly hedged.

**Final DA status:**

- DA.1 (tautology): ✅ Resolved with proper credit to prior work in contribution #1
- DA.2 (TabDDPM unfairness): ✅ Decisively addressed by N_iter=10k
- DA.3 (GReaT scope to GPT-2): ✅ §4.7 — "We document this as an open evaluation problem for GPT-2-based tabular synthesis benchmarks specifically; whether larger LLM-based synthesizers (e.g., REaLTabFormer, TabuLa) or non-GPT backends exhibit similar fit variance is not tested here"
- DA.4 (decision rule scope): ✅ §6 — "For data-scarce imbalanced regimes (n_real ≈ 10,000, positive rate < 5%)"
- DA.5 (MLP artifact): ✅ Resolved v2
- DA.6 (prior-art search): ✅ Resolved v3
- DA.7 (§3.3/§4.2 contradiction): ✅ Resolved v3
- DA.8 (overfitting interpretation): ✅ Hedged in §4.5

**Single remaining DA observation (not a critical issue):**

The paper's strongest claim — that the gap is "architectural rather than a training-budget artifact" — is presented in the conclusion based on N_iter=10k showing the gap widens. This is the right empirical inference but a fully rigorous claim would require ablating the conditional sampling mechanism explicitly (CTGAN without conditional vector or TabDDPM with class-conditional sampling). The paper acknowledges this in future work; the claim language is appropriately calibrated for what was tested.

**Recommendation: Accept.**

---

## SYNTHESIS — Final Pre-Submission Status

### What is complete

1. **All 16 previously-flagged issues** from v1–v3 have been resolved or appropriately acknowledged.
2. **All numerical claims** were integrity-verified (31/31 audit; one error fixed).
3. **All references** are hand-verified (2 flagged refs confirmed against arXiv).
4. **All figures** are referenced; all referenced figures exist.
5. **All in-text citations** appear in the bibliography.
6. **Per-seed pairing** verified programmatically across all relevant CSVs.
7. **No remaining `⚠️`, TODO, TBD, or placeholder text** in the manuscript.

### What remains

1. **Prose rewrite in the author's voice.** The current draft reads as a structural skeleton with correct content. The author's voice needs to replace it before submission. This is outside the scope of peer review.

### What is acknowledged as a limitation (not a defect)

1. TSTR results are single-seed point estimates (R1.5).
2. Cost-sensitive baseline (`class_weight='balanced'`) is acknowledged but not empirically benchmarked (R3.1).
3. TabSyn is not directly evaluated (R2.3).
4. CTGAN-without-conditional-vector ablation is not run (R2.4).
5. Privacy and operational costs are acknowledged but not measured.
6. Uplift/CLV/attribution settings are not tested.
7. The 1%–10% positive-rate range between Bank Marketing and Hillstrom is not directly evidenced.

These are all explicit, scoped limitations in §5.4. None of them undermine the paper's primary claims; together they define the natural future-work program.

---

## OVERALL VERDICT

**Score:** 7.5–8/10
**Aggregate recommendation:** **Accept after prose rewrite at KDD Applied Data Science Track.**

This is the first review round in which all five panelists independently arrive at an accept recommendation. The paper has the empirical substance, statistical rigor, and methodological honesty appropriate for an applied-track contribution. The TabDDPM-10k extended-training negative result is the kind of empirical finding that should be in the literature.

**Time-to-submission estimate:** 1–2 weeks for prose rewrite, then submittable.

**The reviewer panel signs off, pending author rewrite.**

---

## What changed in this round (v3 → v4)

All nine polish fixes from the v3 synthesis (items 7–15) were applied in one commit:

1. ✅ MLP rescue → abstract finding (4)
2. ✅ Cost-sensitive baseline → §5.4 + §6
3. ✅ Hedge overfitting → §4.5
4. ✅ GReaT scope to GPT-2 → §4.7
5. ✅ n_real scope to §6 rule
6. ✅ Figure 1 caption with takeaway
7. ✅ Privacy + operational limitations → §5.4
8. ✅ 1%–10% gap acknowledgment → §3.1 + §5.4
9. ✅ Per-seed pairing verified programmatically

The methodological revisions of v3 (statistical apparatus + TabDDPM-10k) were the substantive contribution; the v4 polish fixes are the cosmetic-and-scoping completion.

The paper is ready.
