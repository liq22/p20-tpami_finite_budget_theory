# umap-learn — invocation scenarios

Realistic prompts for invoking the umap-learn tool skill inside the
Auto-01-tiny-research workspace. Each scenario shows the kind of request that
should trigger this skill, the artifacts it reads, and the workspace outputs
it must produce. umap-learn is a TIER B implementation skill: prefer
scikit-learn for the broader classical-ML analysis, scientific-visualization
for figure rendering, and pymc / pytorch-lightning for Bayesian / deep
workflows.

## Scenario 1: 2D UMAP projection to support an exploratory separability claim

> The paper's results section claims our method produces feature
> representations in which the two phenotype classes separate cleanly. Build a
> 2D UMAP projection of the embedding matrix logged in
> `paper/experiments/run_ledger.md` (run `R-021`), coloured by the phenotype
> label, and update claim `C-09` in `paper/experiments/evidence_matrix.md`.
> The target journal (`paper/refs/target_journal.md`) wants every projection
> figure to carry a fixed seed and version note.

This triggers umap-learn because the request is a nonlinear manifold
projection for visualization. The skill reads the data ref and claim, scales
the numeric features with `StandardScaler` (Euclidean metric), fits
`umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, metric='euclidean',
random_state=42)`, and produces the projection arrays plus a figure spec.
It does NOT render the scatter itself — scientific-visualization / matplotlib
owns the low-level rendering into `paper/assets/figures/`. The skill writes a
run row to `paper/experiments/run_ledger.md`, updates `C-09`, and records the
`umap-learn` version, numba version, seed, metric, and parameters in
`paper/experiments/reproducibility.md`. Do NOT fit UMAP on a held-out test
split combined with training if the same split feeds a downstream supervised
model — that leaks. Do NOT persist a `.joblib` reducer blob into the repo;
record the recipe only.

## Scenario 2: HDBSCAN clustering on a UMAP-reduced space for an ablation

> I need an ablation comparing raw-feature HDBSCAN against UMAP-preprocessed
> HDBSCAN, to go into `paper/assets/tables/ablation_clustering.tex` and
> `paper/experiments/ablation.md`. Use the feature matrix from run `R-021`,
> choose `min_cluster_size` sensibly, and score both against the known labels
> with `adjusted_rand_score`. Mark the variant that does not improve over the
> baseline as `partial` in the evidence matrix.

This triggers umap-learn for the UMAP-preprocessing variant: it fits
`umap.UMAP(n_neighbors=30, min_dist=0.0, n_components=10, metric='euclidean',
random_state=42)` (clustering-tuned parameters — denser packing, more
dimensions than visualization), then runs `hdbscan.HDBSCAN` on the embedding.
The raw-features variant stays in scikit-learn's orbit (or a direct HDBSCAN
call). The skill computes `adjusted_rand_score` against the known labels for
both, applies any multiple-comparison note from
`paper/experiments/statistics.md`, emits the LaTeX table to
`paper/assets/tables/` and a mirrored markdown table in
`paper/experiments/ablation.md`, and writes a run row per variant to
`paper/experiments/run_ledger.md`. Honest negative results (UMAP variant that
does not beat raw) go to `paper/experiments/dead_ends.md` rather than being
dropped. The caveat that UMAP can create artificial cluster divisions must be
surfaced in `paper/logs/decision_log.md`.

## Scenario 3: AlignedUMAP across time-series batches for an insights note

> We have per-day feature matrices for the four experiment days (days 1-4,
> each logged as a separate run in `paper/experiments/run_ledger.md`). Produce
> comparable embeddings across the four days so we can describe trajectory
> structure in `paper/experiments/insights.md`, and hand a 2D-per-day panel
> off to scientific-visualization for `paper/assets/figures/`.

This triggers umap-learn: `AlignedUMAP` is the only tool that maintains a
consistent coordinate system across related datasets. The skill loads the
four day matrices, builds the `relations` dictionaries mapping matched sample
indices between consecutive days (required for meaningful alignment), fits
`umap.AlignedUMAP(random_state=42)`, and extracts `embeddings_`. It records
the alignment relations, parameters, and seed in
`paper/experiments/reproducibility.md`, writes a run row to
`paper/experiments/run_ledger.md`, and notes any trajectory structure (or its
absence) in `paper/experiments/insights.md`. If the relations cannot be
constructed (no sample matching between days), stop and surface the blocker
in `paper/logs/decision_log.md` rather than producing an unaligned,
misleading panel. Figure rendering is delegated to scientific-visualization.
