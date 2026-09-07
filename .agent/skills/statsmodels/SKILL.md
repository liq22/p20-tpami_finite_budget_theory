---
name: statsmodels
description: Support an estimand-aligned statistical analysis with the smallest appropriate statsmodels implementation, relevant diagnostics, and honest uncertainty.
---

# statsmodels

## Purpose

Use statsmodels after the primary analysis task has identified the estimand, independent unit, outcome structure, and comparison. It supports regression, generalized linear models, mixed effects, discrete outcomes, and time-series models when those models directly answer the current scientific question.

It is an implementation aid, not a fixed diagnostic battery or a substitute for `statistical-analysis`.

## Workflow

1. Confirm the estimand, outcome type, independent unit, dependence structure, covariates, comparison, and allowed interpretation. Stop if these semantics are missing.
2. Choose the simplest model and formula that represent the design. Do not select a model because it gives a preferred coefficient or p-value.
3. Handle missingness, categorical variables, grouping, exposure, and temporal order explicitly. Do not silently drop, impute, difference, transform, or re-label observations.
4. Fit the model and surface convergence, separation, singularity, identification, or numerical warnings directly.
5. Run only diagnostics that can invalidate the chosen model or change its uncertainty. Select robust, clustered, heteroskedastic, or autocorrelation-aware covariance from the design and observed failure, not from a universal checklist.
6. Compare alternative specifications only when they distinguish a scientific explanation or materially test sensitivity. Keep comparison data and tuning conditions matched.
7. Report the relevant estimate, contrast, prediction, or model comparison with uncertainty and sample/cluster count. Separate statistical association from causal or mechanistic interpretation.
8. Produce the requested code, table, or analysis result. Record a real completed run and update formal claim support only when those records are in use.
9. Preserve failed fits, null effects, instability, and contradictory results, and update the claim or boundary accordingly.
10. Run the closest script, unit test, or reproducible fit and inspect its output once.

## Output Contract

Return:

- model family, formula, estimand, and independent unit;
- data handling and covariance choices that affect inference;
- actual estimate and uncertainty;
- relevant diagnostics and any unresolved model failure;
- comparison or sensitivity result when decision-relevant;
- the resulting claim decision and one direct validation.

Tables and figures are produced only when requested. A run record or statistical note is supporting material, not the primary result.

## Boundaries

- Do not require a target-journal, statistics, ablation, reproducibility, decision-log, dead-end, or insight file before performing a bounded analysis.
- Do not run every available normality, heteroskedasticity, autocorrelation, influence, or stationarity test by default.
- Do not automatically switch model families, covariance estimators, transformations, or differencing rules without making the change explicit.
- Do not treat a passing diagnostic as proof that the scientific model is correct.
- Do not infer causality from an associational design.
- Do not silently ignore convergence, separation, singularity, or identification failures.
- Do not create general-purpose wrappers, model registries, report generators, or fallback chains.
- Do not suppress or delay reporting a result because it weakens the current claim.
