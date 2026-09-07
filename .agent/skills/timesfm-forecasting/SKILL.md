---
name: timesfm-forecasting
description: Support a selected PaperTrace forecasting task with an explicit TimesFM checkpoint, leakage-safe temporal evaluation, actual point or probabilistic forecasts, and bounded interpretation.
---

# TimesFM Forecasting

## Purpose

Use TimesFM when a selected experiment or analysis needs a time-series foundation
model forecast or baseline. The task may involve point forecasts, predictive
quantiles or intervals, covariates supported by the chosen checkpoint, or a
comparison with classical and learned forecasting methods.

This is a supporting capability. `experimental-design` or `statistical-analysis`
defines the forecasting question and evaluation; `06-experiment-ops` executes an
approved run. TimesFM does not choose the estimand, data cutoff, baseline, metric,
or scientific conclusion.

## Workflow

1. Confirm the forecasting target, series/unit identity, sampling frequency,
   context, horizon, available-at-prediction-time covariates, missingness,
   evaluation cutoff, baseline, metrics, and requested output.
2. Inspect the installed TimesFM package, selected checkpoint/model card, and
   current official API before implementation. Record the exact checkpoint and
   revision when reproducibility requires it; do not rely on bundled API or
   hardware snapshots.
3. Verify that the selected model supports the task: univariate or multivariate
   input, frequency handling, context and horizon, covariates, point or
   probabilistic output, and any fine-tuning mode. Stop when the requested
   semantics are unsupported.
4. Build a leakage-safe temporal evaluation. Future observations and unavailable
   future covariates must not enter preprocessing, scaling, model selection, or
   context construction. Use a final holdout or rolling-origin design that
   matches the claim.
5. Define how missing values, irregular timestamps, duplicated timestamps,
   resampling, and short series are handled. Do not interpolate, truncate,
   resample, or coerce frequency silently.
6. Run the exact checkpoint and configuration through the primary execution path.
   Inspect returned dimensions, horizon alignment, timestamps, point/quantile
   meaning, non-finite values, and one simple reference or baseline forecast.
7. Evaluate only metrics that match the target and decision. For probabilistic
   outputs, inspect interval or quantile calibration and sharpness using the
   actual evaluation design; do not impose a universal acceptable coverage band.
8. If anomaly detection is the requested task, define and validate the anomaly
   rule separately. A point outside a forecast interval is not automatically a
   confirmed anomaly.
9. Save the requested forecast table and evaluation result with model identity,
   cutoff, context, horizon, covariate availability, metrics, uncertainty, and
   output path. Generate a figure only when the primary task asks for one.
10. Preserve null, negative, unstable, and contradictory comparisons and update
    the claim or boundary through the primary Skill.
11. Run one closest forecast or evaluation smoke path and inspect its output once.

## Output Contract

Return the direct product requested by the primary Skill, together with:

- data cutoff, independent series/unit, context, horizon, and covariate contract;
- checkpoint/revision and configuration needed to interpret the result;
- actual point and, when requested, probabilistic forecast outputs with explicit
  dimensions and quantile/interval meaning;
- baseline comparison, metrics, uncertainty or calibration, and boundary;
- output path and one direct validation.

A hardware recommendation, API recipe, run row, anomaly list, or figure request
cannot replace the actual forecast and checked evaluation.

## Boundaries

- Do not require target-journal, statistics, ablation, reproducibility,
  decision-log, open-question, insight, or review files before forecasting
  user-supplied data.
- Do not hard-code a preferred checkpoint, parameter count, model version, context
  minimum, output index, quantile mapping, batch size, memory threshold, device,
  runtime estimate, or expected coverage range.
- Do not silently interpolate missing values, truncate context, resample time,
  infer positivity, use future covariates, or change the evaluation cutoff.
- Do not select TimesFM because it is a foundation model; compare it with the
  strongest relevant baseline under the same data and forecast information.
- Do not infer causal effects, mechanism, or confirmed anomalies from forecast
  performance or interval exceedance.
- Do not download gated assets or transmit private series without the required
  user authorization and data boundary.
- Do not commit model weights or caches to the paper repository.
- Do not suppress a result because a classical or simpler baseline performs
  better.
- Do not create a forecasting framework, model registry, hardware gate,
  fallback model chain, generic report, or additional logging surface.
