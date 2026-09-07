# Code Change Examples

## Scenario 1 — Reproducible bug fix

```text
Fix the tensor-shape error in src/S01_Package/model.py for batched inputs.
Reproduce it with the existing failing test, patch the smallest code path, add a
regression case, and run the targeted test. Do not stop after explaining the
module or updating MODULE_MAP.md.
```

Expected product: changed implementation and a passing regression test.

## Scenario 2 — Bounded refactor

```text
Refactor the duplicated configuration parsing in these two modules into one
shared helper without changing public behavior. Update the relevant tests and run
them. Use normal Python documentation language; do not add repository-governance
terminology to comments.
```

Expected product: simpler source code with preserved behavior and passing tests.

## Scenario 3 — Scientific implementation

```text
Implement the approved normalization operator from
paper/method/method_spec.yaml in the named tokenizer module. Add a unit test for
the specified invariant and run the smallest smoke test. Do not redesign the
method or replace implementation with a design note.
```

Expected product: executable operator and test evidence for the specified
behavior.