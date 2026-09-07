---
name: scikit-learn
description: Support a selected PaperTrace task with leakage-safe classical machine-learning implementation, matched evaluation, and directly inspectable results.
---

# scikit-learn

## Purpose

Use scikit-learn when a selected code, experiment, or analysis task needs a classical classification, regression, clustering, dimensionality-reduction, preprocessing, or model-selection implementation.

This is a supporting capability. The primary Skill defines the scientific question, comparison, estimand, and requested product. scikit-learn supplies the smallest correct implementation and result needed for that decision.

## Workflow

1. Confirm the actual data, target, independent unit, split, metric, and decision. If label, grouping, temporal order, or train/test semantics are ambiguous, stop rather than infer them.
2. Reproduce the current baseline or failing behavior before changing the implementation.
3. Put learned preprocessing inside a `Pipeline` or equivalent fold-local path. Use grouped or temporal splitting when observations are dependent; do not treat windows, folds, or repeated measurements as independent samples.
4. Choose the simplest estimator family that can answer the question. Compare methods with the same data, preprocessing, target information, tuning budget, and evaluation code.
5. Tune only parameters that could change the decision. Keep the final test set outside model and hyperparameter selection.
6. Evaluate at the correct independent unit. Report the requested point estimate and uncertainty or repeated-run variation when they affect interpretation.
7. Produce the actual requested source, notebook, table, or result. Add a completed row to `paper/experiments/run_ledger.md` only when a real run occurred; update `evidence_matrix.md` only when a formal claim exists.
8. Preserve null, negative, unstable, and contradictory results. Revise or refute the claim when the result requires it; no additional authorization is needed to report an observed result honestly.
9. Run the closest test or smoke path and inspect the produced output once.

## Output Contract

Return the direct product requested by the primary Skill, together with:

- model and preprocessing actually used;
- split, independent unit, metric, and comparison conditions;
- actual result and relevant uncertainty;
- leakage or fairness limitations that affect the conclusion;
- the resulting claim or method decision;
- one targeted validation.

Persist a fitted model only when the task requires a reusable artifact, and state its path and reconstruction requirements. Supporting records must not replace the source code or analysis result.

## Boundaries

- Do not require pre-existing ledger, statistics, ablation, reproducibility, decision-log, or target-journal files before inspecting user-supplied data.
- Do not run a broad estimator or hyperparameter sweep merely because the library supports it.
- Do not choose the metric, split, preprocessing, or model after observing which option gives the preferred conclusion.
- Do not silently fall back to another estimator, split, library, or task when a dependency or scientific input is missing.
- Do not create generic experiment plans, dashboards, extra logs, or model registries.
- Do not hard-code a library version unless the current project requires it.
- Do not use this Skill for deep neural-network training or Bayesian inference.
- Do not suppress a result because it weakens the current claim.
