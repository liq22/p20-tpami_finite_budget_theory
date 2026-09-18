---
title: "When Coordinates Help: Finite-Budget Response Explanations"
author: []
lang: en-US
---

# Abstract

A change of coordinates can make an explanation compact without changing the function being explained. Whether this improves prediction of that function's responses depends on the coordinate budget, model-query budget, and information available to the estimator. We study sparse linear decoders of a fixed predictor's responses to a common original-space intervention law. A quadratic projection characterization separates an invariant full-class residual from coordinate approximation, support-search, and coefficient-estimation errors. It also exposes a comparison boundary: a fixed union dictionary contains every single-basis sparse decoder, and a union estimator with the same information can reproduce any routed decoder at any finite query budget. Consequently, a routed implementation outperforming an unconstrained union solver does not establish an intrinsic advantage of routing. This analysis motivates learning a shared orthogonal basis through the held-out response error of the actual finite-query decoder, together with information-matched controls. In a controlled nonlinear example, routing reduces mean response error relative to plain union-OMP at three fitting queries, but an information-matched union estimator reproduces its predictions exactly. The result identifies support restriction as a sufficient explanation of that comparison and establishes the controls needed to evaluate coordinate learning on independent time-series tasks.

# 1. Introduction

Predictive models are often inspected through explanations that retain only a small number of features, time intervals, or transformed coordinates. The practical aim is not merely to produce a short description, but to retain the aspects of model behavior that matter for a specified question. Local surrogates, additive attributions, and response-based fidelity measures provide distinct operational answers to this aim [@ribeiro2016lime; @lundberg2017shap; @yeh2019]. For time series, the distinction is particularly important: relevance may be localized in time, distributed across channels, or expressed through temporal structure that a pointwise representation obscures [@ismail2020; @crabbe2021dynamask]. A compact representation is useful only insofar as it preserves the declared explanatory target.

The target and the experiment used to assess it must therefore be distinguished from the coordinates in which an explanation is written. Removal-based methods differ in what is removed, how absent features are represented, and which aspect of model behavior is summarized [@covert2021removal]. Marginal and conditional feature interventions can answer different dependence questions [@janzing2020; @frye2021]. Perturbation choices also affect measured performance in neural time-series classifiers [@simic2025]. Thus, a lower explanation error obtained after changing both the representation and the intervention law cannot by itself identify a benefit of representation.

Existing methods already provide substantial control over explanatory coordinates. TRIM interprets a model through transformed inputs and explicitly accommodates parameterized transformations [@singh2020trim]. Adaptive Wavelet Distillation learns a wavelet representation using reconstruction, wavelet constraints, and interpretation sparsity while retaining a trained neural model [@ha2021awd]. More generally, task-driven dictionary learning optimizes representations for a downstream objective rather than reconstruction alone [@mairal2012task]. The relevant question is which objective and estimator make those coordinates useful at a specified budget.

A remaining question concerns the source of a measured benefit under finite budgets. Even when the predictor, target, and intervention law are fixed, changing coordinates changes both the best sparse approximation and the estimation problem presented to a finite-query decoder. Local-explanation theory already demonstrates dependence on sampling and neighborhood choices [@garreau2020; @tan2023glime], while adaptive neighborhood sampling addresses query-efficient local fitting [@dhurandhar2022ans]. Structured sparse recovery further shows that restricting admissible supports can improve recovery under appropriate measurement assumptions [@baraniuk2010]. The scientific issue is therefore not whether such restrictions can help, but whether a particular coordinate comparison isolates approximation gains from information, search, and estimation effects.

This distinction becomes decisive when comparing a shared representation with dynamic routing. A fixed union of candidate dictionaries contains every sparse decoder restricted to one candidate. It can also implement the same block restriction as a router when supplied with the same descriptor and query transcript. Figure 1 makes this distinction explicit: a fixed dictionary is not a fixed coefficient vector, and a dynamic gate does not necessarily create a new prediction class. A comparison against plain union-OMP changes the search procedure as well as the representation presented to that procedure. To attribute an observed advantage to routing, one must first rule out an information-matched support-selection explanation.

![**Motivation for information-matched coordinate comparisons.** The predictor, target, intervention law, budgets, development information, and available descriptor are held fixed. A routed decoder selects one block from the candidate family; a fixed union dictionary can represent exactly the same prediction by zero-padding that block's coefficients. Plain union-OMP searches a larger support set and is a different estimator. The observable comparison must therefore distinguish a coordinate approximation benefit from a search or information effect. The final equality is a mathematical identity, not an expected empirical curve.](../assets/figures/motivation.svg){width=100%}

Three challenges follow. **First, semantic comparability:** the same explanation loss must evaluate every coordinate system without changing the underlying model responses. **Second, finite-budget attribution:** the analysis must separate sparse approximation from the support and coefficient errors of an actual estimator. **Third, information-matched selection:** learned coordinates and routers must be assessed with their development information, descriptors, and construction costs exposed, while selection and final scoring remain independent. Prior work supplies important components of this reasoning. FastSHAP separates amortization from value-function choices, and REAL-X uses an optimization-matched baseline and independent evaluation to address encoding and control-flow failures [@jethani2022fastshap; @jethani2021realx]. These results motivate comparing coordinate mechanisms with the same explanatory target and information.

We address these challenges with a fixed-response formulation. For a frozen scalar target score $s$, the response to displacement $v$ is $d_x(v)=s(x)-s(x-v)$. The explanatory object is a $k$-sparse linear decoder fitted from $Q$ scalar responses and evaluated on fresh displacements from the same law. An exact decomposition identifies the terms that coordinates can change. The resulting minimal learning mechanism is a shared orthogonal basis trained through the fresh-within-training error of the finite-query decoder. It is paired with single-basis, fixed-union, and information-matched routed comparisons. Routing is an experimental contrast, not a presumed requirement of the method.

The contributions are threefold. **(1)** We formulate budgeted coordinate comparisons for a fixed response and derive a decomposition and comparator boundary that distinguish coordinate approximation from estimation and information effects. **(2)** We instantiate a shared-coordinate learning mechanism whose objective is the response error of the fitted sparse decoder, rather than an attribution-sparsity proxy, with independent finite-candidate selection. **(3)** We construct an information-matched control showing that a finite-query routing advantage over plain union-OMP can disappear under exact union emulation. The empirical finding is confined to a controlled nonlinear example; the corresponding real-data claim is whether shared-coordinate learning improves independently evaluated response prediction against matched transform-learning and structured-support baselines.

# 2. Related Work

## 2.1 Explanatory targets, interventions, and nonlinear structure

LIME fits local interpretable surrogates, whereas SHAP characterizes additive feature attribution through a coalition value function [@ribeiro2016lime; @lundberg2017shap]. Integrated Gradients uses path-integrated derivatives, and DeepLIFT propagates activation differences relative to a reference [@sundararajan2017ig; @shrikumar2017]. These methods provide different objects and different forms of model access. Their output vectors are not interchangeable coefficients for predicting arbitrary displacements. In particular, a vector derivative is not one scalar forward query, and a path attribution depends on its reference and integration rule.

Infidelity directly measures the squared discrepancy between an attribution's predicted response and an actual model-output difference [@yeh2019]. Its quadratic optimization already supplies the unrestricted least-squares solution and discusses ill-conditioned moment matrices. Cardinality constraints and fitted supports specialize that geometry to separate sources of excess response risk. The removal-based framework of Covert et al. clarifies why retaining the same scalar loss is insufficient if the removal operator or value function changes [@covert2021removal]. Janzing et al. distinguish causal intervention from conditioning, whereas Frye et al. construct on-manifold value functions [@janzing2020; @frye2021]. These alternatives motivate an explicit estimand, not a universally preferred perturbation distribution.

Nonlinear explanation classes offer another route to lower residual error. Integrated Hessians attributes pairwise interactions through path-integrated second derivatives, Faith-Shap uses faithful higher-order approximations, and InstaSHAP connects Shapley explanations with purified additive models [@janizek2021; @tsai2023faith; @enouen2025instashap]. Their interaction structure changes what an explanation can represent. An invertible linear coordinate change instead preserves the unrestricted linear decoder class. Accordingly, a nonzero full-budget residual in our formulation diagnoses that class's limitation; it does not imply that nonlinear explanations cannot improve it.

## 2.2 Coordinates, dictionaries, and structured supports

Classical best-basis selection chooses among orthogonal representations according to a specified objective [@coifman1992]. Online dictionary learning supplies scalable reconstruction-based sparse coding, and task-driven dictionary learning differentiates downstream objectives through sparse codes [@mairal2010online; @mairal2012task]. The relevant distinction for response explanations is the learning target: reconstruction quality, attribution sparsity, and independently scored response error need not select the same basis.

TRIM makes transformed-domain interpretation explicit, including trainable transformations; Adaptive Wavelet Distillation learns wavelets jointly constrained by reconstruction and neural interpretations [@singh2020trim; @ha2021awd]. These are the closest general representation-level predecessors. In machine condition monitoring, transformed explanations are already a direct line of work: Herwig and Borghesani keep the diagnostic network in the time domain while evaluating SHAP in frequency or time--frequency coordinates; CS-SHAP extends SHAP to cyclic-spectral coordinates; and SHEP targets the computational burden of transformed-domain Shapley attribution [@herwig2023raw; @chen2026csshap; @chen2026shep]. Therefore neither transformed-domain PHM explanation nor reducing its attribution cost is the claimed gap. The present comparison retains the central capability of changing explanatory coordinates while preserving a predictor and asks whether direct finite-query response training contributes beyond a matched reconstruction- or sparsity-driven objective. This requires both a faithful original-method comparison and an objective-matched coordinate-family comparison. The two comparisons answer different questions: original-method performance and the effect of the training objective within a controlled coordinate family.

Support restrictions are equally important competitors. Model-based compressive sensing replaces arbitrary sparse supports with structured families and derives recovery benefits under corresponding measurement conditions [@baraniuk2010]. A routed block is one such restriction, although the correlated union dictionaries and nonlinear response residuals considered here do not automatically satisfy compressed-sensing assumptions. The appropriate implication is to compare structured and unstructured support search with the same information, not to transfer a recovery theorem without its hypotheses.

## 2.3 Query efficiency, amortization, and instancewise selection

Garreau and von Luxburg characterize how LIME explanations depend on local sampling choices; GLIME analyzes stability, convergence, and locality [@garreau2020; @tan2023glime]. GLIME also illustrates that a sampling reparameterization may preserve the target objective: changing a sampling implementation is not always changing the estimand. Adaptive neighborhood sampling addresses the conditioning and nonlinear-approximation difficulties of query-efficient local explanation [@dhurandhar2022ans]. Improving KernelSHAP develops regression estimators, uncertainty estimates, and sampling improvements for a fixed Shapley target [@covert2021kernel]. GEEX further shows that gradient-like explanations can be constructed with query-level black-box access [@cai2024geex]. These results establish query-efficient estimation and query-only attribution as prior work, while leaving the coordinate-versus-support contrast to be specified for the response problem studied here.

FastSHAP amortizes a weighted regression objective and explicitly separates benefits of amortization from those of the value-function implementation [@jethani2022fastshap]. Its setup highlights why an offline-trained explanation mechanism cannot be compared to a cold-start estimator by counting online calls alone. Similarly, L2X learns instancewise feature subsets through an information-theoretic objective, while REAL-X addresses prediction encoding and omitted control-flow features in learned selections [@chen2018l2x; @jethani2021realx]. Sparse mixture-of-experts models establish trainable per-example routing for conditional computation [@shazeer2017]. The narrower question is whether a routed response decoder differs from a same-information estimator using a fixed union dictionary, and which imposed computational restriction would make that difference consequential.

## 2.4 Temporal explanations and evaluation validity

Time-series explanation methods address structure beyond an unordered feature set. Temporal Saliency Rescaling separates temporal and feature importance, DynaMask optimizes sparse masks using temporally informed perturbations, and xCEBRA couples contrastive representation learning with regularized attribution maps [@ismail2020; @crabbe2021dynamask; @schneider2025xcebra]. ORTE frames temporal explanations through information retention and learned binary masks [@yue2025orte]. TIMING additionally shows that evaluation metrics can miss opposing directional effects and that temporal paths can create out-of-distribution samples [@jang2025timing]. Their native objectives should be evaluated as such. A mask optimized to retain information is not automatically a linear response decoder, and retraining a representation changes more than the coordinates of a frozen explanatory problem. The fixed response law in this paper is therefore one declared estimand, not a claim to subsume time-series explanation quality.

Meaningful Perturbation distinguishes deletion and preservation objectives and addresses artifacts induced by optimized masks [@fong2017]. ROAR retrains after feature removal to reduce the distribution-shift confound in a different evaluation task [@hooker2019roar]. Randomization tests examine whether explanations depend on learned parameters and labels, while metric-reliability studies examine whether evaluation rankings are stable [@adebayo2018; @tomsett2020]. Adversarial scaffolding can exploit out-of-distribution queries, and systematic time-series studies demonstrate sensitivity to perturbation methods and region sizes [@slack2020; @simic2025]. Together, these studies require us to distinguish response fidelity, robustness of its measurement, and physical or causal interpretation. Improvement in one is not evidence for all three.

Finally, worst-group optimization depends on group definitions and generalization, not merely a maximum in the training objective. Group-DRO experiments show the importance of regularization for worst-group performance [@sagawa2020]. Our independent finite-candidate comparison uses a bounded-loss concentration argument [@hoeffding1963] only when its assumptions hold. It neither certifies unbounded logit losses nor extends automatically to unobserved operating conditions.

# 3. Fixed-Response Formulation and Comparator Boundary

Fix the predictor $s$, target, displacement law $\mu_x$, and development information $\mathcal D$. A new explanation at $x$ observes an available descriptor $z(x)$ and a transcript $T_Q$ of $Q$ scalar construction responses. Its score uses a fresh $v\sim\mu_x$, not the construction residual. For an invertible linear basis $A$, define

$$
R(A,a;x)=\mathbb E_{v\sim\mu_x}[(a^\top Av-d_x(v))^2],\qquad
R_k^*(A;x)=\inf_{\|a\|_0\le k}R(A,a;x).
$$

Finite second moments suffice for the following projection characterization. Suppressing $x$, put $M=\mathbb E[vv^\top]$, $b=\mathbb E[vd]$, $c=\mathbb E[d^2]$, and $\beta=M^\dagger b$. The moments are uncentered because the decoder has no intercept. With $\|u\|_M^2=u^\top Mu$,

$$
R(A,\widehat a)=R_{\rm full}+C_k(A)+G_{\rm support}(A,S)+E_{\rm coef}(A,S,\widehat a),
$$

where $R_{\rm full}=c-b^\top M^\dagger b$, $C_k=R_k^*-R_{\rm full}$, $G_{\rm support}=R_S^*-R_k^*$, and $E_{\rm coef}=R(A,\widehat a)-R_S^*$. All three excess terms are nonnegative. The normal equations establish the identity for singular as well as nonsingular support moments. The mathematical foundation is quadratic projection [@yeh2019]; the decomposition specifies distinct experimental explanations for a measured gain.

For a fixed family $\mathcal A=\{A_j\}_{j=0}^{J-1}$, define $\Psi(v)=[A_0v;\ldots;A_{J-1}v]$ with at most $k$ nonzeros **across the whole union**. Then

$$
R_{k,\rm union}^*(x)\le\min_jR_k^*(A_j;x).
$$

The relation is stronger at the estimator level than an oracle comparison alone suggests. If a router uses $(\mathcal D,x,z,T_Q)$ to return $(j,\widehat a)$, a union estimator with the same information can return $\widetilde a$ that equals $\widehat a$ on block $j$ and zero elsewhere. Thus, for every scoring displacement,

$$
\boxed{\widetilde a^\top\Psi(v)=\widehat a^\top A_jv,\qquad
\|\widetilde a\|_0\le k.}
$$

This identity holds at any finite $Q$. It requires the gate to be fixed for that explanation before the fresh scoring displacement is supplied. It does not assert equal computational costs for arbitrary implementations. Conversely, a lazy union implementation can evaluate only the selected block, so a dense union's measured cost cannot be imposed on every union estimator. A meaningful cost advantage needs an explicit computational model and an actual measurement.

# 4. Shared-Coordinate Learning and Controlled Comparisons

We learn one orthogonal coordinate matrix shared across the inputs of a fixed predictor. The reference parameterization is $A_\theta=\exp(S_\theta)$ with $S_\theta=-S_\theta^\top$. For each development-training unit, normalized-correlation greedy search selects at most $k$ atoms from $V_{\rm fit}A_\theta^\top$. Restricted ridge regression then fits their coefficients from the $Q$ construction responses. Fresh within-training displacements score the fitted decoder. The primary response objective averages this actual finite-query error over independent development units. A predefined worst-group aggregation is treated as a separate robustness ablation and, when used, is applied identically to every matched objective. This prevents an aggregation change from being credited as a coordinate-objective gain.

The matched objective controls require care because two natural losses are degenerate for a full-dimensional orthogonal basis. Let $H_k(u)$ retain the $k$ largest-magnitude coordinates. Orthogonality gives $\|x-A^\top Ax\|_2^2=0$ and $\|A\beta\|_2^2=\|\beta\|_2^2$ for every $A$, so neither full reconstruction nor L2 attribution magnitude can rank bases. We instead use
$
J_{\rm rec,k}(A)=\mathbb E\|Ax-H_k(Ax)\|_2^2
$
for sparse reconstruction and
$
J_{\rm attr,k}(A)=\mathbb E\|A\widehat\beta-H_k(A\widehat\beta)\|_2^2
$
for attribution concentration, where $\widehat\beta$ is a dense raw-coordinate response vector estimated from the declared development response table. These controls share the orthogonal family, $k$, unit split, optimization budget and candidate-selection rule with response training.

The attribution-tail control also identifies the limiting case in which no independent response-objective gain should be expected. If $d(v)=\beta^\top v$ and $\mathbb E[vv^\top]=\sigma^2I$, then
$
R_k^*(A)=\sigma^2\|A\beta-H_k(A\beta)\|_2^2.
$
Thus attribution-tail sparsity is exactly the population coordinate-oracle objective, up to scale, for linear response under isotropic interventions. The proposed response objective becomes distinct only when nonlinear residuals, anisotropic intervention moments, finite queries, support search, or coefficient estimation matter. This is the regime tested by the real-data falsification experiment, rather than assumed a priori.

The current-support derivative passes through the coordinate transform and ridge solve. Discrete support changes make the objective piecewise smooth and nonconvex. Identity and a finite trajectory of learned candidates are frozen before an independent selection sample chooses one basis. Final units influence neither training nor selection. A finite-family uniform bound controls this selection only for genuinely bounded per-unit losses; raw squared response error is reported without applying that certificate when boundedness is unavailable. The dense reference costs cubic time in coordinate dimension for its matrix exponential and is restricted to small-dimensional studies; scalability is a separate empirical requirement.

The experimental comparisons answer different questions. Identity tests the reference coordinates. The best single basis is chosen on selection units, not retrospectively on test units. Plain union-OMP tests one estimator on the fixed union with the same total $k$ and $Q$. A descriptor-based route tests block restriction. Its information-matched union emulator tests whether that route has introduced a distinguishable prediction class. Shuffling the descriptor tests reliance on the prescribed context. These last two controls are necessary even when a route beats all single bases.

| Scientific challenge | Mechanism | Observable contrast |
|---|---|---|
| Keep the explanatory target unchanged | Collect the same original-space responses before changing coordinates | Prediction/reconstruction invariance; common scoring displacements |
| Separate approximation from finite-query fitting | Exact small-dimensional oracle plus the actual support-and-ridge decoder | Oracle-versus-estimator gaps as $k$, $Q$, and conditioning vary |
| Match information and selection | Independent units; declared development cost; same-information union; descriptor controls | Route/emulator equality, shuffled-context change, held-out basis-objective gain |

# 5. Experimental Questions and Evidence

The central empirical estimand is a paired independent-unit difference in fresh response MSE, conditional on the frozen predictor and selected explanatory mechanism. It is not diagnostic classification error, a training residual, or the expected minimum of noisy test losses. Repeated windows and repeated queries within a bearing, subject, or recording remain nested observations, not independent replications.

The minimal experiment set separates six questions. **E1, geometry:** exact small problems test uncentered and singular moments, full-budget invariance, and helpful or harmful bases. **E2, estimation:** query and support-budget sweeps distinguish oracle approximation from greedy support and coefficient error. **E3, information:** the same-information union and shuffled-descriptor controls test the interpretation of routing gains. **E4, learning objective:** response-trained coordinates are compared with the non-degenerate sparse-reconstruction and attribution-tail objectives above under the same coordinate family, $k$, development split, aggregation and selection rule; faithful TRIM/AWD and task-driven dictionary implementations are reported separately because their native objectives and model access differ. Structured-support controls test whether any finite-$Q$ gain is instead attributable to a smaller search family. **E5, generality:** only after E4 survives an independent vibration pilot are frozen inertial, physiological, and forecasting tasks added. **E6, cost and semantics:** development queries, online scalar queries, derivative access, latency, and memory are reported separately; intervention-law sensitivity and interpretable coordinate loadings test the limits of the response conclusion. E4–E6 require new empirical evidence and do not support performance claims here.

## 5.1 A controlled nonlinear comparison

The constructed predictor has 12 signal coordinates and one unperturbed context coordinate. In one context its signal sensitivity follows an identity atom; in the other it follows a DCT atom. A fixed hyperbolic-tangent score introduces nonlinearity. Ten frozen candidate bases comprise identity, DCT, and eight random orthogonal signal bases. The context coordinate is retained unchanged by every basis. The signal displacement is Gaussian with scale $0.5$, $k=1$, and the ridge coefficient is $10^{-4}$. For each query budget, 40 selection units determine the global basis and two-context rule, and 120 independent test units are scored with 128 fresh displacements each. Methods share the construction and scoring responses within each budget; different budgets use fresh units. The route receives the context that defines this synthetic mechanism.

| Fitting queries $Q$ | Plain union-OMP | Context route | Same-information union | Shuffled-context route |
|---:|---:|---:|---:|---:|
| 3 | 0.181839 | 0.043277 | 0.043277 | 0.208259 |
| 6 | 0.039830 | 0.016756 | 0.016756 | 0.093325 |
| 12 | 0.013784 | 0.013784 | 0.013784 | 0.076893 |
| 24 | 0.013608 | 0.013608 | 0.013608 | 0.082317 |

The entries are mean response MSE, not results on real time-series benchmarks. At $Q=3$, identity and the selection-chosen best single basis have MSE $0.233528$ and $0.122438$, respectively. The context route also improves on plain union-OMP. However, the same-information union reproduces the route with maximum absolute prediction difference exactly zero at every tested budget. Shuffling context increases its error. Thus this comparison establishes neither a routing-class advantage nor a benefit independent of the context-conditioned support restriction. The plain union estimator catches up at larger tested budgets, consistent with its finite-query search burden, but this constructed example does not establish a general convergence rate.

## 5.2 Scope of the supported conclusion

The geometry and emulation statements apply under their stated function-class and information assumptions. The synthetic comparison is a falsification control for a broad interpretation of routing, not a validation of shared-coordinate learning across domains. A practical representation claim requires an independent advantage over matched objective and structured-support controls, with the predictor, intervention semantics, and development access held fixed. Physical interpretability additionally requires meaningful coordinate structure or external semantic evidence; sparse response coefficients alone do not supply it.

# References
