---
name: umap-learn
description: 'Implementation skill: umap-learn for nonlinear dimensionality reduction (2D/3D embeddings, supervised/semi-supervised UMAP, DensMAP, AlignedUMAP, clustering prep) feeding paper/experiments/ evidence. Do not use as primary — classical ML to scikit-learn, Bayes to pymc, deep training to pytorch-lightning, figures to scientific-visualization.'
---

# umap-learn

## Purpose

Provide implementation guidance and reference material for UMAP (Uniform
Manifold Approximation and Projection) dimensionality reduction with the
`umap-learn` package: unsupervised embeddings for visualization, supervised /
semi-supervised UMAP, DensMAP, AlignedUMAP across related datasets,
Parametric UMAP (neural encoder), inverse transforms, and UMAP-as-clustering-
preprocessing (e.g. feeding HDBSCAN). In Auto-01-tiny-research this is a TIER B
tool skill: it supplies the code recipes that produce the projections and
clusters backing a paper's exploratory claims, and maps every result onto the
`paper/experiments/` ledger so downstream skills (`08-markdown-draft`,
`09-tex-freeze-formalize`, `13-reviewer-response`) can cite it. It does not
run as an execution engine — this repo documents and recipes analyses rather
than shipping production training jobs.

## Use When

- A claim in `paper/experiments/evidence_matrix.md` or an exploratory note in
  `paper/experiments/insights.md` requires a 2D/3D manifold projection of a
  feature matrix (a UMAP scatter, optionally coloured by label/cluster).
- Clustering evidence (e.g. HDBSCAN on a UMAP-reduced space) must be produced
  and logged for `paper/experiments/ablation.md` or an insights figure.
- A supervised or semi-supervised projection is needed to demonstrate class
  separability for a methods or results figure routed to
  `paper/assets/figures/`.
- Time-series / multi-batch data requires comparable embeddings via
  AlignedUMAP, reported in `paper/experiments/insights.md`.
- UMAP is used as feature engineering inside a downstream classical-ML
  pipeline (coordinate with scikit-learn, which owns the supervised head).

Do not use this skill as the primary planning skill: classical supervised/
unsupervised ML analysis should defer to scikit-learn, Bayesian modeling to
pymc, deep-learning training engineering to pytorch-lightning, and figure
rendering into `paper/assets/figures/` to scientific-visualization. It is also
not for linear PCA, t-SNE specifics, large-scale GPU distributed training, or
non-Python stacks.

## Required Inputs

- A numeric feature matrix / dataframe, or a path to data already logged in
  `paper/experiments/run_ledger.md`. Do not invent or fabricate data.
- The claim ID(s) this projection or clustering must support, from
  `paper/experiments/evidence_matrix.md`, so each figure/cluster result can be
  tied back.
- The metric choice (euclidean for scaled numeric, cosine for text/document
  vectors, hamming for binary) mandated by the data shape and by
  `paper/refs/target_journal.md`; preprocessing must match the metric (scale
  for Euclidean-style metrics; do not blindly standardize for cosine/binary).
- The required embedding role: visualization (2-3 components, `min_dist`
  ~0.1), clustering preprocessing (5-10 components, `min_dist=0.0`), or
  feature engineering (higher dimensions) — this determines parameters.
- A target output path for any persisted result under `paper/experiments/` or
  `paper/assets/figures/`.
- `umap-learn>=0.5.12` with `scikit-learn>=1.6`, numba, pynndescent, NumPy,
  SciPy; optional `hdbscan` for clustering and `tensorflow` only if
  Parametric UMAP is explicitly required. Install with e.g.
  `uv pip install 'umap-learn>=0.5.12'`. The user is responsible for
  installing these; this skill does not pin or ship a runtime.
- No API keys or credentials are required. If any external data source needs a
  credential (e.g. a private dataset token), the user must provide it; never
  hardcode or store it. Substitute `<user-provided-key>` for any such token.

## Workflow

1. Read the target claim and its required output (figure vs cluster labels vs
   feature block) from `paper/experiments/evidence_matrix.md` and
   `paper/refs/target_journal.md`. Do not pick a role the claim does not
   sanction.
2. Load only data referenced by `paper/experiments/run_ledger.md`; if the data
   is absent or unlogged, stop (see Stop With) rather than substituting.
3. Preprocess to match the metric: `StandardScaler` for Euclidean numeric
   data; leave binary / sparse text vectors unscaled for hamming/cosine;
   impute/drop non-finite values before `fit` (UMAP enforces finite-value
   checks in `fit`/`update`).
4. Choose parameters by role from `references/api_reference.md`:
   - visualization: `n_neighbors=15, min_dist=0.1, n_components=2`
   - clustering preprocessing: `n_neighbors≈30, min_dist=0.0, n_components=5-10`
   - global structure: `n_neighbors=50-200, min_dist=0.5`
   Do not invent parameter values outside these documented ranges.
5. Fix and record `random_state` for reproducibility (UMAP is stochastic).
6. For clustering, fit UMAP with the clustering-tuned parameters then run
   HDBSCAN on the embedding; evaluate with `adjusted_rand_score`/silhouette
   against any known labels and log honestly.
7. For new-data projection use `transform` (or Parametric UMAP when the
   train/test distributions diverge); fit the reducer on the training split
   only to avoid leakage — coordinate with scikit-learn's leakage rules.
   For semi-supervised UMAP, mark unlabeled samples with `-1` (scikit-learn
   convention) in the `y` vector before `fit`/`fit_transform`
   (`semi_labels[unlabeled_indices] = -1`).
8. Persist: write the projection/cluster table or figure spec to
   `paper/assets/figures/` or `paper/assets/tables/`, append a run row to
   `paper/experiments/run_ledger.md` (algorithm, parameters, `random_state`,
   metric, data ref, claim ID), and update
   `paper/experiments/evidence_matrix.md` status.
9. Surface non-trivial parameter choices or caveats (UMAP can create
   artificial cluster divisions; inverse transforms are unreliable outside the
   convex hull) in `paper/logs/decision_log.md`; record negative results in
   `paper/experiments/dead_ends.md` instead of suppressing them.

## Output Contract

- A run row in `paper/experiments/run_ledger.md` with: algorithm
  (`umap-learn` variant), parameter config, `random_state`, metric, embedding
  role, and the data/claim IDs it supports.
- Updated status in `paper/experiments/evidence_matrix.md` for every claim the
  projection or clustering addresses (`supported` / `partial` / `refuted` /
  `unsupported`).
- A projection scatter or cluster figure spec under `paper/assets/figures/`
  (rendered by scientific-visualization), or a cluster/ablation table under
  `paper/assets/tables/` mirrored into `paper/experiments/ablation.md`.
- A reproducibility note in `paper/experiments/reproducibility.md` covering
  `umap-learn`/numba/scikit-learn versions, seed, metric, and exact data ref.
- Optional decision/dead-end entries in `paper/logs/decision_log.md` and
  `paper/experiments/dead_ends.md`, and exploratory structure notes in
  `paper/experiments/insights.md`.
- No executable training/inference scripts shipped into the repo (this is a
  paper repo, not an ML runtime); code stays as documented recipes in the
  references.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only umap-learn`
- `python src/S03_Scripts/validate_project.py`
- Confirm every run referenced by `paper/experiments/evidence_matrix.md` has a
  matching row in `paper/experiments/run_ledger.md` (no orphan claims).
- Confirm `random_state`, `umap-learn` version, metric, and parameter config
  are recorded in `paper/experiments/reproducibility.md`.
- Confirm the metric/preprocessing pairing is consistent (no unscaled Euclidean
  UMAP, no StandardScaler applied to binary/cosine inputs without reason).
- Confirm clustering claims cross-check UMAP-derived clusters against known
  labels via `adjusted_rand_score` rather than reporting visual separation
  alone.
- Confirm visualization figure rendering is delegated to
  scientific-visualization/matplotlib, not done inline here.

## Boundaries

- Do not run deep-learning, LLM, or GPU-distributed training here as a primary
  skill; Parametric UMAP is optional and documented only — deep training
  engineering defers to pytorch-lightning.
- Do not fabricate embeddings, cluster labels, or benchmark numbers; if a
  result is missing, mark the claim `missing_evidence` and stop.
- Do not `fit` UMAP on the full dataset when a train/test split exists (leakage
  for downstream supervised heads) — fit on the training fold only.
- Do not persist raw trained models / `.pkl` / `.joblib` / embedding arrays as
  binary blobs into the paper repo; record recipes and metrics, not weights.
- Do not write outputs anywhere except `paper/experiments/`,
  `paper/assets/figures/`, `paper/assets/tables/`, and the designated logs;
  never into `paper/tex/`, `paper/refs/`, or `paper/submission/`.
- Do not copy the upstream `scripts/` executable training/inference code into
  this repo; this skill ships `references/` documentation only.
- Do not shadow installed packages: keep project files named `umap.py`,
  `sklearn.py`, `hdbscan.py`, or `tensorflow.py` out of the working path.

## Stop With

- The data needed to compute a claim is not present in
  `paper/experiments/run_ledger.md` and the user has not supplied it.
- The required embedding role or metric is unspecified by
  `paper/refs/target_journal.md` / `paper/experiments/statistics.md` and the
  user has not disambiguated.
- A leakage risk is unavoidable (e.g. fitting UMAP on combined train+test for
  a downstream supervised claim) — report and pause rather than report a
  biased number.
- `umap-learn` or a required dependency is unavailable and the user cannot
  install it; do not silently fall back to t-SNE/PCA.
- The projection shows no meaningful structure (collapsed to a single cluster,
  fragmented disconnected components, or NaN/inf in input) and the user has
  not authorized reporting a `refuted` / exploratory-null finding — surface it
  in `paper/logs/decision_log.md` and wait.

## References

- UMAP API reference: `.agent/skills/umap-learn/references/api_reference.md`
- Symptom-first troubleshooting (`fragmented clusters`, `transform`
  drift, `collapsed embedding`, slow runs): `.agent/skills/umap-learn/references/troubleshooting.md`
- Invocation scenarios: `.agent/skills/umap-learn/examples/prompts.md`
- Workspace artifacts: `paper/experiments/evidence_matrix.md`,
  `paper/experiments/run_ledger.md`, `paper/experiments/statistics.md`,
  `paper/experiments/ablation.md`, `paper/experiments/reproducibility.md`,
  `paper/experiments/dead_ends.md`, `paper/experiments/insights.md`,
  `paper/assets/figures/`, `paper/assets/tables/`,
  `paper/refs/target_journal.md`, `paper/logs/decision_log.md`
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://umap-learn.readthedocs.io/en/latest/ ,
  https://umap-learn.readthedocs.io/en/latest/api.html ,
  https://github.com/lmcinnes/umap
