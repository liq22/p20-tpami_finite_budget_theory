---
name: code-module-xray
description: Explain one existing code subsystem accurately enough to support a concrete implementation, debugging, experiment, or manuscript decision; route requested code changes to code-change.
---

# Code Module X-ray

## Purpose

Make one subsystem understandable. The product is a concise explanation that
enables a real decision, not a repository tour or documentation expansion.

## Workflow

1. Fix the subsystem and the decision the explanation must support.
2. Read the public entry point, main caller, relevant config, and closest test.
3. Trace one representative input-to-output path.
4. Explain the module's role, inputs, outputs, shapes/units, required conditions,
   scientific parameters, and common failure behavior.
5. Mark unsupported intent or runtime behavior as `UNKNOWN` and name the smallest
   test that would resolve it.
6. Update `MODULE_MAP.md` only when the explanation will be reused or an interface
   or scientific role changed.
7. Validate by one targeted import, test, dry run, or direct code inspection.

## Output Contract

Produce a bounded explanation containing:

- one-sentence role;
- representative data/control flow;
- inputs, outputs, and required conditions;
- scientific versus engineering parameters;
- known failure or uncertainty;
- the concrete decision it enables.

## Boundaries

- Do not use this skill when implementation, repair, refactoring, or optimization
  was requested; use `code-change`.
- Do not scan the whole repository or build a complete call graph.
- Do not update documentation merely to increase coverage.
- Do not run the full project validator for a local explanation.
- Do not use Python to produce architecture metrics or exhaustive inventories.
- Do not add hash, provenance, audit, gate, ledger, or blocker language to code
  comments or normal explanations.
