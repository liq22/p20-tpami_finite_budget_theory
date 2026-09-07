---
name: pymc
description: Support a bounded Bayesian analysis with an explicit estimand, defensible model and priors, convergence checks, predictive validation, and honest posterior uncertainty.
---

# PyMC

## Purpose

Use PyMC when a selected analysis genuinely needs Bayesian estimation, hierarchical partial pooling, posterior prediction, prior sensitivity, or Bayesian model comparison.

This is a supporting implementation capability. The primary Skill owns the scientific question, design, estimand, and conclusion boundary.

## Workflow

1. Confirm the estimand, independent unit, likelihood, hierarchy, prior information, and decision that the posterior must inform. Stop if these are undefined.
2. Build the smallest model that represents the design. State which assumptions are substantive and which are computational.
3. Inspect prior implications when they can reveal an implausible scale, sign, or data-generating behavior. Revise priors transparently; do not tune them to recover a preferred conclusion.
4. Sample with an explicit configuration and random seed. Surface divergences, poor mixing, weak effective information, identifiability problems, and numerical failures rather than hiding them.
5. Use diagnostics and thresholds appropriate to the model and decision. A numerical rule is evidence about the sampler, not proof that the model or claim is correct.
6. Check posterior predictions against the aspects of the observations that matter to the claim. Preserve model misspecification and boundary failures.
7. Compare models only when the comparison distinguishes a scientific explanation or changes model choice. Inspect the reliability of the comparison criterion and prefer the simpler model when evidence is not discriminating.
8. Produce the requested model code, posterior summary, prediction, table, or comparison. Record a completed run and formal evidence only when those records are in use.
9. Report null, unstable, contradictory, and prior-sensitive results directly, and update the claim or applicability boundary.
10. Re-run the closest bounded analysis needed to verify the change, then inspect the output once.

## Output Contract

Return:

- estimand, likelihood, hierarchy, and prior rationale;
- sampler configuration and diagnostics relevant to validity;
- posterior estimate or predictive result with uncertainty;
- prior/posterior sensitivity or model comparison when decision-relevant;
- remaining model mismatch and interpretation boundary;
- the resulting claim decision and one direct validation.

Persist posterior samples or fitted artifacts only when the task needs them, using an explicit path and enough configuration to reconstruct their role. A summary record does not replace the actual analysis result.

## Boundaries

- Do not require target-journal, statistics, ablation, reproducibility, decision-log, dead-end, or insight files before a bounded analysis.
- Do not impose a universal chain count, draw count, convergence threshold, prior family, or model-comparison cutoff independent of the model and decision.
- Do not skip or conceal sampler and identifiability failures.
- Do not silently switch sampler, likelihood, parameterization, prior, model family, or inferential target.
- Do not interpret posterior probability as a frequentist p-value or observational association as causation.
- Do not run Bayesian modeling when a simpler direct estimate answers the question.
- Do not create sampler wrappers, model registries, fallback stacks, or generic Bayesian report packages.
- Do not suppress a posterior result because it weakens or refutes the current claim.
