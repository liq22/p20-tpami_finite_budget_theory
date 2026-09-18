# Adversarial pre-submission review

Date: 2026-09-18  
Target: IEEE TPAMI  
Status vocabulary: `pass`, `needs revision`, `needs new experiment`.

This is an internal revision artifact. It is not manuscript prose and should not
be included in the submission. A condensed copy of the checklist is kept as an
HTML comment near the end of `paper/draft/main.md` so that claim edits cannot
silently bypass it.

## Highest reject risks

| Priority | Reviewer attack | Status | Required resolution |
|---|---|---|---|
| P0 | The proposed shared-coordinate objective (C2) has no independent real-data evidence; the paper's strongest evidence currently supports C1/C3 rather than the main learned method | needs new experiment | Execute the first real falsification protocol before strengthening the Abstract/Introduction; preserve null or reversed results |
| P0 | C1 specializes known quadratic projection/sparse approximation tools and C3 is a simple containment construction; without a nontrivial C2 finding the total contribution may be insufficient for TPAMI | needs new experiment | Demonstrate an independent, practically meaningful finite-budget effect beyond matched objectives and structured support, or reposition the paper around a stronger new scientific finding |
| P0 | Recent time-series explainers were missing from the direct comparison set | needs revision / needs new experiment | Cover ContraLSP, TimeX++, TIMING and other task-compatible recent methods; separate faithful native comparisons from matched-family controls |
| P1 | Response MSE is a custom endpoint and cannot support broad claims of “better explanation quality” | needs revision / needs new experiment | Keep C2 phrased as fixed-response prediction; add compatible localization/native temporal-XAI metrics for broader claims |
| P1 | The result can depend materially on the intervention law | needs new experiment | Prespecify the primary law and one scientifically reasonable alternative; report reversals as boundaries |
| P1 | Dense SO(p) learning is O(p^3) and capped at p<=256 | needs revision / needs new experiment | Report dimensionality/cost; either add a scalable structured parameterization or restrict the practical scope |
| P1 | Group-wise outer optimization may be an unisolated source of gain | needs new experiment | If groups are used, compare mean-risk vs worst-group training; otherwise use a single group |
| P1 | A grid over k,Q,ridge can create hidden researcher degrees of freedom | needs revision | Freeze a primary pair/reference on development data; secondary grid is prespecified; control multiplicity for cell-wise inferential claims |
| P1 | One predictor checkpoint cannot support model-independent claims | needs new experiment | First falsification may use one frozen predictor; final evidence should replicate across seeds or architectures |
| Operational | PR has no workflow runs/statuses despite configured checks | needs revision | Do not merge under the current gate until repository-wide validation actually runs or the gate is deliberately changed by the author |

## 1. Contribution

| Question | Status | Evidence / action |
|---|---|---|
| What new knowledge does the paper give? | needs new experiment | C1 gives a useful decomposition and C3 gives an information-matched containment boundary. The proposed C2 mechanism still lacks real evidence. |
| Is the failure case meaningful rather than trivial? | needs revision | Finite-query confounding is meaningful, but currently demonstrated only by a constructed context-gated example. Add one real case where the distinction changes a conclusion. |
| Is the technical idea non-obvious beyond established practice? | needs new experiment | Infidelity, task-driven dictionaries, transformed explanations, structured sparsity and instancewise selection are established. Novelty must come from the specific fixed-response relationship plus a nontrivial empirical finding. |
| Is the gain surprising or insightful? | needs new experiment | The negative routing result is insightful. No real shared-coordinate gain is established. |
| Is there a clear novelty type? | needs revision | Current viable types are formulation/boundary, controlled falsification, and—only if E4/E5 succeeds—new empirical mechanism. Do not claim “learned transform” or “outer objective” as the novelty. |

## 2. Writing clarity

| Question | Status | Evidence / action |
|---|---|---|
| Can a knowledgeable reader reproduce the method? | pass | Fixed-response arrays, OMP-ridge, shared orthogonal parameterization, train/select/test separation and execution entry are specified. |
| Enough technical detail for key modules? | needs revision | Matched reconstruction- and sparsity-trained objectives are protocol-level descriptions until implemented; add exact equations/optimization only when they become real baselines. |
| Motivation of every module explicit? | pass | Remaining components map to semantic comparability, finite-budget attribution, or information matching. |
| Terms and notation consistent? | pass | Current fixed-response notation is coherent; re-audit after real-data sections are inserted. |
| One clear message per paragraph? | pass | Introduction/Related Work are substantially improved; avoid re-expanding them before evidence changes. |

## 3. Experimental strength

| Question | Status | Evidence / action |
|---|---|---|
| Meaningful improvement over strong baselines? | needs new experiment | None yet for C2. |
| Competitive absolute performance? | needs new experiment | Synthetic response MSE cannot establish practical competitiveness. |
| Consistent across datasets/settings/metrics? | needs new experiment | Current controlled example is one constructed family. |
| Strengths and failure cases reported? | pass for current evidence | The route/union negative control and shuffled-context degradation are retained. Apply the same discipline to real data. |

## 4. Evaluation completeness

| Question | Status | Evidence / action |
|---|---|---|
| Ablations for all key design choices? | needs new experiment | Objective, k, Q, ridge, group objective, support search, coordinate parameterization and intervention law remain. |
| Strong/recent baselines included fairly? | needs revision / needs new experiment | TRIM/AWD/task-driven dictionary are not sufficient for a time-series paper. Add ContraLSP, TimeX++, TIMING when compatible and preserve native objectives. |
| Metrics standard and sufficient? | needs revision / needs new experiment | Response MSE is sufficient only for the fixed-response estimand. Broader XAI claims require compatible localization/faithfulness/native metrics. |
| Datasets/scenarios challenging enough? | needs new experiment | No independent real dataset is currently executed. |
| Protocol documented? | pass | `REAL_FALSIFICATION_PROTOCOL.md` now defines independent units, matched response tables, primary paired estimand, comparator tiers and stop rules. |

## 5. Method design soundness

| Question | Status | Evidence / action |
|---|---|---|
| Is the setting realistic? | needs new experiment | Validate scalar-query access and intervention law on real units. |
| Hidden defects or unreasonable assumptions? | needs revision | State dense p<=256 boundary, fixed gate before scoring displacement, declared descriptors/groups, and conditional nature of the response target. |
| Robust without per-scenario tuning? | needs new experiment | Freeze development-only tuning and report sensitivity across the prespecified budget grid and seeds. |
| Benefits exceed added complexity? | needs new experiment | Report offline basis training, online query count, runtime and memory against fixed transforms and matched objectives. |
| Could net benefit be negative? | needs new experiment | This is plausible. Identity, best fixed basis, matched objectives and structured support are mandatory; preserve null/reversed outcomes. |

## Decision rule before submission

Do not treat this draft as submission-ready while any P0 item remains. In
particular, prose changes cannot resolve the absence of real C2 evidence. The next
scientifically informative action is one independent-unit real falsification
experiment, not another theory expansion or broader benchmark sweep.
