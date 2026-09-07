# networkx — invocation scenarios

Realistic prompts for invoking the networkx tool skill inside the
Auto-01-tiny-research workspace. Each scenario shows the kind of request that
should trigger this skill and the workspace artifacts it produces or reads.

## Scenario 1: Centrality and community analysis of a citation network

> I have a co-citation network stored as `paper/experiments/cocite.edgelist`
> (referenced in `paper/experiments/run_ledger.md`). For the claim in
> `paper/experiments/evidence_matrix.md` that "the field's core is dominated by
> a small set of hub papers," compute degree, betweenness, and eigenvector
> centrality, run greedy modularity community detection, and report the
> top-10 hubs plus the community size distribution into
> `paper/experiments/statistics.md`. Set `seed=42` everywhere stochastic and
> append provenance to the run ledger.

This triggers networkx because the request is graph construction plus classical
graph algorithms on a real network. The skill loads the edgelist with
`nx.read_edgelist`, builds an undirected `Graph`, runs
`nx.degree_centrality`/`nx.betweenness_centrality`/`nx.eigenvector_centrality`
and `community.greedy_modularity_communities`, records the seed and algorithm
choices in `paper/experiments/run_ledger.md`, and writes the ranked hubs and
community-size table into `paper/experiments/statistics.md` linked from the
claim in `paper/experiments/evidence_matrix.md`. Do NOT train a GNN or compute
learned embeddings here — that is torch-geometric's job; do NOT plan the
topology figure here — defer the drawing to scientific-visualization.

## Scenario 2: Null-model comparison with synthetic scale-free networks

> To support the ablation in `paper/experiments/ablation.md`, generate 50
> Barabasi-Albert scale-free graphs and 50 Erdos-Renyi random graphs matched
> to the empirical network's node and edge counts (n=500, m from the real
> graph). For each, compute average clustering coefficient and characteristic
> path length, then report the mean/std and whether the empirical graph's
> values fall outside the null distribution. Save the comparison table to
> `paper/experiments/statistics.md` and log seeds in the run ledger.

This triggers networkx because the task is synthetic network generation plus
classical structural statistics for a null-model comparison. The skill uses
`nx.barabasi_albert_graph` and `nx.erdos_renyi_graph` with explicit per-graph
seeds, `nx.average_clustering` and `nx.average_shortest_path_length` (on the
largest connected component), records all seeds and the matching procedure in
`paper/experiments/run_ledger.md`, and writes the comparison table into
`paper/experiments/statistics.md` for `paper/experiments/ablation.md`. If the
graph is too large for exact path lengths, surface the approximation choice in
`paper/logs/decision_log.md` rather than silently using an estimate.

## Scenario 3: Topology figure for the methods section

> Draw the regulatory network from `paper/experiments/regulatory.graphml` for
> the methods figure: nodes colored by community (from the earlier
> `greedy_modularity_communities` run), node size proportional to betweenness
> centrality, a spring layout, and export to both PDF and PNG at 300 dpi into
> `paper/assets/figures/regulatory_network.{pdf,png}`. It must fit a
> single-column width per `paper/refs/target_journal.md`.

This triggers networkx for the layout and metric-driven drawing, but the
figure plan (panel, column width, caption, restyle) belongs to
scientific-visualization. The skill loads the GraphML, recomputes the community
and centrality values (or reads them from the run ledger), builds a
`spring_layout(pos, seed=42)`, maps node color/size to the metrics, and exports
dual PDF/PNG at 300 dpi with `bbox_inches='tight'` into
`paper/assets/figures/`. The export is logged in the run ledger; if restyled
after the tex freeze, the change is noted in `paper/logs/change_log.md`. For
fully custom annotations or a non-standard projection, drop to matplotlib.
