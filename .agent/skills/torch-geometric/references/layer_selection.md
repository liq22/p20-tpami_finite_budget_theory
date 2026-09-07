# Layer Selection Aid

Decision aid for picking a `torch_geometric.nn` conv layer. Use this to defend a
layer choice in `paper/logs/decision_log.md` and reviewer responses. Pick the
row whose "Best for" matches the task and graph structure.

| Layer | Best for | Key idea |
|-------|----------|----------|
| `GCNConv` | Homogeneous, semi-supervised node classification | Spectral-inspired, degree-normalized aggregation |
| `GATConv` / `GATv2Conv` | When neighbor importance varies | Attention-weighted messages |
| `SAGEConv` | Large graphs, inductive settings | Sampling-friendly, learnable aggregation |
| `GINConv` | Graph classification, maximizing expressiveness | As powerful as WL test |
| `TransformerConv` | Rich edge features, complex interactions | Multi-head attention with edge features |
| `EdgeConv` | Point clouds, dynamic graphs | MLP on edge features (x_i, x_j - x_i) |
| `RGCNConv` | Heterogeneous with many relation types | Relation-specific weight matrices |
| `HGTConv` | Heterogeneous graphs | Type-specific attention |

All conv layers accept `(x, edge_index)` at minimum; many also accept
`edge_attr` for edge features. PyG conv layers ship no activation by design —
apply ReLU / dropout yourself between layers.
