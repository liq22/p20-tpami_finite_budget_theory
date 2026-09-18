# Shared-coordinate response model

## Source and scientific scope

`paper/draft/main.md`, Sections 2–3, defines the problem and Algorithm 1.
`src/S01_Package/response_basis.py` implements the shared basis, decoder,
three outer objectives, and independent candidate selection. The predictor is
fixed; no PHMFactory code or dependency pointer changes.

The shared matrix is A=exp(S), S=-S^T, with p(p-1)/2 parameters and p<=256.
Its dense matrix exponential is cubic in p. Responses are collected at x-v in
original coordinates. An inverse reconstruction through A does not define a new
predictor or establish physical interpretability.

## Decoder and differentiation

For Z=V A^T, greedily maximize squared residual correlation divided by column
squared norm. Refit ridge coefficients after each selected atom:

$$
\hat a_S=(Z_S^T Z_S/Q+\lambda I)^{-1}Z_S^T d/Q,\qquad \lambda>0.
$$

Stop at k atoms, zero residual, or no eligible column. The same numerical
column-eligibility and tie rules apply to every basis. This is normalized greedy
support search with restricted ridge refitting. Its residual is not the
orthogonal residual of unregularized OMP, and its support is not the population
cardinality oracle.

Autograd differentiates the matrix exponential and restricted solve on the
current discrete support branch. It does not differentiate the argmax or prove
a population-gradient formula across support discontinuities.

## Three matched outer objectives

| `objective` | Training quantity | Information used |
|---|---|---|
| `response` | Fresh squared response error of the Q-query sparse decoder | Construction and separate development outer responses |
| `reconstruction` | Squared k-term reconstruction tail of actual input x | Actual development inputs in batch unit order |
| `coefficient_sparsity` | Normalized k-term tail of A beta_hat | Full raw-space ridge beta_hat from the same Q construction responses |

Reconstruction requires `inputs=[N,p]` explicitly. It never silently substitutes
perturbations for real inputs. Full orthogonal reconstruction is zero for every
A; truncation of a spherically symmetric perturbation has an invariant population
loss. Neither makes a discriminating reconstruction baseline.

The coefficient proxy uses full ridge coefficients, not an already k-sparse
vector. Its denominator is ||beta_hat||^2; zero beta_hat gives zero loss by
definition. It obtains no additional predictor queries or gradients.

These controls are matched-family objective interventions, not faithful
reproductions of TRIM, AWD, or task-driven dictionary learning. All methods have
the same available inputs/responses, but intentionally use different training
losses. All candidates are selected by response loss.

## Library entry and unchanged default

Existing calls to `train_basis(...)` retain `objective='response'` and
`aggregation='worst_group'`. New explicit values are:

```python
candidates, history = train_basis(
    train, k=k, ridge=ridge, steps=steps, learning_rate=learning_rate,
    checkpoint_every=checkpoint_every,
    objective="reconstruction", inputs=train_x, aggregation="mean",
)
A, selected_index, selection_losses = select_basis(
    candidates, selection, k=k, ridge=ridge, aggregation="mean",
)
```

`train_x` must contain the actual fixed-preprocessing input for each training
unit in exactly the same order as `train.unit_ids`. The shared three-objective
study calls the same functions with the three declared objective names. The
existing command-line runner remains a response-only study; it does not yet
load input vectors or execute the complete three-objective real-data protocol.

`aggregation='mean'` averages unit losses. `worst_group` maximizes predefined
group-mean excess over each objective's identity loss. Use the same aggregation
for every objective and selection family. One group reduces both choices to the
same mean criterion. Multi-group excess is not worst absolute risk.

## Independence and output semantics

Construct disjoint train, selection and final-test `ResponseBatch` objects.
Each existing reference row is one independent unit with fit/scoring arrays:
`fit_v [N,Q,p]`, `fit_d [N,Q]`, `score_v [N,R,p]`, `score_d [N,R]`,
`groups [N]`, and unique `unit_ids [N]`.

For a first real experiment, use one observation per unit selected by a frozen
rule. A multiple-window extension must first average within each unit, then
compute uncertainty over units; relabeling windows as independent rows is not
permitted. The current shape checks do not establish biological or mechanical
independence of supplied IDs.

Outer training responses train A. Selection responses choose among a finite
family frozen before selection inspection. Test scoring responses never choose
A, k, Q, lambda or the reference. Including identity does not certify population
no-harm for unbounded raw squared loss.

The best fixed single basis in the existing runner is selected from identity,
DCT, and eight seed-fixed random orthogonal bases. The exact union emulator is
an equality control for a routed decoder, not a comparator expected to be beaten.

## Direct validation and remaining evidence

```bash
python -m unittest discover -s src/S04_Tests -p 'test_response_basis.py' -v
python -m unittest discover -s src/S04_Tests -p 'test_response_objectives.py' -v
```

The added tests cover actual-input reconstruction, its spherical degeneracy,
full-Q coefficient estimation, proxy non-vacuity, branch gradients, common
candidate selection, and explicit aggregation. They validate method semantics;
they are not evidence of a real-data C2 advantage. Execute
`paper/experiments/REAL_FALSIFICATION_PROTOCOL.md` next.
