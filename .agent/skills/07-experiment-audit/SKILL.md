---
name: 07-experiment-audit
description: Independently inspect a named completed experiment only when explicitly requested, and report the few validity problems that would change the result, interpretation, or next research decision.
---

# 07 Experiment Review

## Purpose

Test whether a specific reported result can support the intended scientific
conclusion. This is an explicit review task, not a default stage after every run.

## Workflow

1. Restate the claimed result and the decision it is meant to support.
2. Inspect the actual protocol, baseline, data split, metrics, outputs, and
   uncertainty relevant to that claim.
3. Check for common high-impact failures: leakage, unfair comparison, wrong unit
   of analysis, broken metric, missing uncertainty, or mismatch between method
   and implementation.
4. Reproduce one critical calculation or comparison only when needed.
5. Report only findings that change the conclusion or next experiment.

## Output Contract

Return a concise review:

- conclusion that remains justified;
- material validity issue, if any;
- exact correction or decisive rerun;
- whether the result can currently be used in the paper.

## Boundaries

- Do not generate a comprehensive audit template, PASS matrix, receipt, hash, or
  reviewer packet.
- Do not repeat checks already resolved without new experiment changes.
- Do not enumerate improbable corner cases unrelated to the reported result.
- Do not modify the experiment while claiming to be its independent reviewer.
- Minor formatting, logging, or naming issues are omitted unless they alter the
  scientific interpretation.
