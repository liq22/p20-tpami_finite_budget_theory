---
name: 06-experiment-ops
description: Execute one bounded experiment that tests a named claim or competing mechanism, returning actual run outputs, uncertainty, boundary, and interpretation with minimal reproducibility context.
---

# 06 Experiment Operations

## Purpose

Produce a real experimental result that changes a scientific decision. A run
plan, ledger row, validation report, audit package, or successful process exit is
not an experiment.

Use this Skill when a new or approved run must be executed. Parsing and
interpreting the outputs produced by that run are part of completion. A task that
only analyzes data from an already completed experiment routes to
`statistical-analysis`.

## Workflow

1. State the claim role:

   ```text
   demonstrate a failure
   test a mechanism
   test the key intervention
   compare task performance
   identify a boundary
   ```

2. Fix the competing hypotheses, independent unit, dataset/split, baseline,
   intervention, metrics, budget, and stopping rule.
3. Check only prerequisites that can invalidate the comparison: leakage,
   inconsistent data access, wrong metadata/sampling, unequal preprocessing,
   unconsumed config, broken metric, or target-domain tuning.
4. Run the experiment.
5. Inspect the actual outputs, parsed metrics, sample/unit counts, and one sanity
   check tied to the expected signature.
6. Quantify variability or uncertainty in a way appropriate to the design. Do not
   add mechanical significance tests.
7. Compare the result with the expected, rejection, and boundary signatures.
8. Classify the result as supporting, weakening, refuting, or leaving the claim
   unresolved. Preserve negative, null, unstable, and contradictory results.
9. Record only the reproducibility information needed to rerun and interpret the
   result: code version, config, data version, command, seed/unit, environment,
   metrics, result, and output path.
10. Stop. Use independent review only when explicitly requested.

## Output Contract

Return:

- claim and experiment role;
- what was actually run;
- baseline/intervention fairness conditions;
- actual primary and mechanism/property metrics;
- variability or uncertainty;
- result files, plots, or model outputs;
- interpretation, alternative explanation, and important boundary;
- concise reproducibility details.

A failed run is reported as a failed run. A scientifically negative completed run
is reported as evidence, not hidden or relabelled as failure.

## Boundaries

- Do not use this Skill solely to analyze data from a completed experiment; route
  that task to `statistical-analysis`. Run-level interpretation of outputs
  produced by the current execution remains in scope.
- Do not mark a run completed when outputs, units, or metrics are missing.
- Do not count failed, timed-out, invalid, or unverified executions as positive
  evidence.
- Do not select favorable datasets, seeds, metrics, or baselines after the fact
  without labeling the comparison exploratory.
- Do not give the proposed method extra data, metadata, preprocessing, target
  access, tuning, or compute.
- Do not automatically run every robustness test, statistical test, independent
  audit, or the full repository suite.
- Do not calculate hashes, create receipts, build evidence packages, or update
  every supporting paper record as a completion requirement.
- Add defensive checks only for observed/common failures or errors that could
  change the conclusion or corrupt the run.
- If scientific inputs are ambiguous, fail clearly rather than guessing or
  silently changing the protocol.
