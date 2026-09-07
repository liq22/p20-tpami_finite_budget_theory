# torch-geometric — Invocation Scenarios

Realistic prompts for using the PyTorch Geometric implementation skill inside
the Auto-01-tiny-research single-paper workflow. Each scenario ties the GNN
recipe to a specific claim in `paper/experiments/evidence_matrix.md` and shows
where the result must be persisted.

## Scenario 1: Node classification on Cora backing a transductive claim

Claim C-04 in `paper/experiments/evidence_matrix.md` requires a 2-layer GCN
accuracy on Cora with the standard public train/val/test masks, reported with a
95% CI.

> I need a PyG recipe for a 2-layer `GCNConv` model on Cora: load
> `Planetoid(root='data', name='Cora')`, build the model with hidden channels
> 16 and dropout 0.5, train full-batch for 200 epochs with cross-entropy on
> `data.train_mask`, and report test accuracy on `data.test_mask`. Verify
> `edge_index` is `[2, num_edges]` and undirected before training. Append the
> run (algorithm, seed, epoch count, test accuracy + CI, Cora data ref) to
> `paper/experiments/run_ledger.md`, update claim C-04 to `supported`, and add
> a reproducibility note with torch + torch-geometric versions to
> `paper/experiments/reproducibility.md`. Do not persist model weights.

## Scenario 2: Graph classification on ENZYMES for an ablation table

The paper compares pooling strategies; `paper/experiments/ablation.md` needs a
graph-classification result on ENZYMES comparing `global_mean_pool` vs
`global_add_pool` under 10-fold CV.

> Give me a `GraphClassifier` using two `GCNConv` layers plus a global pooling
> op, trained with `DataLoader(dataset, batch_size=32, shuffle=True)` on the
> ENZYMES TUDataset. Run 10-fold CV comparing `global_mean_pool` and
> `global_add_pool`, fixed seed. Produce a comparison table for
> `paper/assets/tables/` and mirror it into `paper/experiments/ablation.md`,
> with a statistical note (mean +/- std, paired test if applicable) in
> `paper/experiments/statistics.md`. Document the conv/pool choice rationale in
> `paper/logs/decision_log.md`. Ship only the documented recipe — no
> executable training script.

## Scenario 3: Heterogeneous link prediction on an OGB-style graph

Claim C-11 requires a link-prediction result on a heterogeneous graph (papers,
authors, venues) that is too large for full-batch training.

> Build a heterogeneous GNN with `HeteroData` and `to_hetero()` over a
> `SAGEConv((-1,-1), ...)` backbone. Use `RandomLinkSplit` with
> `add_negative_train_samples=False` to carve train/val/test edges, and train
> with `LinkNeighborLoader` (match `num_neighbors` length to the GNN depth).
> Disable `add_self_loops` on bipartite relations and use skip connections.
> Report Hits@K per `references/link_prediction.md`. Append the run to
> `paper/experiments/run_ledger.md`, record the sampling config and seeds in
> `paper/experiments/reproducibility.md`, and stop if any train/test edge
> leakage cannot be ruled out.
