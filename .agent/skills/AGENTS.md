# Skill Directory Contract

Repository policy is defined in `../../AGENTS.md`; `.agent/` ownership is defined
in `../AGENTS.md`. Skill files specify only their local purpose and behavior.

## Routeable primary Skills

A routeable primary Skill must contain:

```text
Purpose
Workflow
Output Contract
Boundaries
```

Its route is declared only in `ROUTING_MATRIX.md` and the relevant evaluation
case definitions.

## Supporting and explicit-only Skills

- Supporting Skills and tools do not compete for the primary route.
- Audit and review Skills are selected only by explicit audit intent.
- Office, plotting, ML-library, lookup, and ARIS capabilities activate only when
  the selected primary needs them.
- Internal Skills must not gain a host wrapper unless repository authority is
  deliberately changed.

Do not copy repository-wide execution, scientific, language, safety, Python, or
integrity rules into individual Skills unless a narrower local exception is
required.
