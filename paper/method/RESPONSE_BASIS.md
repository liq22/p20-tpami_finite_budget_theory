# Shared orthogonal response-basis model

## Model, not a new diagnostic predictor

The learned component is a single coordinate matrix A shared across inputs of a
fixed predictor. It does not train, clone or replace the predictor. With
z=Ax and inverse A^T, s(A^Tz)=s(x). Responses are collected at original x-v,
never at independently masked transformed coordinates.

`SharedOrthogonalBasis` stores p(p-1)/2 parameters in a skew-symmetric matrix S:

$$A=\exp(S),\quad S=-S^T,\quad A^TA=I.$$

This dense reference is limited to p<=256. Matrix exponential costs O(p³).
A block/structured implementation for long sequences and images is future work,
not an automatic dimensionality reduction. The component learns SO(p); row sign
changes do not change the sparse prediction class, so the missing reflection
component is not a restriction on that class.

## Inner decoder

For each input, collect Q fitting perturbations and scalar differences from one
fixed target. Z_fit=V_fit A^T. Greedy normalized-correlation support selection
with residual refitting chooses at most k coordinates S. On those coordinates:

$$\hat a_S=(Z_S^TZ_S/Q+\lambda I)^{-1}Z_S^Td/Q.$$

Lambda is positive and explicit. The method is OMP support selection followed by
ridge fitting, not the population cardinality oracle. It returns sensitivity
coefficients for response prediction, not native Integrated Gradients scores.
A singular Gram matrix is not repaired by replacing the task or explanation.

## Outer objective

For fresh perturbations of each development-training input, compute

$$\ell_u(A)=\operatorname{mean}_{v\in score(u)}
[(\hat a_u^TAv-d_u(v))^2].$$

The primary matched-objective study optimizes the mean excess

$
\min_\theta
\operatorname{mean}_u
[\ell_u(A_\theta)-\ell_u(I)].
$

A predefined worst-group aggregation,

$
\min_\theta\max_h\operatorname{mean}_{u\in h}
[\ell_u(A_\theta)-\ell_u(I)],
$

is an optional robustness ablation. It must be applied identically to every
matched coordinate objective and is not part of the claimed response-objective
gain.

These score queries are development-training data because they optimize A; they
are not confirmation evidence. Differentiation passes through the matrix
exponential and restricted ridge solve on the currently selected support.
Support argmax is discrete, so this is piecewise-smooth nonconvex optimization.
No global minimizer or support-recovery theorem is claimed.

The optimizer never receives predictor parameters or calls the predictor after
response collection. One finite checkpoint trajectory, including identity, is
selected on separate development-selection units. Final evaluation units are
unseen by both optimization and selection.

## User interface

Run `bash scripts/run_response_basis.sh test` before training. Then use `demo`
for a labelled synthetic diagnostic or `study --input DATA.npz --output DIR`
for supplied scalar response data. The runner defaults to
`--aggregation mean`; `--aggregation worst_group` is an explicit robustness
ablation and is used for both training and candidate selection. All data remain
local. Output directories are never overwritten. Test data affect reported
metrics only, not the selected basis. A required method or invalid scientific
input fails explicitly.

The NPZ holds train/select/test prefixes, each with:
`fit_v [N,Q,p]`, `fit_d [N,Q]`, `score_v [N,R,p]`, `score_d [N,R]`,
`groups [N]` integer labels and `unit_ids [N]` Unicode strings. Each row is one
independent unit in this reference format. Repeated windows of one bearing or
patient must first be aggregated into a unit-preserving study; do not relabel
windows as independent IDs. No targets or pretrained models are inferred from
filenames. Data producers own the explicit fixed-target contract.

## Comparison boundary

Identity, DCT and random orthogonal bases use identical fit/scoring arrays and
the identical decoder. Basis-training and selection costs are amortized but not
free. A scalar-query lower bound with no previous information does not apply to
a new explanation whose basis already encodes development responses from the
same fixed model. A dense rotated coordinate is a response feature; physical
interpretability remains a separate requirement.

## Routing is a diagnostic, not the primary learned component

`experiments/p19/comparators.py` compares frozen candidate bases and their union.
Its context-matched union uses the same rule and transcript as the group route,
with zero coefficients outside the selected block. This establishes finite-query
emulation, not a new optimized union baseline. Plain union-OMP is only one
support-search algorithm. A lower error against that algorithm cannot establish
an intrinsic routing advantage. See `paper/theory/04_COMPARATOR_GEOMETRY_AND_ROUTING.md`.

The remaining method test uses the non-degenerate controls in
\`paper/theory/05_MATCHED_OBJECTIVE_CONTROLS.md\`: best-$k$ sparse
reconstruction and best-$k$ attribution-tail concentration. Full reconstruction
and L2 attribution magnitude are invalid controls for this orthogonal family
because they are rotation invariant. The response, reconstruction and
attribution objectives must use the same unit split, coordinate family, $k$,
candidate-selection rule and aggregation. Structured-support controls are
evaluated separately with the same response table. No real-data or
state-of-the-art superiority is presently established.
