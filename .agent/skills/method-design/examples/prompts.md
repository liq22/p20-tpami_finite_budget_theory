# Method Design Examples

## Scenario 1 — Remove module soup before implementation

```text
Use Card 2M. Turn the approved C1/C2 direction into paper/method/method_spec.yaml.
For each proposed component, state its scientific role, strongest alternative,
deletion test, property metric, and complexity cost. Remove components that do not
earn a distinct role. Do not write code or manuscript prose.
```

## Scenario 2 — Redesign an existing method around a failure boundary

```text
Use method-design on the selected method. The current system fails under
cross-domain sampling-rate shift. Define assumptions/invariants, the changed
research object, expected and rejection signatures, one negative control, one
boundary test, and an outcome-to-hypothesis table. Update method_spec.yaml only.
```

## Scenario 3 — Direct problem without an IDEA record

```text
The research direction is already human-approved and did not use the idea
workspace. Set origin.type=direct_problem, link the approved claims, and design the
minimum mechanism/evaluation contract. Keep the experiment approval gate false.
```
