---
name: experimental-design
description: Design the smallest fair experiment that reduces a named scientific uncertainty by fixing the estimand, independent unit, competing explanation, information access, outcome meanings, and stopping rule before the run.
---

# Experimental Design

## Purpose

Design an experiment that can change one scientific decision. The product is the
actual protocol or run layout needed to distinguish explanations—not a collection
of logs, checklists, power curves, or generic design templates.

## Workflow

1. State the current claim, largest unresolved uncertainty, and result that would
   weaken or reject the claim.
2. Identify the favored mechanism and strongest competing explanation.
3. Before designing the run, write:

   ```text
   required evidence
   possible outcomes
   decision under each outcome
   ```

   If every plausible outcome leaves claim confidence, mechanism discrimination,
   method choice, theory, boundary, novelty, and reviewer-critical conclusions
   unchanged, stop and do not run the experiment.
4. Define the estimand and true independent experimental unit. Repeated windows,
   cells, patches, frames, folds, seeds, or measurements from one unit are not
   automatically independent replicates.
5. Identify the main confound that could mimic the expected result.
6. Choose the smallest informative comparison from only what the question needs:
   - naive or canonical baseline;
   - strongest recent method;
   - closest prior art;
   - proposed method with the key mechanism removed;
   - simplest valid alternative.
7. Make information and budget access explicit:

   ```text
   training data access
   target-environment information
   metadata access
   pretraining
   search/tuning budget
   compute budget
   evaluation protocol
   ```

   Match these where possible. Disclose unavoidable asymmetry and do not support an
   unconditional superiority claim from an asymmetric comparison.
8. Decide what varies, what remains fixed, and whether randomization, blocking,
   pairing, stratification, or a factorial design is actually needed.
9. Define:

   ```text
   intervention
   control/baseline
   primary task metric
   mechanism/property metric
   uncertainty or repeated units
   rejection signature
   boundary/assumption-breaking test
   resource ceiling and stopping rule
   ```

10. Match the planned analysis to the design. Use a power calculation only when a
    defensible effect scale and sample-size decision exist.
11. Produce the executable protocol, allocation, config, or run table required by
    the experiment. Record only the minimum information needed to run and
    interpret it.
12. Check once that every design element answers the claim and that no condition
    receives privileged information.

## Output Contract

Produce a bounded experimental protocol containing:

- claim at risk and key uncertainty;
- favored and competing hypotheses;
- possible outcomes and decision under each;
- independent unit and estimand;
- intervention, baseline, and confound controls;
- data, target-information, metadata, pretraining, tuning, compute, and evaluation
  fairness;
- primary and mechanism metrics;
- randomization/blocking/pairing only when required;
- planned analysis, uncertainty, rejection signature, boundary test, budget, and
  stopping rule;
- executable run/config/layout when requested.

Update `paper/experiments/` records only to keep the real protocol and later result
understandable. The records are not the experiment.

## Boundaries

- Do not begin from a favorite DOE template. Begin from the claim, uncertainty,
  and independent unit.
- Do not mechanically require randomization, blinding, blocking, factorial DOE,
  power analysis, preregistration, or a reporting-standard checklist when they do
  not change the inference.
- Do not treat dependent observations as independent sample size.
- Do not give the proposed method extra data, metadata, target-domain access,
  preprocessing, pretraining, tuning, or compute that the baseline does not
  receive without explicit disclosure.
- Do not design every possible robustness experiment. Include only tests whose
  outcomes could change the claim, mechanism, novelty, or boundary.
- Do not add weak baselines merely to make a table look complete.
- Do not require updates to decision logs, change logs, open-question logs,
  evidence matrices, manifests, and figures as a completion quota.
- Do not write scripts merely to format a small allocation table when a direct
  table or existing tool is sufficient.
- Fail clearly when the independent unit, target leakage boundary, baseline,
  information access, or primary outcome is undefined; do not guess and continue.
