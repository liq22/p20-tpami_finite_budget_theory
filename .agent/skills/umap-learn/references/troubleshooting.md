# UMAP Common Issues and Solutions

Symptom-first diagnostic map for `umap-learn`, focused on the parameter
knobs that affect figure/cluster quality in a paper workflow. Each entry
names the symptom observed in the embedding and the minimum parameter
change to try. Always re-record `random_state`, the changed parameter,
and the resulting `adjusted_rand_score` / silhouette in
`paper/experiments/run_ledger.md` so the comparison stays auditable.

For the role-to-parameter baseline (visualization vs clustering
preprocessing vs global structure), see
`references/api_reference.md`; this file only covers the
deviation-from-expected cases below.

## Symptom -> Fix pairs

**Symptom:** Disconnected components or fragmented clusters
- **Fix:** Increase `n_neighbors` to emphasize more global structure.

**Symptom:** Clusters too spread out or not well separated
- **Fix:** Decrease `min_dist` to allow tighter packing.

**Symptom:** `transform` results differ significantly from training
embeddings
- **Fix:** Ensure the test-data distribution matches training, or switch
  to Parametric UMAP (a neural encoder that generalizes to new points).

**Symptom:** Slow performance on large datasets
- **Fix:** Keep `low_memory=True` (the default), or reduce dimensionality
  with PCA before UMAP.

**Symptom:** All points collapsed to a single cluster
- **Fix:** Check preprocessing scaling (match it to the metric — see
  Workflow step 3), and increase `min_dist`.

## Notes

- "Poor clustering results" is handled by the clustering-specific
  parameter block (`n_neighbors≈30, min_dist=0.0, n_components=5-10`)
  documented in SKILL.md Required Inputs and Workflow step 4/6; it is
  not repeated here.
- NaN/inf inputs and local-file shadowing (`umap.py`, `sklearn.py`,
  `hdbscan.py`, `tensorflow.py` in the working path) are guarded by
  Workflow step 3 (finite-value check) and Boundaries respectively, so
  they are not duplicated as symptom pairs here.

## Provenance

Ported (condensed) from
`scientific-agent-skills/skills/umap-learn/SKILL.md` (v2.53.0, MIT),
"Common Issues and Solutions" section; see NOTICE.md.
