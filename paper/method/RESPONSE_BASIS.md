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
loss. Neither makes a discriminating reconstruction baseline. Actual inputs can
also be spherical, as in the synthetic diagnostic; using actual x does not by
itself guarantee that the reconstruction objective has a population preference.

The coefficient proxy uses full ridge coefficients, not an already k-sparse
vector. Its denominator is ||beta_hat||^2; zero beta_hat gives zero loss by
definition. It obtains no additional predictor queries or gradients.

These controls are matched-family objective interventions, not faithful
reproductions of TRIM, AWD, or task-driven dictionary learning. All methods have
the same available inputs/responses, but intentionally use different training
losses. All candidates are selected by response loss.

## Executable matched study

The existing response-only mode is retained. Add `--matched-objectives` to execute
all three training objectives, common response-based selection and paired test
scoring. The minimal mean-objective diagnostic is:

```bash
python src/S03_Scripts/run_response_basis.py \
  --synthetic --matched-objectives --aggregation mean \
  --steps 80 --output results/matched_synthetic
```

For supplied fixed-response data:

```bash
python src/S03_Scripts/run_response_basis.py \
  --input DATA.npz --matched-objectives --aggregation mean \
  --k 1 --steps 80 --ridge 1e-4 --learning-rate 0.04 \
  --output results/matched_real
```

The second command consumes data; it does not download a dataset, train a
predictor, or establish that the supplied data are real. `DATA.npz` contains the
existing train/select/test-prefixed response arrays described below, plus
`train_x [N_train,p]` in exactly `train_unit_ids` order. Missing actual inputs fail;
there is no perturbation or synthetic substitute. The current study fixes the
same construction Q and feature coordinates across all three splits.

The response, reconstruction and coefficient objectives have the same
initialization, optimizer steps, checkpoint schedule and aggregation. Candidate
families are frozen before selection. The primary reference is the better
response-selected proxy on development-selection units, fixed before test loss
is computed. Identity, DCT and best selected fixed basis remain separate controls.
The mean step budget is not a claim of equal wall time or FLOPs across objectives.

`aggregation='mean'` averages unit losses. `worst_group` maximizes predefined
group-mean excess over each objective's identity loss. Use the same aggregation
for every objective and selection family. One group reduces both choices to the
same mean criterion. Multi-group excess is not worst absolute risk. Existing
library calls retain `objective='response'` and `aggregation='worst_group'`.

Outputs are `responses.csv` (one row per unit and method), `basis.npz` (selected
bases), and `summary.json` (candidate selection, shared query counts, test MSE and
the primary paired interval). The interval uses 2,000 paired unit resamples and
is conditional on the frozen development result and predictor. It does not
include between-training-seed uncertainty. A stratified target requires a
corresponding prespecified analysis rather than silently reusing pooled inference.

## Independence and output semantics

Construct disjoint train, selection and final-test `ResponseBatch` objects.
Each reference row is one independent unit with fit/scoring arrays:
`fit_v [N,Q,p]`, `fit_d [N,Q]`, `score_v [N,R,p]`, `score_d [N,R]`,
`groups [N]`, and unique `unit_ids [N]`.

For a first real experiment, use one observation per unit selected by a frozen
rule. A multiple-window extension must first average within each unit, then
compute uncertainty over units; relabeling windows as independent rows is not
permitted. The shape checks do not establish biological or mechanical
independence of supplied IDs.

Construction and scoring perturbations must be sampled independently conditional
on x. Independent draws from a discrete law may have equal numerical values;
those coincidences are not leakage. The loader neither rejects nor resamples
matches, because doing so would condition the scoring law on the fit table.
Conversely, value inequality cannot certify independent sampling. The data
producer remains responsible for separate draws, not copied construction tables.

Outer training responses train A. Selection responses choose among a finite
family frozen before selection inspection. Test scoring responses never choose
A, k, Q, lambda or the reference. Including identity does not certify population
no-harm for unbounded raw squared loss.

The best fixed single basis is selected from identity, DCT, and eight seed-fixed
random orthogonal bases. The exact union emulator is an equality control for a
routed decoder, not a comparator expected to be beaten. Structured-support and
native-method comparisons are separate from the matched-objective CLI.

## Direct validation and remaining evidence

```bash
python -m unittest discover -s src/S04_Tests -p 'test_response_basis.py' -v
python -m unittest discover -s src/S04_Tests -p 'test_response_objectives.py' -v
python -m unittest discover -s src/S04_Tests -p 'test_response_runner.py' -v
```

The tests protect reconstruction and coefficient semantics, branch gradients,
common selection, discrete-draw coincidences, the three-objective entry, and
invariance of selected bases/reference to changed final-test responses. They are
not real-data validation or a replacement for the full repository checks.
The executed synthetic diagnostic and its inconclusive paired objective contrast
are recorded in `paper/experiments/SCIENTIFIC_CHAIN.md` and manuscript Section 5.2.
Execute `paper/experiments/REAL_FALSIFICATION_PROTOCOL.md` next on real units.
