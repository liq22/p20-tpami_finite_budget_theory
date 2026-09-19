---
title: "When Coordinates Help: Finite-Budget Response Explanations"
author: []
lang: en-US
---

# Abstract

A change of coordinates can make an explanation compact without changing the function being explained. Whether it improves prediction of that function's responses depends on the coordinate budget, query budget, and information available to the estimator. We study sparse linear decoders of a frozen predictor's responses to a common original-space intervention law. A projection characterization separates the invariant full-class residual from coordinate approximation, support-search, and coefficient-estimation errors. A fixed union dictionary also contains every single-basis sparse decoder and can reproduce any routed decoder given the same information. These relationships motivate learning shared orthogonal coordinates through the fresh-response error of the actual finite-query decoder. Matched reconstruction and coefficient-concentration objectives isolate this choice of learning target, while information-matched support controls distinguish coordinate effects from search restrictions. In a controlled nonlinear example, a context route improves over plain union-OMP at three fitting queries, but its same-information union emulator produces identical predictions. A separate matched-objective diagnostic does not establish an incremental benefit of response training over coefficient concentration. These results establish comparison boundaries rather than a real-data advantage of learned coordinates. The remaining empirical question is when direct response training improves independently evaluated finite-budget prediction beyond matched objectives and support priors.

# 1. Introduction

Predictive models are often inspected through explanations that retain only a small number of features, time intervals, or transformed coordinates. The practical aim is not merely to produce a short description, but to retain the aspects of model behavior that matter for a specified question. Local surrogates, additive attributions, and response-based fidelity measures provide distinct operational answers to this aim [@ribeiro2016lime; @lundberg2017shap; @yeh2019]. For time series, relevance may be localized in time, distributed across channels, or expressed through temporal structure that a pointwise representation obscures [@ismail2020; @crabbe2021dynamask]. A compact representation is useful only insofar as it preserves the declared explanatory target.

The explanatory target must be distinguished from the coordinates in which an explanation is written. Removal-based methods differ in what is removed, how absent features are represented, and which aspect of model behavior is summarized [@covert2021removal]. Marginal and conditional feature interventions can answer different dependence questions [@janzing2020; @frye2021]. Perturbation choices also affect measured performance in neural time-series classifiers [@simic2025]. A lower error obtained after changing both coordinates and the intervention law cannot by itself identify a coordinate benefit.

Existing methods already provide substantial control over explanatory coordinates. TRIM interprets a model through transformed inputs and accommodates parameterized transformations [@singh2020trim]. Adaptive Wavelet Distillation learns wavelets using reconstruction, wavelet constraints, and interpretation sparsity while retaining a trained neural model [@ha2021awd]. Task-driven dictionary learning optimizes representations for a downstream objective rather than reconstruction alone [@mairal2012task]. Thus, changing coordinates or using an outer learning objective is not the unresolved issue.

The question is which source of improvement a finite-budget comparison identifies. Even with the predictor, target, and intervention law fixed, a coordinate change modifies both the best sparse approximation and the estimation problem presented to a finite-query decoder. Local-explanation theory demonstrates dependence on sampling and neighborhood choices [@garreau2020; @tan2023glime], and adaptive neighborhood sampling addresses query-efficient local fitting [@dhurandhar2022ans]. Structured sparse recovery shows how support restrictions can improve recovery under appropriate measurement assumptions [@baraniuk2010]. A coordinate advantage must therefore be distinguished from an information, search, or coefficient-estimation advantage.

Three challenges follow. **Semantic comparability** requires identical response targets and intervention laws. **Finite-budget attribution** requires separating sparse approximation from the errors of the fitted decoder. **Information-matched selection** requires exposing development information and support priors while keeping construction and final scoring distinct. FastSHAP separates amortization from value-function choices, and REAL-X uses optimization-matched comparisons to diagnose failures of learned feature selection [@jethani2022fastshap; @jethani2021realx]. These precedents motivate a controlled coordinate comparison rather than a new claim of universal explanation quality.

We study a shared orthogonal basis learned through the response error of a fitted sparse decoder. The basis is fixed across evaluation inputs; the support and coefficients may change with each input's construction responses. Reconstruction and coefficient-concentration controls use the same coordinate family and selection rule. A separate union-emulation control establishes that a routed decoder need not create a new prediction class. Figure 1 defines the fixed problem and the observable comparison; Figure 2 locates the learning intervention and the information boundaries.

The contributions are threefold. **(1)** We specialize response-projection geometry to budgeted coordinate comparisons, separating approximation, support-search, and coefficient-estimation effects. **(2)** We instantiate direct finite-query response training of shared coordinates and matched objectives that make its incremental value testable. **(3)** We establish and execute an information-matched union control that removes an intrinsic-routing interpretation of a synthetic performance gap. The first and third contributions establish analytical and controlled comparison boundaries. The second supplies a learning mechanism whose real-data benefit remains an empirical question.

# 2. Basic Theory and Problem Formulation

## 2.1 Problem setting

Let $f$ be a frozen predictor and $x\in\mathbb R^p$ its input in fixed, preprocessed coordinates. For a classification model, $s_t(x)=f(x)_t$ is an explicitly chosen scalar score; a forecasting task analogously fixes a horizon and output component. The rule selecting $t$ is fixed before perturbation and shared across methods. We suppress $t$ and write $s$. Any context descriptor $z(x)$ is available before explanation fitting and is not itself the explanation coordinate matrix.

An original-space displacement $v\sim\mu_x$ produces the model response

$$
d_x(v)=s(x)-s(x-v). \tag{1}
$$

The same law $\mu_x$ defines construction and scoring within a comparison. Changing this law defines another explanatory problem. Here an intervention means an input perturbation of a frozen model, not an identified intervention on a physical data-generating system [@covert2021removal; @janzing2020].

A method receives development information $\mathcal D$, the input and available context, and a construction transcript

$$
T_Q(x)=\{(v_q,d_x(v_q))\}_{q=1}^Q. \tag{2}
$$

The output is a coordinate map $A$ and coefficients $\widehat a$ with at most $k$ nonzeros, defining $\widehat d_x(v)=\widehat a^\top Av$. A shared $A$ may be learned from $\mathcal D$; $\widehat a$ is fitted separately for each input. The reference setting permits scalar forward evaluations, not uncharged gradients or new predictor training. There are $Q$ perturbed-score evaluations plus one reusable evaluation of $s(x)$; scoring and development evaluations are counted separately.

| Object | Meaning | Role in the comparison |
|---|---|---|
| $f,t,\mu_x$ | Predictor, scalar target, original-space displacement law | Fixed explanatory semantics |
| $\mathcal D,z(x)$ | Development information and available context | Common information access |
| $k,Q$ | Nonzero-coordinate budget and construction-response budget | Distinct resource constraints |
| $m,A,\widehat S,\widehat a$ | Method, coordinates, selected support, fitted coefficients | Intervention and intermediate quantities |
| $R,L_u,\Delta$ | Fresh-response risk, unit loss, paired effect | Outcomes, not training residuals |

## 2.2 Relevant theoretical foundations

Response fidelity is grounded in infidelity: a squared discrepancy between a linear explanation's predicted change and the actual model-output difference [@yeh2019]. For an invertible linear $A$, define

$$
R(A,a;x)=\mathbb E_{v\sim\mu_x}[(a^\top Av-d_x(v))^2]. \tag{3}
$$

Assume $\mathbb E\|v\|^2<\infty$ and $\mathbb E[d_x(v)^2]<\infty$. At a fixed $x$, put

$$
M=\mathbb E[vv^\top],\quad b=\mathbb E[vd_x(v)],\quad
c=\mathbb E[d_x(v)^2],\quad \beta=M^\dagger b.
$$

These are uncentered moments because the decoder has no intercept. Quadratic projection gives

$$
R(A,a;x)=R_{\rm full}(x)+\|A^\top a-\beta\|_M^2,
\qquad R_{\rm full}=c-b^\top M^\dagger b. \tag{4}
$$

The identity also holds for singular $M$: if $h\in\ker M$, then $h^\top v=0$ almost surely and hence $h^\top b=0$, so $b\in\operatorname{range}M$. Completing the square proves (4). This is a reused least-squares foundation, not a new explanation metric. Every invertible $A$ spans the same unrestricted linear response class. Its residual can remain positive when the response is nonlinear.

Sparse approximation restricts the admissible support of $a$; dictionary learning changes its coordinates, and structured sparsity restricts the support family [@coifman1992; @mairal2012task; @baraniuk2010]. These operations can affect finite-budget estimation even when the unrestricted prediction class is unchanged. Their established roles motivate distinguishing coordinates from the procedure that chooses a support.

## 2.3 Mathematical formulation

A method $m$ maps $(\mathcal D,x,z,T_Q)$ to $(A_m,\widehat S_m,\widehat a_m)$. Its sparse approximation limit and actual finite-query risk are different quantities:

$$
R_k^*(A;x)=\inf_{\|a\|_0\le k}R(A,a;x),\qquad
\mathcal R_{k,Q}(m)=\mathbb E_{x,T_Q}[R(A_m,\widehat a_m;x)]. \tag{5}
$$

The expectation in $\mathcal R_{k,Q}$ is conditional on the frozen development outcome and includes construction randomness. An empirical fitting residual does not estimate the fresh risk after support selection. All matched methods use the same response tables, including common fresh scoring displacements independent of their construction transcript. Independence concerns the sampling process conditional on $x$, not numerical distinctness: independent draws from a discrete intervention law may coincide. Rejecting or resampling scoring draws merely because their values appeared in the construction table changes the scoring law.

The independent sampling unit $u$ is a recording, subject, patient, machine run, or other prespecified non-overlapping entity. For $W_u$ observations within that unit, let fixed nonnegative weights $w_{uj}$ sum to one. The unit loss and paired effect are

$$
L_u(m)=\sum_{j=1}^{W_u}w_{uj}\frac1R\sum_{r=1}^R
[\widehat d_{uj,m}(v_{ujr})-d_{x_{uj}}(v_{ujr})]^2,
\quad
\Delta_u(m,m_0)=L_u(m)-L_u(m_0). \tag{6}
$$

The sample mean estimates $\Delta(m,m_0)=\mathbb E_u[\Delta_u(m,m_0)]$; negative values favor $m$. Windows and queries are nested measurements, not additional independent units. The primary reference $m_0$, $(k,Q)$, aggregation, and weighting are fixed using development data. Uncertainty is computed over independent units. This is a controlled algorithmic comparison, not an observational causal effect inferred from $\mathbb E[Y\mid m]$.

![**The fixed-response comparison.** Original-space perturbations of the same frozen score produce a common construction transcript and separate fresh scoring responses. The experimental intervention is the coordinate-learning objective, while the coordinate family, sparse decoder, information access, and budgets remain matched. The observed output is a fitted response predictor and its unit-level loss. A lower loss alone cannot identify whether coordinates improved approximation, support identification, or coefficient estimation. Symbols correspond to (1)–(6); no empirical advantage is asserted by the arrows.](../assets/figures/motivation.svg){width=100%}

## 2.4 Existing limitation and research gap

Learned interpretation coordinates, task-driven dictionaries, and query-efficient explanations already exist [@singh2020trim; @ha2021awd; @mairal2012task; @covert2021kernel]. Their existence does not determine whether directly training a coordinate map on the error of a finite-query response decoder improves over a reconstruction or coefficient-concentration objective under the same information and computational choices. Figure 1 isolates that intervention. A second ambiguity arises when a coordinate comparison also changes admissible supports: a larger fixed dictionary does not imply fixed coefficients or an absence of input-dependent support selection.

The gap is therefore an attribution problem: under matched explanatory semantics and budgets, which component of fresh response risk changes, and does a response-specific training objective yield a reproducible benefit beyond alternative objectives and support priors? Neither generic explanation accuracy nor intrinsic routing superiority follows from the formulation.

## 2.5 Research objective

This work investigates whether direct finite-query response training of a shared coordinate map reduces (6) relative to development-selected matched objectives, and whether any reduction is associated with approximation, support identification, or coefficient estimation. A regime-specific or reversed effect is part of the answer. The predictor, response target, and original-space law remain fixed within each test; broader semantic and cross-predictor claims require separate evidence.

# 3. Method

## 3.1 Overview and design rationale

The method has one learned object: a shared orthogonal coordinate matrix. It reuses a sparse response decoder and optimizes the response error that decoder incurs at the intended $(k,Q)$. Figure 2 separates three stages: development training produces a finite candidate trajectory; independent selection freezes one basis; a new input uses that basis with its own $Q$ construction responses. Fresh scoring responses evaluate the result and never return to the online fit or basis update.

To connect the objective to the gap, let $R_S^*(A;x)$ be the minimum population risk restricted to a selected support $S$, where $|S|\le k$. Adding and subtracting the restricted and cardinality-constrained optima in (4) gives

$$
\begin{aligned}
R(A,\widehat a;x)
&=R_{\rm full}+C_k(A)+G_{\rm support}(A,S)+E_{\rm coef}(A,S,\widehat a),\\
C_k(A)&=R_k^*(A)-R_{\rm full},\\
G_{\rm support}&=R_S^*(A)-R_k^*(A),\\
E_{\rm coef}&=R(A,\widehat a)-R_S^*(A).
\end{aligned} \tag{7}
$$

All three excess terms are nonnegative at the population level. The statement holds conditional on any realized fitted support and coefficients, including singular support moments. It specializes the projection foundation to the present comparison; it is not a new recovery theorem. Ridge bias belongs to $E_{\rm coef}$. Optimizing only an oracle approximation proxy omits the last two terms, whereas fresh error of the fitted decoder includes them. This motivates the training objective without guaranteeing that optimization will reduce population risk.

![**Shared-coordinate response learning and evaluation.** Thin-outline components are inherited: fixed response collection, greedy support selection, and restricted ridge fitting. The heavy-outline block identifies the response-specific outer objective and its update of the shared basis. Dashed feedback is confined to development training. A finite trajectory, including identity, is selected on separate units and then frozen. At a new input only the support and coefficients are fitted. Fresh evaluation responses enter the loss measurement, not the construction path. Matched proxy objectives replace the outer loss but retain the coordinate family, decoder, budget, and response-based selection rule. The diagram corresponds to Algorithm 1 and (8)–(13); the bottom identity is an external containment control.](../assets/figures/method_overview.svg){width=100%}

## 3.2 Shared coordinates and the finite-query decoder

We parameterize the shared matrix as

$$
A_\theta=\exp(S_\theta),\qquad S_\theta=-S_\theta^\top. \tag{8}
$$

Thus $A_\theta^\top A_\theta=I$ and $s(A_\theta^\top A_\theta x)=s(x)$. Responses are still collected at $x-v$, not by masking transformed coordinates. Orthogonality removes scale as a degree of freedom and makes isotropic ridge penalties comparable. The parameterization spans $SO(p)$; changing a row sign preserves the sparse prediction class, so excluding reflections does not restrict that class. These are representation constraints, not new prediction capabilities.

Write $V\in\mathbb R^{Q\times p}$ for construction displacements, $d\in\mathbb R^Q$ for their responses, and $Z=VA_\theta^\top$. Starting from $S=\varnothing$ and residual $r=d$, each greedy step chooses an eligible atom by

$$
j^*=\arg\max_{j\notin S,\ \|Z_j\|>0}
\frac{(Z_j^\top r)^2}{\|Z_j\|^2},\qquad S\leftarrow S\cup\{j^*\}. \tag{9}
$$

It then refits

$$
\widehat a_S=(Z_S^\top Z_S/Q+\lambda I)^{-1}Z_S^\top d/Q,
\qquad r=d-Z_S\widehat a_S,\qquad \lambda>0. \tag{10}
$$

The procedure stops at $k$ atoms, a zero residual, or no remaining eligible column. The output has zero coefficients outside $S$. We refer to it as OMP-ridge: positive ridge makes the residual different from the orthogonal residual of unregularized OMP. It is not the exhaustive support oracle in (5). Correlation ties use a fixed coordinate order. Near-zero numerical columns are excluded using the same rule for every basis.

## 3.3 Direct response training and matched objective interventions

For development-training input $x$, let $V^{\rm out},d^{\rm out}$ be fresh displacements and responses drawn independently of its $Q$ construction queries. The primary outer loss is

$$
\ell_{\rm resp}(A;x)=\frac1R\left\|V^{\rm out}A^\top
\widehat a(A;V,d)-d^{\rm out}\right\|^2. \tag{11}
$$

These outer responses train the basis and are not confirmation data. They are fixed across methods once collected. Gradients pass through (8) and (10) on the currently selected support, not through the discrete argmax in (9). Away from support changes this is a differentiable branch of a nonconvex objective; it is not a claim of global convergence or a justified interchange of differentiation and population expectation at support boundaries.

Two matched controls specify exactly what the outer-objective intervention changes. Let $H_k$ retain the $k$ largest-magnitude entries. Reconstruction training uses the **actual development input**:

$$
\ell_{\rm rec}(A;x)=\|x-A^\top H_k(Ax)\|^2.
$$

Full reconstruction through an orthogonal inverse is identically exact and cannot learn coordinates. Likewise, if the reconstruction input were a spherically symmetric perturbation $v$, then $Av\overset d=v$ for every orthogonal $A$, so its expected truncation loss would be invariant. The actual-input control avoids defining the competing objective only on that degenerate distribution. It is a matched sparse-reconstruction control, not a reproduction of Adaptive Wavelet Distillation.

Coefficient-concentration training first obtains a full raw-space ridge estimate from the same construction transcript,

$$
\widehat\beta_x=(V^\top V/Q+\lambda I)^{-1}V^\top d/Q,
\qquad
\ell_{\rm coef}(A;x)=
\begin{cases}
\dfrac{\|A\widehat\beta_x-H_k(A\widehat\beta_x)\|^2}{\|\widehat\beta_x\|^2},&\widehat\beta_x\ne0,\\
0,&\widehat\beta_x=0.
\end{cases}
$$

This is a concentration proxy of fitted response coefficients, not a native attribution map. Applying such a penalty to an already $k$-sparse decoder would be vacuous. No extra model gradients or higher-query coefficient oracle is provided to this control.

All three objectives share input access, parameterization, initialization, optimizer steps, candidate schedule, and downstream response decoder. Each is centered against its own identity-basis loss and uses the same prespecified aggregation: a mean for the minimal one-group experiment, or the maximum of predefined group means for a worst-group-excess study. With one group, identity centering is constant in $A$ and does not affect optimization. With multiple groups, worst-group excess is a different objective from worst absolute risk; the two must not be conflated. Groups cannot be invented from final-test outcomes [@sagawa2020].

## 3.4 Independent response-based selection

Training yields a finite, frozen family $\mathcal A_o=\{I,A_{o,1},\ldots,A_{o,J_o-1}\}$ for objective $o$. Independent development-selection units choose

$$
\widehat A_o=\arg\min_{A\in\mathcal A_o}
\operatorname{Agg}_{u\in\mathcal U_{\rm sel}}
\big[L_u(A)-L_u(I)\big]. \tag{12}
$$

Here $L_u$ always means fresh **response** error, including when candidates were trained by reconstruction or coefficient concentration. Every candidate uses the same construction and scoring responses; ties retain the earlier candidate, with identity first. Consequently, the comparison concerns alternative candidate-generation objectives under a common deployment-selection criterion. It does not compare entirely response-free learning pipelines.

The best fixed single basis is selected by the same rule from identity, DCT, and eight seed-fixed random orthogonal bases. The candidate count and search budget are reported separately for this finite fixed family and the learned trajectories. The comparison does not give any candidate a retrospective test-set minimum. Independent finite-candidate selection admits bounded-loss uniform-deviation arguments [@hoeffding1963], but raw squared response losses need not be bounded. Including identity is therefore not a population no-harm guarantee.

## 3.5 Information-matched support controls

For frozen candidate bases $\{A_j\}_{j=0}^{J-1}$, define the fixed union $\Psi(v)=[A_0v;\ldots;A_{J-1}v]$ and allow at most $k$ nonzeros across the entire union. Its oracle risk is at most the best single-basis oracle risk. More strongly, a route using $(\mathcal D,x,z,T_Q)$ to return $(j,\widehat a)$ can be emulated by zero-padding its coefficients:

$$
\widetilde a=[0;\ldots;\widehat a;\ldots;0],\qquad
\widetilde a^\top\Psi(v)=\widehat a^\top A_jv,
\qquad \|\widetilde a\|_0\le k. \tag{13}
$$

The identity holds for every scoring displacement and any $Q$, provided the route is chosen before that displacement is supplied. It matches the gate, information, and transcript rather than simply matching dictionary size. Plain union-OMP changes the search procedure; a structured union applies the same available block prior. The exact emulator is an equality control, not a baseline that another implementation is expected to beat.

If a coordinate advantage disappears against a structured support control, support identification is a plausible explanation, not an established causal mediation result. Diagnostic estimates of the terms in (7) are needed to separate mechanisms. An empirical gap against plain union search cannot establish routing-class superiority. Neither does (13) assert equal runtime: costs depend on implementation, and a lazy union can evaluate only the selected block.

## 3.6 Algorithm and computational scope

**Algorithm 1. Matched-objective shared-coordinate study.**

```text
Input: frozen scalar score s; law mu_x; independent train/select/test units;
       k, Q, R, ridge lambda; common aggregation and candidate schedule.
1. Collect fixed-target construction and separate scoring responses in raw space.
   Retain actual input vectors; expose the same inputs and responses to each method.
2. For each outer objective o in {response, reconstruction, coefficient concentration}:
   a. Start A at identity; for the coefficient proxy, fit full beta from Q responses.
   b. For the response objective, fit each decoder by greedy selection and ridge.
   c. Evaluate the chosen outer loss and update only the shared basis parameters.
      Reconstruction/coefficient losses need no decoder refit for their gradient.
   d. Freeze identity and the prespecified checkpoints; do not adapt this family
      after examining selection outcomes.
3. On separate selection units, select every learned/fixed family by the SAME
   fresh response criterion. Freeze the primary k, Q, reference and analysis rule.
4. On each test input, hold A fixed; use Q construction responses to fit only
   the support and coefficients. Predict responses on fresh displacements.
5. Aggregate observations within independent units, then compute paired effects.
   Report support controls and risk diagnostics separately from the primary effect.
Output: selected bases, sparse response predictors, unit losses and paired effects.
```

Steps 2b–2c differentiate through the decoder only for the response objective; the proxy objectives change candidate generation, not the final decoder. Steps 3–5 prohibit test-to-training feedback. There is no router or expert network in the learned shared-basis method.

The dense reference uses $p(p-1)/2$ parameters, $O(p^2)$ matrix storage, and an $O(p^3)$ matrix exponential per basis update. It is restricted to $p\le256$ input coordinates. Coordinate evaluation for $Q$ displacements costs $O(Qp^2)$ before sparse fitting. This is a small-dimensional reference, not evidence of scalability to raw long sequences. A fixed input representation or a future structured orthogonal family would define a separate, explicitly matched study. Development training, independent selection, online fitting, and scoring costs are reported separately.

# 4. Related Work

## 4.1 Explanatory targets, interventions, and nonlinear structure

LIME fits local interpretable surrogates, whereas SHAP characterizes additive feature attribution through a coalition value function [@ribeiro2016lime; @lundberg2017shap]. Integrated Gradients uses path-integrated derivatives, and DeepLIFT propagates activation differences relative to a reference [@sundararajan2017ig; @shrikumar2017]. These methods provide different objects and different forms of model access. Their output vectors are not interchangeable coefficients for predicting arbitrary displacements. In particular, a vector derivative is not one scalar forward query, and a path attribution depends on its reference and integration rule.

Infidelity directly measures the squared discrepancy between an attribution's predicted response and an actual model-output difference [@yeh2019]. Its quadratic optimization already supplies the unrestricted least-squares solution and discusses ill-conditioned moment matrices. Cardinality constraints and fitted supports specialize that geometry to separate sources of excess response risk. The removal-based framework of Covert et al. clarifies why retaining the same scalar loss is insufficient if the removal operator or value function changes [@covert2021removal]. Janzing et al. distinguish causal intervention from conditioning, whereas Frye et al. construct on-manifold value functions [@janzing2020; @frye2021]. These alternatives motivate an explicit estimand, not a universally preferred perturbation distribution.

Nonlinear explanation classes offer another route to lower residual error. Integrated Hessians attributes pairwise interactions through path-integrated second derivatives, Faith-Shap uses faithful higher-order approximations, and InstaSHAP connects Shapley explanations with purified additive models [@janizek2021; @tsai2023faith; @enouen2025instashap]. Their interaction structure changes what an explanation can represent. An invertible linear coordinate change instead preserves the unrestricted linear decoder class. Accordingly, a nonzero full-budget residual in our formulation diagnoses that class's limitation; it does not imply that nonlinear explanations cannot improve it.

## 4.2 Coordinates, dictionaries, and structured supports

Classical best-basis selection chooses among orthogonal representations according to a specified objective [@coifman1992]. Online dictionary learning supplies scalable reconstruction-based sparse coding, and task-driven dictionary learning differentiates downstream objectives through sparse codes [@mairal2010online; @mairal2012task]. The relevant distinction for response explanations is the learning target: reconstruction quality, attribution sparsity, and independently scored response error need not select the same basis.

TRIM makes transformed-domain interpretation explicit, including trainable transformations; Adaptive Wavelet Distillation learns wavelets jointly constrained by reconstruction and neural interpretations [@singh2020trim; @ha2021awd]. These are the closest representation-level predecessors. The present comparison retains their central capability—changing explanatory coordinates while preserving a predictor—and asks whether direct finite-query response training contributes beyond a matched reconstruction- or sparsity-driven objective. This requires both a faithful original-method comparison and an objective-matched coordinate-family comparison. The two comparisons answer different questions: original-method performance and the effect of the training objective within a controlled coordinate family.

Support restrictions are equally important competitors. Model-based compressive sensing replaces arbitrary sparse supports with structured families and derives recovery benefits under corresponding measurement conditions [@baraniuk2010]. A routed block is one such restriction, although the correlated union dictionaries and nonlinear response residuals considered here do not automatically satisfy compressed-sensing assumptions. The appropriate implication is to compare structured and unstructured support search with the same information, not to transfer a recovery theorem without its hypotheses.

## 4.3 Query efficiency, amortization, and instancewise selection

Garreau and von Luxburg characterize how LIME explanations depend on local sampling choices; GLIME analyzes stability, convergence, and locality [@garreau2020; @tan2023glime]. GLIME also illustrates that a sampling reparameterization may preserve the target objective: changing a sampling implementation is not always changing the estimand. Adaptive neighborhood sampling addresses the conditioning and nonlinear-approximation difficulties of query-efficient local explanation [@dhurandhar2022ans]. Improving KernelSHAP develops regression estimators, uncertainty estimates, and sampling improvements for a fixed Shapley target [@covert2021kernel]. These results establish query-efficient estimation as prior work, while leaving the coordinate-versus-support contrast to be specified for the response problem studied here.

FastSHAP amortizes a weighted regression objective and explicitly separates benefits of amortization from those of the value-function implementation [@jethani2022fastshap]. Its setup highlights why an offline-trained explanation mechanism cannot be compared to a cold-start estimator by counting online calls alone. Similarly, L2X learns instancewise feature subsets through an information-theoretic objective, while REAL-X addresses prediction encoding and omitted control-flow features in learned selections [@chen2018l2x; @jethani2021realx]. Sparse mixture-of-experts models establish trainable per-example routing for conditional computation [@shazeer2017]. The narrower question is whether a routed response decoder differs from a same-information estimator using a fixed union dictionary, and which imposed computational restriction would make that difference consequential.

## 4.4 Temporal explanations and evaluation validity

Time-series explanation methods address structure beyond an unordered feature set. Temporal Saliency Rescaling separates temporal and feature importance, DynaMask optimizes sparse masks using temporally informed perturbations, and xCEBRA couples contrastive representation learning with regularized attribution maps [@ismail2020; @crabbe2021dynamask; @schneider2025xcebra]. More recent methods sharpen the comparison further: ContraLSP learns contrastive, in-domain perturbations together with sample-specific sparse gates [@liu2024contralsp]; TimeX++ learns explanation-embedded instances through a modified information-bottleneck objective [@liu2024timexpp]; and TIMING introduces temporality-aware Integrated Gradients together with signed temporal evaluation metrics [@jang2025timing]. ORTE frames temporal explanations through information retention and learned binary masks [@yue2025orte]. Their native objectives should be evaluated as such. A mask optimized to retain information, localization, or signed attribution is not automatically a linear response decoder, and retraining a representation changes more than the coordinates of a frozen explanatory problem. These methods serve as external comparisons where their native semantics apply, not as interchangeable response coefficients.

Meaningful Perturbation distinguishes deletion and preservation objectives and addresses artifacts induced by optimized masks [@fong2017]. ROAR retrains after feature removal to reduce the distribution-shift confound in a different evaluation task [@hooker2019roar]. Randomization tests examine whether explanations depend on learned parameters and labels, while metric-reliability studies examine whether evaluation rankings are stable [@adebayo2018; @tomsett2020]. Adversarial scaffolding can exploit out-of-distribution queries, and systematic time-series studies demonstrate sensitivity to perturbation methods and region sizes [@slack2020; @simic2025]. These studies distinguish response fidelity, robustness of its measurement, and physical or causal interpretation. Improvement in one is not evidence for all three.

# 5. Experimental Questions and Evidence

The primary empirical estimand is the independent-unit paired mean in (6), conditional on the frozen predictor and selected explanatory mechanism. It is not diagnostic classification error or a test-set oracle minimum. The primary reference and budget pair are fixed using development data; other prespecified budget cells are secondary. Separate inferential claims across cells require simultaneous uncertainty or multiplicity adjustment. An interval containing zero is inconclusive rather than evidence of equivalence. Practical relevance is assessed against a justified, prespecified margin and measured costs, not an arbitrary percentage threshold.

The experiment set separates six questions. **E1, geometry:** exact small problems test uncentered and singular moments, full-budget invariance, and helpful or harmful bases. **E2, estimation:** query and support-budget sweeps distinguish oracle approximation from greedy support and coefficient error. **E3, information:** the same-information union and shuffled-descriptor controls test the interpretation of routing gains. **E4, learning objective:** response training is compared with actual-input sparse reconstruction and fitted-coefficient concentration in the same coordinate family, with common response-based selection. **E5, external validity:** one independently split real dataset and one frozen predictor first test C2; faithful TRIM/AWD, task-driven dictionary methods, and recent temporal explainers provide additional comparisons only under compatible native objectives and metrics. **E6, cost and semantics:** development and online queries, derivative access, runtime, memory, group aggregation, and intervention-law sensitivity delimit any benefit. E4–E6 do not yet supply real-data performance evidence.

## 5.1 A controlled nonlinear comparison

The constructed predictor has 12 signal coordinates and one unperturbed context coordinate. In one context its signal sensitivity follows an identity atom; in the other it follows a DCT atom. A fixed hyperbolic-tangent score introduces nonlinearity. Ten frozen candidate bases comprise identity, DCT, and eight random orthogonal signal bases. The context coordinate is retained unchanged by every basis. The signal displacement is Gaussian with scale $0.5$, $k=1$, and the ridge coefficient is $10^{-4}$. For each query budget, 40 selection units determine the global basis and two-context rule, and 120 independent test units are scored with 128 fresh displacements each. Methods share construction and scoring responses within each budget; different budgets use fresh units. The route receives the context that defines this synthetic mechanism.

| Fitting queries $Q$ | Plain union-OMP | Context route | Same-information union | Shuffled-context route |
|---:|---:|---:|---:|---:|
| 3 | 0.181839 | 0.043277 | 0.043277 | 0.208259 |
| 6 | 0.039830 | 0.016756 | 0.016756 | 0.093325 |
| 12 | 0.013784 | 0.013784 | 0.013784 | 0.076893 |
| 24 | 0.013608 | 0.013608 | 0.013608 | 0.082317 |

The entries are mean response MSE, not real time-series benchmark results. At $Q=3$, identity and the selection-chosen best single basis have MSE $0.233528$ and $0.122438$, respectively. The context route also improves on plain union-OMP. However, the same-information union reproduces it with maximum absolute prediction difference exactly zero at every tested budget. Shuffling context increases error. Thus this comparison establishes neither a routing-class advantage nor a benefit independent of context-conditioned support restriction. Plain union catches up at the larger tested budgets, but the example does not establish a general convergence rate.

## 5.2 A matched-objective diagnostic

A separate four-dimensional diagnostic tests the objective contrast in Section 3.3. The fixed score is $s(x)=\tanh(w^\top x)$ with $w=(0.6,-0.5,0.4,0.3)$ and $x\sim\mathcal N(0,0.4^2I)$. Two equally represented strata use Gaussian displacement scales $0.15$ and $0.0975$. Every method shares 24 training units, 24 selection units, and 64 test units, with $k=1$, $Q=24$, $R=48$, and $\lambda=10^{-4}$. Each learned objective uses 80 Adam steps at learning rate $0.04$, identity initialization, and nine candidates comprising identity and every tenth checkpoint. Training and selection use mean loss. The seed is 19. The ten-member fixed family is selected independently by the same response criterion.

| Coordinate objective or baseline | Mean test response MSE |
|---|---:|
| Identity | $6.601736\times10^{-3}$ |
| DCT | $5.555947\times10^{-3}$ |
| Best selected fixed basis | $1.058112\times10^{-3}$ |
| Actual-input reconstruction | $1.641236\times10^{-3}$ |
| Coefficient concentration | $5.732090\times10^{-5}$ |
| Direct response training | $5.785960\times10^{-5}$ |

Development selection chooses coefficient concentration as the primary matched reference before test losses are evaluated. The paired mean difference, response minus reference, is $5.386964\times10^{-7}$; its 95% unit-bootstrap percentile interval from 2,000 resamples is $[-1.028030\times10^{-7},1.275877\times10^{-6}]$. This diagnostic does not establish an incremental response-objective benefit despite the reduction relative to identity. The interval also does not establish equivalence. The input distribution is spherical, so the reconstruction objective is population-rotation-invariant in this particular diagnostic; its fitted variation does not constitute evidence against informative reconstruction on non-spherical real inputs. The result concerns one constructed score and budget, not real time-series performance or a general absence of benefit.

## 5.3 Scope of the supported conclusion

The geometry and emulation statements apply under their stated function-class and information assumptions. The first synthetic comparison is a falsification control for a broad interpretation of routing; the second tests matched objectives without establishing an incremental response-training benefit. Neither validates shared-coordinate learning across domains. A practical coordinate claim requires independent evidence against matched objectives and structured-support controls. Response MSE supports prediction of the declared model-response function; broader temporal localization, signed-attribution, or physical-meaning claims require compatible external evidence. A null or reversed C2 result must narrow the conclusion rather than prompt a retrospective change of model, data split, or primary budget.

# References
