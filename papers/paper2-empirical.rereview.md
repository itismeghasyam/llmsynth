# Peer Review Panel — Re-Review of `paper2-empirical.md`

**Manuscript:** *When Class Imbalance Dominates: A Controlled Empirical Study of Synthetic Data Augmentation for Marketing Classification*
**Re-review date:** 2026-06-07
**Reviewers:** EIC + R1 (statistical methods) + R2 (synthetic data) + R3 (applied marketing ML) + DA (Devil's Advocate)
**Previous review:** `paper2-empirical.review.md`
**Mode:** Re-review — verify which previous issues are resolved, identify what remains and what is new.

---

## EDITORIAL ASSESSMENT — Editor-in-Chief

**Verdict:** Substantial progress on the cosmetic and integrity issues. The paper is now structurally complete with figures, full bibliography (26 refs), and verified numbers (30/31 in the last audit, the one error since corrected). However, **the four critical methodological issues from the first review remain unaddressed**. The MLP-on-Criteo issue was resolved differently than the panel recommended (and in fact strengthens the paper), but the four headline gaps remain.

**Status of critical issues from first review:**

| First-review issue | Status |
|---|---|
| Statistical apparatus (paired tests, FDR) | ❌ Not addressed |
| TabDDPM at library defaults | ❌ Not addressed |
| MLP Criteo treatment | ✅ **Resolved** — root-cause diagnosis corrected (sklearn convergence failure, not Metal GPU); reframed as a finding (CTGAN rescues all 10 seeds) |
| Single-seed §4.2 mislabeled as CI | ⚠️ Partially — §3.3 now states "TSTR results on benchmark datasets and the original §4.2 augmentation sweep are reported under a single-seed protocol... we mark these explicitly as point estimates"; but the §4.2 table still shows "0.844 ± 0.015" without explanation of what the ± represents |
| n=2 marketing datasets | ❌ Not addressed |

**The MLP fix is genuinely good.** The previous draft had a logically inconsistent treatment (excluding the baseline as "broken" while keeping augmented results from the same setup). The corrected diagnosis is more honest *and* delivers a stronger finding — augmentation rescuing a fully-failed classifier is the most dramatic single result in the paper. This is rewriting at its best.

**The remaining critical issues are existential.** Without paired statistical tests, the comparison claims are reviewer-vulnerable. Without a tuned TabDDPM run, the headline novelty claim is contestable. These are not optional improvements — they are gate conditions for KDD Applied.

**Recommendation unchanged: Major revision.** Estimated score improvement: 4/10 → 5/10 (figures, MLP fix, number correction). Final 7/10 target still requires the four unresolved items.

---

## REVIEWER 1 — Statistical Methods (Re-Review)

**Summary:** The numerical integrity is now verified (31/31 checks, per the audit report appended to commit history). However, **none of the four R1 points from the first review have been addressed.** The paper has 5–10 seeds per cell — enough data for proper inferential tests — but does not run them.

### Status of previous R1 issues:

**R1.1 Paired tests on headline comparisons — ❌ Not addressed.**
The TabDDPM vs CTGAN comparison in §4.5 still reports mean differences (+4.40, +2.96 pts) without paired t-statistics or effect sizes. The per-seed Δ values are sitting in the result CSVs. A 10-line script would produce a paired t-statistic, p-value, and Cohen's d_z for each comparison. The author did this for the GReaT n=2000 result (paired p=0.001 cited in §4.7) but did not extend the analysis to the headline TabDDPM-vs-CTGAN finding.

**R1.2 Multiple-comparison correction — ❌ Not addressed.**
The paper makes roughly 40 distinct numerical comparisons (TSTR × 3, augmentation × 4 benchmarks × 3 generators, marketing × 2 × 4 generators × 5 alphas, multi-classifier × 2 × 4 classifiers × 3 generators × 5 alphas, GReaT × 6 n-values). The selection of "best α per cell" is a per-cell multiple comparison; the aggregation into headlines is a family-level one. The improvement plan in the original draft pre-registered BH-FDR at q=0.10 — none of that apparatus is in this paper.

**R1.3 Formal hypothesis test — ❌ Not addressed.**
The paper claims to "test the hypothesis that class imbalance is the primary and sufficient condition" but never formalizes or runs the test. The cleanest formalization: compute per-seed Δ_CTGAN-Baseline for each dataset, regress Δ on `log(positive_rate)`, report the coefficient and CI. This is a 20-line analysis with the data the paper already has.

**R1.4 §4.2 ± labels — ⚠️ Partially addressed.**
The protocol section (§3.3) now distinguishes 5-seed CIs from single-seed point estimates. But the §4.2 table headers and cells still display "0.844 ± 0.015" formatting that visually reads as a CI. A casual reviewer scanning §4.2 will not register the protocol distinction. Fix: either (a) re-run §4.2 with 5 seeds (the data exists — `ci_telco_churn.csv` etc. have 5 seeds per row, the table is just labeled with the wrong protocol claim), or (b) recompute the §4.2 ± as the actual per-seed CI from the available data and update the protocol claim accordingly.

**R1.5 §4.1 TSTR confidence intervals — ❌ Not addressed.**
TSTR results in §4.1 are still single-seed point estimates with no CIs. Add or move to appendix.

### New R1 issue from the re-review

**R1.6 (New) — §4.2 table uses 5-seed data but cites the result as single-seed.**
Spot-checking: `ci_telco_churn.csv` contains 5 seeds × 5 methods × 5 alphas = 125 rows. The baseline AUC of 0.844 with ±0.015 in the §4.2 table is a 5-seed t-CI, *not* a single-seed point estimate. So the protocol claim in §3.3 is wrong: §4.2 is in fact 5-seed CI for the benchmark datasets. This is a documentation bug, not a data problem. **Action: update §3.3 to remove the "single-seed" caveat for §4.2, and remove the duplicate "point estimate" claim.**

**Recommendation:** Major revision. R1.1–R1.3 are non-negotiable for a "controlled empirical study" framing. R1.6 needs to be fixed before the paper makes any "single-seed point estimate" claim about §4.2 — the data is 5-seed.

---

## REVIEWER 2 — Synthetic Data / Tabular ML (Re-Review)

**Summary:** Two of my five issues are minorly improved (citations, MLP). The three critical issues — TabDDPM hyperparameter tuning, n=2 marketing datasets, TabSyn omission — are not addressed.

### Status of previous R2 issues:

**R2.1 TabDDPM hyperparameters at library defaults — ❌ Not addressed.**
This was my top critical issue and the paper's central comparative claim. The paper still uses synthcity defaults (N_iter=2000, num_timesteps=1000). A reviewer at KDD will ask: did you try N_iter=10000? num_timesteps=2000? Class-conditional sampling? If not, the "TabDDPM loses to CTGAN" claim is conditional on a configuration that the TabDDPM authors themselves would likely call undertrained.

**Required action for resubmission:** at least one TabDDPM ablation with extended training (a single seed on Criteo at N_iter=10000 is enough as a sanity check). If the gap closes, soften the abstract. If it doesn't, the claim survives. Either way, the result must be reported.

**R2.2 Two marketing datasets too thin — ❌ Not addressed.**
The 1%–10% positive-rate range (between Bank Marketing at 11.7% and Hillstrom at 0.9%) is still empty. The paper's strongest claim — "imbalance is the switch" — requires evidence that the switch is gradual rather than a step function. Without an intermediate dataset, "switch" is metaphor, not finding.

**R2.3 TabSyn omission — ❌ Not addressed.**
The practitioner-facing conclusion (default to CTGAN) cannot survive in the presence of an untested alternative (TabSyn) that the cited prior work (Davila et al. 2025) flags as competitive with or above TabDDPM on augmentation. Acknowledged but not resolved.

**R2.4 Mechanism ablation — ❌ Not addressed.**
The §5.2 explanation that "CTGAN's conditional vector explicitly targets the minority class" remains speculative without an ablation. A single run of CTGAN with `condvec=False` on Criteo would convert this from hypothesis to evidence.

**R2.5 Privacy and fidelity not evaluated — ❌ Not addressed.**

### What did improve

The MLP-Criteo treatment (R2 was silent on this in the first review but had implicit concerns) is now sound. The figures are in place. The reference list is appropriate scope for an applied paper.

### New R2 issue

**R2.6 (New) — The MLP convergence finding deserves prominent treatment.**
The current draft buries the "CTGAN rescues 7/10 MLP seeds" finding in §4.6 with a single paragraph. This is arguably the most striking single result in the paper and the strongest evidence for the augmentation-as-rescue mechanism. Consider:
- Promoting it to a separate subsection or callout box
- Adding a figure showing per-seed AUC distribution for MLP-on-Criteo baseline vs CTGAN-augmented (the existing data supports this with no new compute)
- Citing it in the abstract

This is a content recommendation, not a critical issue.

**Recommendation:** Major revision. R2.1 is the most important single item from the entire review panel — fixing it would substantially strengthen the comparative claim.

---

## REVIEWER 3 — Applied Marketing ML (Re-Review)

**Summary:** The paper now reads well as a structured empirical study. My concerns were less about the methodology than about generality and practical usability; those concerns persist.

### Status of previous R3 issues:

**R3.1 Cost-sensitive baseline comparison — ❌ Not addressed.**
Practitioners try `class_weight='balanced'` before any synthetic augmentation. The paper has not added this comparison. Without it, the practitioner-facing recommendation cannot account for the cheapest alternative.

**R3.2 n=2 marketing datasets — ❌ Not addressed.** Same as R2.2.

**R3.3 Uplift/CLV scope — ❌ Not addressed.** Still only in future work.

**R3.4 "20× compute cost" specifics — ⚠️ Partially.**
The paper now says "CTGAN ≈ 2 min CPU; TabDDPM ≈ 45 min GPU" in the §4.5 table. This is helpful but still anecdotal. A simple wall-clock log table would convert this to evidence.

**R3.5 Operational concerns — ❌ Not addressed.**

### What did improve

The MLP-as-rescue framing is the most practitioner-relevant finding in the paper, and the corrected diagnosis raises its visibility. Decision-makers care more about "without augmentation this classifier fails" than "with augmentation it improves by 12 points."

### New R3 issue

**R3.6 (New) — The cross-dataset summary figure (Figure 1) deserves a caption with the headline takeaway.**
The figure is referenced as a "cross-dataset summary," but a practitioner reading the paper for the bottom line will scan Figure 1 first. The caption should explicitly state: "Augmentation gains concentrate on positive rates below 5%; all generators are within noise on balanced datasets."

**Recommendation:** Major revision, lean accept. The applied-track verdict depends on R2.1 and R3.1 being addressed; my own concerns are downstream of those.

---

## DEVIL'S ADVOCATE — Re-Review

**The first review's central challenge — that the imbalance finding is a tautology dressed as a discovery — is structurally unaddressed.** The current draft still presents contribution #1 as "controlled evidence that class imbalance is the necessary and sufficient condition," which is precisely the framing my first review rejected.

### Status of previous DA issues:

**DA.1 Tautology critique — ❌ Not addressed.**
The paper still frames imbalance-as-driver as a discovery rather than a multi-generator confirmation. The fix is a sentence-level edit, not a re-run. The abstract bullet should read something like "We confirm — across multi-generator, multi-classifier, multi-seed evidence — that the imbalance regime identified by prior work (Chawla et al. 2002; Fonseca & Bacao 2023; Won et al. 2026) holds with the addition of TabDDPM as a comparator."

**DA.2 TabDDPM unfair comparison — ❌ Not addressed.** Same as R2.1.

**DA.3 GReaT-fit variance scope — ❌ Not addressed.**
The variance finding is still framed as a general claim about LLM-based synthesis. Without a second LLM-based generator tested, this overclaims. Scope must explicitly limit to GPT-2 117M.

**DA.4 "Decision rule oversimplifies" — ❌ Not addressed.**
The §6 conclusion still says "if positive rate < 5%, run CTGAN at α ∈ {0.1, 0.3}." The dataset-size dimension is not in the rule.

**DA.5 MLP Criteo artifact — ✅ Resolved.**
The corrected diagnosis (sklearn convergence failure, not Metal GPU) is technically sound and converts the issue into a finding. The internal inconsistency is gone. This is the cleanest single fix in the revision.

**DA.6 Prior-art search for CTGAN-vs-TabDDPM on marketing data — ❌ Not addressed.**
The "first direct head-to-head" claim still has no documented prior-art check. Even a brief paragraph stating "to our knowledge, no prior work reports..." with the search terms used would satisfy this.

### New DA issue

**DA.7 (New) — The §3.3 protocol section now contains an internal contradiction.**
The protocol claim "Benchmark dataset results (§4.1–4.3) ... are point estimates rather than confidence-interval estimates" is contradicted by §4.2 results showing 5-seed confidence intervals. Either §4.2 is single-seed and the ± values are something else (cross-validation folds?), or §4.2 is multi-seed and the protocol claim is wrong. **The current state is logically inconsistent.** R1.6 covers the same issue from a statistical angle.

**Recommendation:** Reject — though I revise my recommendation downward in severity given the MLP fix and structural improvements. **Conditional accept after major revision with DA.1, DA.3, DA.6, and DA.7 specifically addressed.**

---

## SYNTHESIS — Re-Review Conclusions

### Issues resolved between reviews

1. **MLP-Criteo treatment** (DA.5, R2 implicit, R3 minor) — Resolved cleanly. The corrected diagnosis is more honest and yields a stronger finding.
2. **Numerical integrity** (cross-cutting) — Verified 31/31 checks; one error fixed (Nomao dense 0.972→0.992).
3. **Figure references** (R3 minor) — All 12 relevant plot files now referenced as Figures 1–5.
4. **Reference list scope** (R2 minor) — Expanded from 9 to 26 references with 2 flagged for hand-verification.

### Issues that remain critical (must address for acceptance)

5. **Statistical apparatus** (R1.1, R1.2, R1.3) — Paired tests, effect sizes, multiple-comparison correction. The data exists; the analysis does not.
6. **TabDDPM hyperparameter sensitivity** (R2.1, DA.2) — At minimum one extended-training TabDDPM run on Criteo.
7. **Single-seed labeling inconsistency** (R1.4, R1.6, DA.7) — §3.3 protocol claim contradicts §4.2 results. Resolve documentation, then re-verify.
8. **n=2 marketing datasets** (R2.2, R3.2) — Either add intermediate-imbalance dataset or scope claims to "Hillstrom-like and Criteo-like."

### Issues that remain important (should address)

9. **Tautology framing** (DA.1) — Credit prior work for the imbalance hypothesis; reframe contribution as multi-generator confirmation with TabDDPM addition.
10. **Cost-sensitive baseline** (R3.1) — `class_weight='balanced'` comparison on Hillstrom and Criteo.
11. **TabSyn comparison** (R2.3) — At least one run.
12. **Mechanism ablation** (R2.4) — CTGAN without conditional vector OR TabDDPM with conditional sampling.

### Issues that are content improvements (nice to address)

13. **MLP-rescue finding deserves abstract mention** (R2.6, new) — Strongest single result in the paper.
14. **Figure 1 caption with takeaway** (R3.6, new).
15. **Prior-art search documentation** (DA.6).
16. **GReaT scope to GPT-2 117M** (DA.3).
17. **Operational details** (R3.4, R3.5).

---

## OVERALL VERDICT

**Score:** 5/10 (current, after re-review) → estimated 7.5/10 after must-have revisions

**Aggregate recommendation:** Major revision, **lean toward accept after revision** at KDD Applied Data Science. The substantive empirical contribution is now well-documented; the methodological apparatus around it is not. Issues #5–#8 are blockers; everything below is improvement-tier.

**Comparative assessment vs first review:**
- First review verdict: Major revision
- Re-review verdict: Major revision
- Net progress: ~1 point on the editor's internal scale; substantial cosmetic improvement; no movement on the four critical methodological issues
- Time-to-resubmission estimate: 2–3 days for items #5 and #7 (statistical apparatus + labeling fix); 1–2 days for item #6 (one TabDDPM ablation); 3–5 days for item #8 (add intermediate dataset). Total ~1 working week with no new compute beyond one TabDDPM run.

The paper has a real finding worth publishing and a corrected MLP-rescue result that elevates it. The remaining gap to acceptance is statistical rigor and one head-to-head TabDDPM tuning run — both achievable within a week. Recommend the author prioritize items #5 (statistical apparatus) and #7 (labeling fix) as the first sprint; these are zero-compute fixes that close the most-visible reviewer-flagged gaps.
