---
name: torch-geometric
description: 'Implementation skill for PyG GNNs (Data/HeteroData, GCN/GAT/GraphSAGE/GIN, message passing, neighbor sampling). Use to implement a GNN backing a paper/experiments/ claim. Do not use for NetworkX analytics, classical ML (scikit-learn), training orchestration (pytorch-lightning), or Bayesian inference (pymc); planning skill primary.'
---

# torch-geometric

## Purpose

Provide an implementation-only reference for building Graph Neural Networks with
PyTorch Geometric (PyG 2.7.x on PyTorch 2.6+): graph data structures (`Data`,
`HeteroData`), the `torch_geometric.nn` layer catalogue, custom `MessagePassing`
layers, neighbor sampling for large graphs, custom dataset loaders, and
GNN explainability. In Auto-01-tiny-research this is a TIER B (tool) skill: it
documents the implementation recipes that produce the evidence behind graph-shaped
claims, and maps every result onto `paper/experiments/` so downstream skills
(`08-markdown-draft`, `09-tex-freeze-formalize`, `13-reviewer-response`) can cite
it. It is a supporting implementation skill; the relevant planning/capability
skill should be preferred as primary — classical ML defers to scikit-learn,
plotting to scientific-visualization, deep-learning training engineering to
pytorch-lightning, and Bayesian modeling engine to pymc.

## Use When

- A claim in `paper/experiments/evidence_matrix.md` is realized by a node-,
  link-, or graph-level GNN (e.g. node classification on Cora, graph
  classification on a TUDataset, link prediction) and you need the implementation recipe.
- You must select a PyG conv layer (`GCNConv`, `GATConv`/`GATv2Conv`,
  `SAGEConv`, `GINConv`, `TransformerConv`, `EdgeConv`, `RGCNConv`, `HGTConv`)
  and justify the choice against graph structure in
  `paper/logs/decision_log.md`.
- The data is heterogeneous (multi-type nodes/edges) and you need
  `HeteroData`, `to_hetero()`, `HeteroConv`, or `HGTConv` recipes.
- A graph is too large for full-batch training and `NeighborLoader` /
  `LinkNeighborLoader` sampling is required.
- A reviewer asks for a GNN explanation (`GNNExplainer`, `PGExplainer`,
  `CaptumExplainer`) to be reported in `paper/reviews/response_to_reviewers.md`.

Do not use this skill for plain NetworkX graph analytics, classical tabular ML
(scikit-learn), end-to-end deep-learning training orchestration (pytorch-lightning),
Bayesian inference (pymc), or non-Python stacks. It is also not an execution
harness: in this repo it documents and recipes GNN analyses; it does not run
production training jobs and ships no executable training/inference scripts.

## Required Inputs

- A graph already logged in `paper/experiments/run_ledger.md` (node features,
  `edge_index` as a `[2, num_edges]` COO tensor, labels) or a user-supplied
  dataset path. Do not invent or fabricate graph data.
- The claim ID(s) this GNN must support, from
  `paper/experiments/evidence_matrix.md`, so each metric can be tied back.
- The metric(s) and protocol mandated by `paper/refs/target_journal.md` and
  `paper/experiments/statistics.md` (e.g. node-classification accuracy with
  fixed train/val/test masks, graph-classification 10-fold CV).
- A target output path for any persisted result under `paper/experiments/` or
  `paper/assets/tables/`.
- Python 3.10+, PyTorch 2.6+, and torch-geometric 2.7.x. Optional accelerated
  wheels (`pyg-lib`, `torch-scatter`, `torch-sparse`, `torch-cluster`) are
  version-matched from the PyG wheel index. The user is responsible for
  installing these; this skill pins no runtime. For reviewer-accepted
  benchmark picks by task (Planetoid/OGB node, TUDataset/OGB graph, OGB link,
  QM9/MoleculeNet molecular, ShapeNet/ModelNet/FAUST point cloud), see
  `references/datasets.md`.
- No API keys or credentials are required by PyG itself. If a dataset download
  (e.g. OGB, private token) needs a credential, the user must provide it; never
  hardcode or store it.

## Workflow

1. Read the target claim and its required metric from
   `paper/experiments/evidence_matrix.md` and `paper/refs/target_journal.md`.
   Do not pick a metric the journal or claim does not sanction.
2. Load only graph data referenced by `paper/experiments/run_ledger.md`; if the
   graph or its masks are absent/unlogged, stop (see Stop With) rather than
   substituting.
3. Verify the `edge_index` contract: shape `[2, num_edges]`, `torch.long`,
   contiguous, and (for undirected graphs) both directions present — fix with
   `.t().contiguous()` or `T.ToUndirected()` before training. Record the check.
4. Choose conv layers from `references/message_passing.md` and the
   `references/layer_selection.md` decision aid (Layer | Best for | Key idea,
   covering `GCNConv` / `GATConv` / `GATv2Conv` / `SAGEConv` / `GINConv` /
   `TransformerConv` / `EdgeConv` / `RGCNConv` / `HGTConv`); document the
   rationale in `paper/logs/decision_log.md`. Apply activations yourself — PyG
   conv layers ship no activation by design.
5. For heterogeneous graphs, build the model with `to_hetero()`, `HeteroConv`,
   or `HGTConv` per `references/heterogeneous.md`; disable `add_self_loops` in
   bipartite layers and use skip connections instead.
6. For large graphs, configure `NeighborLoader` so `len(num_neighbors)` equals
   the number of GNN layers; slice predictions/labels to the first
   `batch.batch_size` seed nodes (see `references/scaling.md`).
7. Train and evaluate using the journal-mandated metrics; for link prediction
   follow `references/link_prediction.md` (`RandomLinkSplit`, GAE/VGAE,
   negative sampling). Fix and record `random_state` / seeds.
8. Persist: append a run row to `paper/experiments/run_ledger.md` (model,
   layer config, sampling config, metric + CI, seeds, data/claim IDs), update
   `paper/experiments/evidence_matrix.md` status (`supported` / `partial` /
   `refuted`), and write any comparison/ablation table to
   `paper/assets/tables/` mirrored into `paper/experiments/ablation.md`.
9. Surface non-trivial decisions in `paper/logs/decision_log.md` and record
   negative results honestly in `paper/experiments/dead_ends.md` instead of
   suppressing them.

## Output Contract

- A run row in `paper/experiments/run_ledger.md` with: model architecture (layer
  types/counts/hidden dims), sampling config (if any), split/CV protocol, point
  metric + CI, seeds, and the data/claim IDs it supports.
- Updated status in `paper/experiments/evidence_matrix.md` for every claim the
  run addresses.
- An ablation/model-comparison table under `paper/assets/tables/` when more
  than one variant was compared; mirror it into
  `paper/experiments/ablation.md`.
- A statistical note in `paper/experiments/statistics.md` when CIs or tests
  were computed.
- A reproducibility note in `paper/experiments/reproducibility.md` covering
  PyTorch / torch-geometric (and any extension wheel) versions, seeds, exact
  data ref, and the split/mask definition.
- Optional decision/dead-end entries in `paper/logs/decision_log.md` and
  `paper/experiments/dead_ends.md`.
- No executable training scripts shipped into the repo (this is a paper repo,
  not an ML runtime); code stays as documented recipes in the references.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only torch-geometric`
- `python src/S03_Scripts/validate_project.py`
- Confirm every GNN run referenced by `paper/experiments/evidence_matrix.md`
  has a matching row in `paper/experiments/run_ledger.md` (no orphan claims).
- Confirm no metric is reported for a claim the matrix marks `unsupported`,
  `missing_evidence`, or `refuted`.
- Confirm `edge_index` is `[2, num_edges]` and (for undirected graphs) contains
  both directions in the cited recipe — grep for the transpose / `ToUndirected`
  step.
- Confirm PyTorch + torch-geometric versions and seeds are recorded in
  `paper/experiments/reproducibility.md`.

## Boundaries

- Do not run general NetworkX analytics, classical ML (defer to scikit-learn),
  training orchestration (defer to pytorch-lightning), or Bayesian inference
  (defer to pymc) here. PyG GNN recipes only.
- Do not fabricate metrics, datasets, masks, or benchmark numbers; if a result
  is missing, mark the claim `missing_evidence` and stop.
- Do not leak test-fold edges into training for link prediction — use
  `RandomLinkSplit` with `add_negative_train_samples=False` and report any
  unavoidable leakage risk before reporting a number.
- Do not persist raw trained weights / `.pt` / `.pth` / `.ckpt` artifacts into
  the paper repo (no model binary blobs); record recipes and metrics, not weights.
- Do not write outputs anywhere except `paper/experiments/`,
  `paper/assets/tables/` (and `paper/assets/figures/` for explanation
  visualizations), and the designated logs; never into `paper/tex/`,
  `paper/refs/`, or `paper/submission/`.
- Do not copy the upstream `scripts/` executable training/inference code into
  this repo; this skill ships `references/` documentation only.

## Stop With

- The graph data needed to compute a claim is not present in
  `paper/experiments/run_ledger.md` and the user has not supplied it.
- The required metric, task level (node/link/graph), or split protocol is
  unspecified by `paper/refs/target_journal.md` /
  `paper/experiments/statistics.md` and the user has not disambiguated.
- A leakage risk is unavoidable (e.g. edges bridging train/test, no fixed
  masks for a transductive claim) — report and pause rather than report a
  biased number.
- torch-geometric or PyTorch is unavailable and the user cannot install the
  matched wheels; do not silently fall back to a different library.
- The result would contradict the claim's required direction and the user has
  not authorized reporting a `refuted` finding — surface it in
  `paper/logs/decision_log.md` and wait.

## References

- Message passing & custom layers: `.agent/skills/torch-geometric/references/message_passing.md`
- Layer selection aid (Layer | Best for | Key idea): `.agent/skills/torch-geometric/references/layer_selection.md`
- Common datasets by task: `.agent/skills/torch-geometric/references/datasets.md`
- Heterogeneous graphs: `.agent/skills/torch-geometric/references/heterogeneous.md`
- Scaling to large graphs: `.agent/skills/torch-geometric/references/scaling.md`
- Link prediction: `.agent/skills/torch-geometric/references/link_prediction.md`
- Custom datasets: `.agent/skills/torch-geometric/references/custom_datasets.md`
- Explainability: `.agent/skills/torch-geometric/references/explainability.md`
- Invocation scenarios: `.agent/skills/torch-geometric/examples/prompts.md`
- Workspace artifacts: `paper/experiments/evidence_matrix.md`,
  `paper/experiments/run_ledger.md`, `paper/experiments/statistics.md`,
  `paper/experiments/ablation.md`, `paper/experiments/reproducibility.md`,
  `paper/experiments/dead_ends.md`, `paper/refs/target_journal.md`,
  `paper/assets/tables/`, `paper/assets/figures/`,
  `paper/logs/decision_log.md`.
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://pytorch-geometric.readthedocs.io/ ,
  https://data.pyg.org/whl/ ,
  https://github.com/pyg-team/pytorch_geometric/releases/tag/2.7.0
