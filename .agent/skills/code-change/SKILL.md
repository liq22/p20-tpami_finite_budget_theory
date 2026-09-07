---
name: code-change
description: Implement, repair, refactor, or optimize one bounded code behavior while preserving the stated scientific problem, using fail-fast semantics and the closest relevant test.
---

# Code Change

## Purpose

Change executable behavior needed by the research. Source code and the relevant
test or real smoke result are the product. Architecture, reports, and defensive
machinery are secondary.

## Workflow

1. State the expected behavior, observed bug or bottleneck, and the scientific or
   engineering consequence.
2. Reproduce the behavior or establish the smallest real baseline.
3. Trace the shortest relevant path from input to output. Confirm data, labels,
   metadata, split, transforms, objective, metric, shapes, units, and config only
   where they affect this change.
4. Make the smallest coherent source modification.
5. For semantic inconsistencies in dataset, label, metadata, sampling rate,
   split, transform, task, objective, metric, model, checkpoint, or protocol:

   ```text
   detect -> clear error -> stop
   ```

   Do not guess, auto-repair, silently fall back, or continue with changed
   semantics.
6. Add or update a regression test only for an observed bug, a common user path,
   or a high-impact failure that could change a scientific result.
7. Run the closest targeted test, smoke path, or minimal experiment.
8. Inspect the output and diff for unintended numerical, interface, or scope
   changes, then stop.

Before adding an abstraction, validator, wrapper, cache, factory, registry, or
schema, ask:

1. Does it solve a real current problem?
2. Could the scientific result be wrong without it?
3. Is a direct local implementation simpler?

Abstract only after at least two real current use cases exist.

## Output Contract

Produce:

- changed source code;
- the relevant targeted test when needed;
- observed behavior before and after;
- one direct validation result;
- one remaining scientific or implementation uncertainty only when material.

## Boundaries

- Do not stop after updating `MODULE_MAP.md`, a plan, review report, comments,
  architecture document, or status record.
- Do not add manager -> adapter -> wrapper -> builder -> executor chains around a
  single implementation.
- Do not add broad validation layers, fallback trees, or defensive branches for
  hypothetical inputs outside the current research protocol.
- Do not write tests for every theoretical input combination or pursue coverage
  as a product.
- Do not run the full suite after each edit; reserve it for final PR review.
- Do not add hashes, receipts, artifact integrity checks, or supply-chain-style
  controls.
- Preserve scientific behavior unless the requested change explicitly modifies
  the method, protocol, or estimand.
