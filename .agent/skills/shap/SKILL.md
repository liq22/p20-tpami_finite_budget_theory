---
name: shap
description: 'Compute SHAP feature attributions and produce interpretability evidence for a trained ML model. Use when a paper claim needs feature-importance support, a single prediction must be explained, or reviewers demand XAI. Do not use for causal inference, unsupervised clusters with no model, or as a substitute for held-out evaluation.'
---

# shap

## Purpose

Compute SHAP values for a trained, evaluated model and turn them into
auditable interpretability evidence for the paper: global feature importance
(beeswarm / bar), single-prediction breakdowns (waterfall / force), and
feature-relationship views (scatter / heatmap). SHAP attributes each
feature's contribution to a prediction as the deviation from a baseline
(expected model output), grounded in Shapley values from cooperative game
theory. Works with tree-based models (XGBoost / LightGBM / CatBoost /
Random Forest), linear models, and any black-box via model-agnostic
explainers. This is a TIER A core capability skill: its outputs map heavily
onto the single-paper workspace (evidence, figures, statistics, reviews).

## Use When

- A model trained and recorded in `paper/experiments/run_ledger.md` must be
  explained to support a paper claim (which features drive the prediction).
- A reviewer (or `paper/reviews/ai_review.md`) requests feature importance,
  bias/fairness analysis, or per-prediction explanations.
- You must justify a specific prediction or detect data leakage / unexpected
  feature reliance during model debugging.
- A figure in `paper/assets/figures/` needs a SHAP beeswarm, bar, waterfall,
  scatter, force, or heatmap plot.
- Comparing feature importance across candidate models to pick the most
  interpretable one (feed results into `paper/experiments/ablation.md`).
- A fairness/bias analysis is needed across cohort subgroups.

Do NOT use this skill for causal claims (SHAP shows association, not
causation), for unsupervised methods with no predictive model, or to replace
held-out accuracy/validation metrics. For general figure planning and
journal-fit styling, prefer `scientific-visualization` and hand off only the
SHAP-specific rendering here.

## Required Inputs

- A trained, evaluated model plus the background/evaluation data (NumPy /
  pandas) it was scored on, referenced from `paper/experiments/run_ledger.md`
  (a run id) or supplied directly by the user.
- The feature names and, if relevant, the model output type to explain
  (probability vs. log-odds/margin vs. raw regression output). Mismatches
  here are the most common source of misinterpreted SHAP values.
- The target journal figure constraints from `paper/refs/target_journal.md`
  (column width, font, vector vs. raster, colorblind-safe palette).
- The claim id(s) the explanation supports, so the figure can be linked from
  `paper/experiments/evidence_matrix.md`.
- No API keys or credentials are required by this skill. If a wrapped
  experiment-tracking integration (e.g. MLflow) needs a credential, the user
  must provide it; never hardcode or store it.

## Workflow

1. Confirm the model is already evaluated and logged in
   `paper/experiments/run_ledger.md`. Do not train or tune here.
2. Pick the right explainer for the model family (see
   `.agent/skills/shap/references/explainers.md`):
   - Tree-based -> `shap.TreeExplainer` (fast, exact).
   - Linear -> `shap.LinearExplainer`.
   - Deep net (TF/PyTorch) -> `shap.DeepExplainer` or `GradientExplainer`.
   - Any other black-box -> `shap.KernelExplainer` / `PermutationExplainer`
     (slower; use only when no specialized explainer applies).
   - Unsure -> `shap.Explainer` auto-selects.
3. Select background data: 50-1000 representative training samples (or kmeans
   summary); the baseline affects magnitudes but not relative importance.
4. Compute SHAP values on the evaluation set; for very large sets, sample or
   batch to keep plots legible and compute tractable.
5. Start global, then go local: beeswarm / bar for overall importance, then
   scatter for the top features, then waterfall / force for representative or
   misclassified predictions (see `.agent/skills/shap/references/plots.md`).
6. Check for data leakage: unexpectedly dominant features may indicate a leak
   or a proxy; record findings in `paper/logs/insights.md` or
   `paper/logs/dead_ends.md`.
7. Render figures with a perceptually-uniform / colorblind-safe colormap,
   sized to the journal column width, exported as PDF (vector) + PNG preview
   into `paper/assets/figures/`.
8. Record provenance in `paper/experiments/run_ledger.md`, link the figure to
   its claim id(s) in `paper/experiments/evidence_matrix.md`, and add the
   mean-|SHAP| table to `paper/experiments/statistics.md`.
9. Log methodology (explainer, background-data choice, model output type,
   seed) in `paper/experiments/reproducibility.md` and any decision in
   `paper/logs/decision_log.md`.

## Output Contract

- One or more figures under `paper/assets/figures/` (PDF + PNG), named to
  match the figure id used in `paper/experiments/evidence_matrix.md`.
- A feature-importance table (mean |SHAP|, with sign / direction) added to
  `paper/experiments/statistics.md`.
- A provenance row in `paper/experiments/run_ledger.md` (source run id,
  explainer, background-data size, output type) and, where the explanation
  supports a claim, a row in `paper/experiments/evidence_matrix.md`.
- A reproducibility note in `paper/experiments/reproducibility.md` capturing
  explainer choice, background-data sampling, random seed, and SHAP library
  version.
- For reviewer-driven requests, a draft paragraph / response stub in
  `paper/reviews/response_to_reviewers.md` referencing the new figure.
- A `paper/logs/change_log.md` entry if figures are regenerated post-freeze
  (post-freeze changes also touch `paper/tex/`).

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only shap`
- `python src/S03_Scripts/validate_project.py`
- Confirm SHAP additivity holds: `sum(shap_values[i]) + base_value ==
  model_output[i]` (within tolerance) for the explained output type.
- Confirm the model output type matches what the claim/figure caption states
  (probability vs. log-odds vs. raw margin) — a mismatch invalidates the
  interpretation.
- Confirm every figure supporting a claim is not linked to a claim that
  `paper/experiments/evidence_matrix.md` marks `unsupported`,
  `missing_evidence`, or `refuted`.
- Confirm figure size/DPI and palette satisfy
  `paper/refs/target_journal.md`.

## Boundaries

- SHAP quantifies association, not causation. Never let an interpretation
  become a causal claim in `paper/draft/` or `paper/tex/` without separate
  causal evidence.
- Do not train, tune, or change the model here; explain the model already
  logged in the ledger.
- Do not fabricate or smooth SHAP values to make a feature look important;
  plot only values computed from the supplied model and data.
- Do not explain a model whose evaluation metrics are missing or
  unsatisfactory — interpretations of a bad model are not paper evidence.
- Do not write figures outside `paper/assets/figures/` (or a named scratch
  dir); never into `paper/tex/`, `paper/refs/`, or `paper/submission/`.
- For fairness/bias analysis, do not single out protected attributes without
  the cohort definitions and mitigation context the user must approve.

## Stop With

- The model is not in `paper/experiments/run_ledger.md` or its evaluation
  metrics are missing / clearly inadequate.
- The model output type is ambiguous (cannot tell probability vs. log-odds),
  which makes SHAP values uninterpretable.
- The requested interpretation would imply a causal claim from associational
  attributions.
- Background data cannot be assembled (no training-set access) and the user
  has not supplied an alternative.
- The chosen explainer is unavailable (e.g. `shap` not installed, or
  `DeepExplainer` lacks the required backend) — report the failure and suggest
  the nearest specialized explainer rather than silently falling back to a
  very slow `KernelExplainer` on a large set.

## References

- Explainer catalog: `.agent/skills/shap/references/explainers.md`
- Visualization guide: `.agent/skills/shap/references/plots.md`
- Workflows (debugging, fairness, model comparison, production):
  `.agent/skills/shap/references/workflows.md`
- Theory (Shapley values, algorithms, interaction values):
  `.agent/skills/shap/references/theory.md`
- Workspace artifacts: `paper/experiments/run_ledger.md`,
  `paper/experiments/evidence_matrix.md`,
  `paper/experiments/statistics.md`,
  `paper/experiments/reproducibility.md`,
  `paper/experiments/ablation.md`, `paper/assets/figures/`,
  `paper/reviews/response_to_reviewers.md`,
  `paper/refs/target_journal.md`, `paper/logs/decision_log.md`,
  `paper/logs/insights.md`.
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills
  v2.53.0 (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://shap.readthedocs.io/ ,
  https://github.com/shap/shap ; Lundberg & Lee (2017), "A Unified Approach
  to Interpreting Model Predictions"; Lundberg et al. (2020), "From local
  explanations to global understanding with explainable AI for trees".
