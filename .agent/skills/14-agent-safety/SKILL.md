---
name: 14-agent-safety
description: Minimal safety check for credentials, private-data egress, paid remote compute, destructive remote writes, publication, and submission. Routine local research work proceeds without a safety detour.
---

# 14 Agent Safety

## Purpose

Stop only concrete actions that could expose sensitive data, incur unapproved
cost, destroy remote work, or publish externally. This skill is not a general
review stage and must not consume routine research tasks.

## Workflow

1. Identify the exact action about to occur.
2. If it is a routine local read, narrow reversible edit, local test, local
   compile, diff inspection, or public literature lookup, return `Proceed`.
3. Ask one concise confirmation only when the action uses:
   - credentials or private-data egress;
   - a paid API, cloud GPU, or remote compute budget;
   - destructive remote writes;
   - push, PR creation, release, publication, submission, or external disclosure.
4. Refuse secret extraction, fabricated results/citations, hidden destructive
   actions, impersonation, or unauthorized publication.
5. Return immediately to the original product task after a permitted decision.

Do not build action fingerprints, stable blocker IDs, risk taxonomies, permission
matrices, approval caches, or repeated safety loops.

## Output Contract

Use one of three short outcomes:

```text
Proceed.
```

```text
Confirmation required: <exact action, cost/data/remote effect>.
```

```text
Cannot execute: <specific prohibited action>. Safe alternative: <one option>.
```

A successful safety check is middleware, not the final deliverable.

## Boundaries

- Never read, print, or transmit secret values.
- Do not broaden the check beyond the exact action.
- Do not ask again when the current user request already authorizes the same
  repository, action, destination, and scope.
- Do not treat scientific disagreement, ordinary uncertainty, formatting, local
  editing, or local testing as a safety issue.
- Do not add hypothetical defenses for cases with no realistic data, cost,
  publication, credential, or destructive-write consequence.

## Validation

When this skill itself changes, inspect the three outcomes above and run only the
safety-related routing cases. The full repository suite belongs to final PR
review, not this skill.
