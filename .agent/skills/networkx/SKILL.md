---
name: networkx
description: 'Implementation skill for networks/graphs with NetworkX 3.x. Use for graph construction, algorithms (paths, centrality, clustering, communities), generators, and I/O. Do not use for figure planning (scientific-visualization), ML on graph features (scikit-learn), graph deep learning (torch-geometric), or Bayesian models (pymc); not a primary skill.'
---

# networkx

## Purpose

Build, manipulate, analyze, and visualize complex networks and graphs with
NetworkX 3.x (current stable 3.6, requires Python >= 3.11). Capabilities include
the four graph types (`Graph`/`DiGraph`/`MultiGraph`/`MultiDiGraph`), node and
edge attributes, graph algorithms (shortest paths, centrality, PageRank,
clustering, community detection, connectivity, flows, isomorphism), network
generators (classic, random, small-world, scale-free, lattice), and I/O across
edgelist, GraphML, GML, JSON node-link, pandas, NumPy, and SciPy sparse formats.
This is a TIER B implementation-only tool skill: it constructs and analyzes the
graph; it does not plan the figure or the experiment.

## Use When

- A network/graph structure must be built from data in
  `paper/experiments/run_ledger.md` (e.g. a citation, co-authorship,
  biological-interaction, or transportation network) and analyzed for
  `paper/experiments/evidence_matrix.md`.
- Graph-theoretic metrics are required to support a claim — centrality,
  PageRank, clustering coefficient, shortest paths, community structure — and
  must be recorded as evidence.
- A synthetic network (random, scale-free, small-world) is needed for a
  simulation, ablation baseline, or null model logged in
  `paper/experiments/ablation.md`.
- A network topology visualization must be embedded in `paper/draft/`
  (pre-freeze) or `paper/tex/` (post-freeze) and benefits from NetworkX layout
  algorithms.

This is a TIER B tool skill: prefer `scientific-visualization` as the primary
skill for figure planning (panel layout, journal column widths, captions,
restyling) when a network drawing is the deliverable. Plotting tools defer to
scientific-visualization; classical-ML on graph-derived features to
scikit-learn; deep-learning on graphs (GNN message passing, learned embeddings)
to torch-geometric; Bayesian network/graphical-model inference to pymc.
networkx handles only the graph construction and classical-algorithm analysis
those skills may hand off to it; matplotlib remains the escape hatch for fully
custom drawings.

## Required Inputs

- A graph source: either a file already referenced by
  `paper/experiments/run_ledger.md` (edgelist, GraphML, GML, JSON, CSV,
  adjacency matrix) or a pandas DataFrame / NumPy array / SciPy sparse array
  supplied explicitly by the user or planning skill. Do not fabricate nodes,
  edges, or weights.
- The analysis spec from the calling planning skill: which graph type, which
  algorithms (centrality family, path metric, community method), the random
  seed for any stochastic step, and the claim ID from
  `paper/experiments/evidence_matrix.md` the result must support.
- Target-journal constraints from `paper/refs/target_journal.md` (column width,
  font, vector vs raster) and the output paths: figures under
  `paper/assets/figures/`, computed metrics into `paper/experiments/` artifacts.
- NetworkX >= 3.0 (ideally 3.6) with the default extras (numpy, scipy,
  pandas, matplotlib) for full algorithm and I/O coverage; optional backends
  (`nx-cugraph` GPU, `nx-parallel` multicore, `graphblas-algorithms`) for large
  graphs. The user is responsible for installing these; this skill does not pin
  or ship a runtime.
- No API keys or credentials are required. If a wrapped workflow ever needs an
  external credential (e.g. a private dataset token), the user must provide it;
  never hardcode or store it.

## Workflow

1. Read the analysis spec and target claim from the planning skill and
   `paper/experiments/evidence_matrix.md`. Do not invent new science, metrics,
   or network structure.
2. Load only the graph referenced by `paper/experiments/run_ledger.md`; if it is
   absent or unlogged, stop (see Stop With) rather than substituting data.
   Use `references/io.md` to pick the format and the NetworkX 3.6 node-link
   convention (edges stored under the `"edges"` key; older files may use
   `"links"`).
3. Pick the graph type by relationship semantics: `Graph` (undirected, single
   edge), `DiGraph` (directed), `MultiGraph`/`MultiDiGraph` (parallel edges).
   Use `references/graph-basics.md` for creation, attributes, and subgraphs.
4. Run only the algorithms the spec requests; consult
   `references/algorithms.md` for shortest paths, centrality (degree /
   betweenness / closeness / eigenvector / PageRank), clustering, connectivity,
   community detection (`greedy_modularity_communities`), flows, and
   isomorphism. Pass `weight=` explicitly when edges carry weights.
5. For generation/baselines, use `references/generators.md` (Erdos-Renyi,
   Barabasi-Albert, Watts-Strogatz, lattice, trees). Note that `nx.random_tree`
   was removed in 3.4 — use `nx.random_labeled_tree`. Always pass `seed=` for
   reproducibility and record the seed in the run ledger.
6. For large graphs, use appropriate sparse structures and consider a backend
   (`backend="cugraph"` / `nx.config.backend_priority`) — no algorithm code
   changes. Surface memory/approximation choices in
   `paper/logs/decision_log.md`.
7. For visualization, follow `references/visualization.md`: choose a layout
   (`spring_layout`/`kamada_kawai_layout`/`circular_layout`/`spectral_layout`),
   set `seed=` on stochastic layouts, color/size nodes by a metric, and export
   with explicit `dpi` (300 print) and `bbox_inches='tight'`, writing both PDF
   and PNG when vectors are required. Hand figure planning off to
   `scientific-visualization`.
8. Write figures into `paper/assets/figures/` and computed metrics (centrality
   tables, community assignments, path statistics) into
   `paper/experiments/statistics.md` or `paper/experiments/evidence_matrix.md`.
   Append provenance to `paper/experiments/run_ledger.md` (data ref, algorithm,
   seed, claim ID); note post-freeze restyles in `paper/logs/change_log.md`.

## Output Contract

- One or more figure files under `paper/assets/figures/` (PNG/PDF/SVG) for any
  requested topology drawing, named to match the figure ID used in
  `paper/experiments/evidence_matrix.md`.
- Computed graph metrics recorded in `paper/experiments/statistics.md`
  (centrality distributions, clustering, path lengths, community sizes) and/or
  an evidence-status update in `paper/experiments/evidence_matrix.md`.
- A provenance row in `paper/experiments/run_ledger.md` (graph data ref,
  algorithm, seed, backend if any, claim ID), and an optional insight entry in
  `paper/experiments/insights.md` when analysis reveals structure worth
  recording.
- An optional serialized graph under `paper/experiments/` (GraphML/GML) so the
  analysis is reproducible; record the path in the run ledger.
- No executable scripts shipped into the repo; code stays as documented recipes
  in `references/`. This is a paper repo, not a graph-analysis runtime.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only networkx`
- `python src/S03_Scripts/validate_project.py`
- Re-open each exported figure and serialized graph file to confirm it is
  non-empty and the expected format (GraphML is valid XML; GML is parseable).
- Confirm every computed metric is reproducible from the seed and data
  referenced in `paper/experiments/run_ledger.md`.
- Confirm no graph result supports a claim that
  `paper/experiments/evidence_matrix.md` marks `unsupported`,
  `missing_evidence`, or `refuted`.
- Confirm random seeds are set for any stochastic algorithm, generator, or
  layout, and recorded in the run ledger.
- Confirm figure DPI/size and palette match `paper/refs/target_journal.md`
  (column width, colorblind-safety, vector vs raster).

## Boundaries

- Do not decide figure content, panel choice, or captions on its own — that is
  `scientific-visualization`'s job. This skill only renders the topology it is
  asked to draw.
- Do not fabricate nodes, edges, or weights; analyze only the graph present in
  a run referenced by the ledger or supplied explicitly by the user.
- Do not write outputs anywhere except `paper/assets/figures/`,
  `paper/experiments/`, or a clearly named scratch dir; never into
  `paper/tex/`, `paper/refs/`, or `paper/submission/`.
- Do not run heavy ML training/inference or learned graph representations;
  classical-ML on graph features defers to scikit-learn, GNN/deep graph learning
  to torch-geometric, Bayesian graphical models to pymc.
- Do not copy executable training/inference scripts; ship `references/` docs
  only. Do not use rainbow colormaps (`jet`) or unset seeds on stochastic steps.
- Be explicit about floating-point precision: results on graphs with
  floating-point weights are approximate; record this when it affects
  min/max-flow or centrality outcomes.

## Stop With

- The graph data needed for the analysis is not in
  `paper/experiments/run_ledger.md` and the user has not supplied it.
- The analysis spec is missing, ambiguous, or the requested algorithm would
  imply a causal claim from a purely structural/correlational network.
- The graph is too large for in-memory NetworkX and no accelerated backend
  (`nx-cugraph`/`nx-parallel`/`graphblas-algorithms`) is available and the user
  will not authorize an approximate algorithm or sampling.
- NetworkX or a required dependency (numpy/scipy/pandas/matplotlib) is
  unavailable and the user cannot install it; do not silently fall back to a
  different library.
- The result would contradict the claim's required direction and the user has
  not authorized reporting a `refuted` finding — surface it in
  `paper/logs/decision_log.md` and wait.

## References

- Graph basics (types, attributes, subgraphs):
  `.agent/skills/networkx/references/graph-basics.md`
- Algorithms (paths, centrality, clustering, communities, flows, isomorphism):
  `.agent/skills/networkx/references/algorithms.md`
- Generators (classic, random, small-world, scale-free, lattice, trees):
  `.agent/skills/networkx/references/generators.md`
- I/O formats (edgelist, GraphML, GML, JSON node-link, pandas, NumPy, SciPy):
  `.agent/skills/networkx/references/io.md`
- Visualization (layouts, customization, interactive, publication figures):
  `.agent/skills/networkx/references/visualization.md`
- Invocation scenarios: `.agent/skills/networkx/examples/prompts.md`
- Companion skills: `.agent/skills/scientific-visualization/SKILL.md` (figure
  planning), `.agent/skills/matplotlib/SKILL.md` (custom drawing escape hatch),
  `.agent/skills/scikit-learn/SKILL.md` (ML on graph features),
  `.agent/skills/torch-geometric/SKILL.md` (deep graph learning),
  `.agent/skills/pymc/SKILL.md` (Bayesian graphical models).
- Workspace artifacts: `paper/assets/figures/`,
  `paper/experiments/run_ledger.md`, `paper/experiments/evidence_matrix.md`,
  `paper/experiments/statistics.md`, `paper/experiments/insights.md`,
  `paper/refs/target_journal.md`, `paper/logs/decision_log.md`,
  `paper/logs/change_log.md`
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://networkx.org/documentation/latest/ ,
  https://networkx.org/documentation/latest/tutorial.html ,
  https://networkx.org/documentation/latest/auto_examples/index.html
