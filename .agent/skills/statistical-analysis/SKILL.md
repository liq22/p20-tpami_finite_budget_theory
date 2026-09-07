---
name: statistical-analysis
description: Analyze actual experimental data with the smallest statistical model needed to answer the estimand, respect the independent unit, quantify uncertainty, and bound the paper claim without mechanical significance testing.
---

# Statistical Analysis

## Purpose

Use statistics to answer a scientific question, not to manufacture rigor or
significance. The product is a correct analysis result and interpretation tied to
the actual data and design.

## Workflow

1. State the claim, estimand, comparison, outcome, and conclusion the analysis may
   change.
2. Inspect the actual data source and experiment protocol. Confirm the independent
   unit, pairing/repeated structure, missingness, and grouping before fitting a
   model.
3. Summarize the observed data first: sample/unit counts, distribution, central
   tendency, spread, and any obvious data-quality issue relevant to the claim.
4. Choose the simplest analysis consistent with the design:
   - descriptive estimate when inference is unnecessary;
   - paired/independent comparison when the design is simple;
   - regression or hierarchical/mixed model when covariates, clusters, or
     repeated units require it;
   - bootstrap, permutation, robust, non-parametric, or Bayesian analysis only
     when it answers the question better.
5. Check assumptions that could materially invalidate this model. Do not run a
   fixed battery of tests or silently switch methods after seeing significance.
6. Estimate the relevant magnitude and uncertainty. Use an effect size,
   confidence/credible interval, repeated-seed summary, or distributional report
   when appropriate to the estimand.
7. Add multiplicity correction, sensitivity analysis, alternative model, or
   missing-data analysis only when the actual claim depends on it.
8. Separate:

   ```text
   observed fact
   statistical inference
   mechanistic interpretation
   unresolved hypothesis
   ```

9. Save the actual result/table/plot or analysis output and update the minimum
   paper record needed to reuse the number.
10. State whether the claim is supported, weakened, refuted, or unresolved and
    give the important boundary.

## Output Contract

Produce:

- the data and independent unit analyzed;
- the selected model/test and why it matches the design;
- actual estimates, uncertainty, and relevant diagnostics;
- a result artifact or table when requested;
- an honest interpretation and claim boundary;
- one decisive follow-up only when the current analysis cannot resolve the
  question.

Use field-appropriate reporting rather than forcing APA style onto every domain.

## Boundaries

- Do not fabricate data, p-values, confidence intervals, Bayes factors, or sample
  sizes.
- Do not treat windows, frames, cells, repeated measurements, folds, or seeds as
  independent replicates when the scientific unit is higher-level.
- Do not require a p-value, effect size, confidence interval, normality test,
  Bayesian alternative, power analysis, or sensitivity suite merely to look
  rigorous. Use what the inference requires.
- Do not select among tests after observing which gives the preferred result.
- Do not interpret non-significance as proof of no effect or significance as
  practical importance.
- Do not turn one analysis into mandatory updates across statistics, evidence,
  run, reproducibility, ablation, decision, change, review, and figure files.
  Update only records made stale by the result.
- Do not run a clean-room replay or full project validator unless the analysis
  implementation itself changed or final PR review is underway.
- Fail clearly when the data, estimand, independent unit, or comparison is
  undefined; do not infer them from filenames or desired conclusions.
