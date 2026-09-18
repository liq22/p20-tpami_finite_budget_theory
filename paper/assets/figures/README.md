# Figures for the problem and method

The source is `experiments/p19/plot_motivation.py`. Run it from the repository
root to regenerate both SVGs; `bash scripts/build_paper.sh build/p20` renders
vector PDFs, PNG previews and the reading manuscript. SVG text, rectangles,
polylines and arrowheads are individually editable. Neither figure embeds a
raster image or encodes an invented numerical result.

## Figure 1 — Fixed-response comparison

File: `motivation.svg`. Section: 2.3.

Purpose: distinguish fixed predictor/target/law/information/budgets from the
coordinate-learning intervention and the measured response loss. The figure
replaces the earlier routing-focused motivation panel rather than adding another
redundant diagram. The earlier numerical containment result remains in Section 5.

Elements: raw x and v -> d_x(v); construction T_Q; separate scoring responses;
method intervention m; fitted A, support S and coefficients a; L_u and Delta.
These map to manuscript equations (1)–(6). The lower gap panel explains why a
loss comparison alone does not isolate approximation from fitting effects.

Caption: the manuscript supplies the full caption. Its conclusion is the need
for controlled comparison, not an observed coordinate-learning gain.

## Figure 2 — Shared-coordinate method

File: `method_overview.svg`. Section: 3.1.

Purpose: make the learned object and information boundaries visible.
The three stages are development training, independent selection, and frozen
new-input evaluation. Thin outlines mark inherited operations; the heavy outline
marks the response-specific outer loss. Dashed feedback updates only the shared
basis. Fresh development outer responses feed the outer loss directly; they do
not enter the construction decoder. Test scoring has no return edge.

Elements: A_theta (8); greedy support and ridge (9)–(10); outer response loss
(11); matched proxy replacements (Section 3.3); common selection (12); and
independent-unit measurement (6). These correspond to Algorithm 1 steps 1–5.
The union comparator appears only in the footer because it is an external
control, not an extra trainable module.

Caption: the manuscript supplies the full caption, distinguishing proposed
learning intervention from reused components and unresolved real-data evidence.

## Rendering and scope

Both diagrams use a 180-mm canvas and readable vector text. Scientific purpose,
restrained hierarchy and rendered inspection follow the supplied nature-figure
reference; no figure-management framework is copied into this repository.
Inspect both the standalone SVG and the compiled manuscript at reading size.
The main manuscript, not this README, contains all mathematical definitions.
