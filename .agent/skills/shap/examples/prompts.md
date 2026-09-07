# shap — invocation scenarios

Realistic prompts for invoking the shap capability skill inside the
Auto-01-tiny-research workspace. Each scenario shows the kind of request that
should trigger this skill and the workspace artifacts it produces or reads.

## Scenario 1: Global feature importance figure to support a paper claim

> The XGBoost classifier from run `R-014` in `paper/experiments/run_ledger.md`
> backs claim `C-03` in `paper/experiments/evidence_matrix.md`, but the
> reviewer comment in `paper/reviews/ai_review.md` asks which features
> actually drive the predictions. Produce a SHAP beeswarm and a mean-|SHAP|
> bar chart, sized to the journal column width in
> `paper/refs/target_journal.md`, and update the statistics and evidence
> tables accordingly.

This triggers the shap skill because the request is explicitly about
feature attribution for an already-trained, logged model. The skill uses
`shap.TreeExplainer` (the model is a tree ensemble), selects ~200 background
samples from the training set, computes SHAP values on the held-out
evaluation set, renders a colorblind-safe beeswarm plus bar chart at 300 dpi,
and writes PDF + PNG into `paper/assets/figures/`. It appends the mean-|SHAP|
table to `paper/experiments/statistics.md`, adds a provenance row to
`paper/experiments/run_ledger.md`, links the figure to claim `C-03` in
`paper/experiments/evidence_matrix.md`, records the explainer/seed/version in
`paper/experiments/reproducibility.md`, and seeds a reviewer-response stub in
`paper/reviews/response_to_reviewers.md`. Do NOT retrain the model or invent
features; SHAP explains association, not causation, so the draft paragraph
must not become a causal claim.

## Scenario 2: Explaining misclassified predictions and checking for leakage

> While auditing run `R-014` we noticed a few surprising misclassifications.
> For the five worst errors, show per-prediction SHAP waterfalls and a scatter
> of the top two features, and tell me whether any feature looks suspiciously
> dominant (possible data leakage or a proxy). Capture findings in the logs.

This triggers the shap skill because the task is local per-prediction
explanation plus a leakage sanity check on an existing model. The skill
identifies the misclassified indices, generates `shap.plots.waterfall` for
each (plus `shap.plots.scatter` colored by a candidate interacting feature
for the top two mean-|SHAP| features), and visually inspects for an
unexpectedly dominant feature. Any leakage/proxy suspicion is written to
`paper/logs/insights.md` (or `paper/logs/dead_ends.md` if the feature turns
out to be unusable), with the decision rationale in
`paper/logs/decision_log.md`. The diagnostic figures go into a scratch
subdir under `paper/assets/figures/` (not promoted to a claim-supporting
figure unless the user confirms). Stop and report if the model output type
is ambiguous (probability vs. log-odds), because that makes the waterfalls
uninterpretable.
