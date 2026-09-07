# Code Module X-ray Examples

## Scenario 1 — Understand one model subsystem

```text
Inspect src/S01_Package/model/encoder.py, its caller, one config and its focused
test. Update src/MODULE_MAP.md with scientific role, 5W1H, interfaces, invariants,
configuration, failure signatures and paper links. Trace one input-to-latent path.
Do not refactor or change code.
```

## Scenario 2 — Reconcile paper and implementation

```text
The Methods section claims that the router enforces sparse expert selection.
Inspect only the router module, relevant config and test. Map what is actually
implemented, which invariant is tested, where the paper over- or under-specifies
behavior, and the smallest missing diagnostic. Do not rewrite the paper or code.
```

## Scenario 3 — Do not trigger

```text
Implement a new tokenizer, run experiments, and rewrite the Methods section.
```

This is not one code-comprehension action; route implementation, experiment and
writing as separate bounded actions.
