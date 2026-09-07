---
name: statistical-power
description: Estimate sample size, detectable effect, or simulation power only when a real design decision requires it, using a defensible effect scale and the same model planned for analysis.
---

# Statistical Power and Sample Size

## Purpose

Answer one concrete design question: whether the available or planned independent
units can resolve an effect that matters. Power analysis is optional scientific
decision support, not a mandatory paper artifact.

## Workflow

1. State the decision: required sample size, power at a fixed budget, minimum
   detectable effect, or sensitivity across plausible effects.
2. Confirm the true independent unit and the exact planned analysis. Match the
   power model to the model that will analyze the experiment.
3. Choose an effect scale in this order:
   - smallest scientifically or practically meaningful effect;
   - conservative prior or pilot estimate with its uncertainty;
   - a clearly labelled conventional effect only when no better basis exists.
4. State alpha/error criterion, target power, allocation, pairing, clustering,
   dropout, or multiplicity only when they apply.
5. Use a closed-form calculation for a standard design or simulation for a
   complex design. Keep the implementation as small as the decision allows.
6. Examine a plausible effect range when one point estimate would be misleading.
7. Report the assumptions, calculation, result, and how the result changes the
   design or claim.
8. Save a table or curve only when it helps the researcher or manuscript; do not
   generate both by default.

## Output Contract

Produce:

- the design and independent unit;
- the effect basis and plausible range;
- the planned analysis and calculation method;
- required `n`, achieved power, or minimum detectable effect;
- relevant clustering/dropout/multiplicity adjustment;
- the design decision and important uncertainty;
- a reproducible command or script only when a calculation was actually run.

## Boundaries

- Do not invent or select an optimistic effect size to obtain an affordable `n`.
- Do not count dependent observations as independent units.
- Do not compute observed/post-hoc power as a substitute for reporting the
  estimate and uncertainty from collected data.
- Do not require power analysis for deterministic benchmarks, exhaustive data,
  descriptive studies, fixed public datasets, or comparisons where seeds/tasks
  rather than sampled participants define uncertainty unless it changes the
  inference.
- Do not require a power curve, table, Methods paragraph, evidence row, run row,
  figure manifest, decision log, change log, and open-question entry for every
  calculation.
- Do not default to Monte Carlo simulation when a transparent closed-form
  calculation answers the question.
- Do not stop merely because a journal or target venue is unset; venue formatting
  is separate from the scientific calculation.
- Fail clearly when the independent unit, planned analysis, or defensible effect
  scale is unavailable. State the missing assumption rather than guessing.
