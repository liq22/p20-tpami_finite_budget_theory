---
name: grill-me
description: Explicit-only read-only interview that pressure-tests a research idea, protocol, manuscript architecture, venue decision, or implementation plan one consequential question at a time.
license: MIT
compatibility: PaperTrace direct-capability mode; stateless and read-only.
metadata:
  version: '2.1.0'
  source_repository: https://github.com/mattpocock/skills
  source_commit: 391a2701dd948f94f56a39f7533f8eea9a859c87
  owner: PaperTrace maintainers
  task_type: core
  writes: false
---

# Grill Me

## Purpose

Expose weak assumptions and force clear decisions before expensive research or
implementation work. Challenge the proposal, not the person. This skill never
implements the resulting plan.

## Workflow

1. Identify the single highest-leverage unresolved decision.
2. Ask one concrete question at a time.
3. After each answer, state the implication and recommend a position with the
   main trade-off.
4. Verify external facts only when they materially affect the decision.
5. Resolve contradictions before moving to the next decision.
6. Stop when the user has a coherent, actionable position or explicitly ends the
   interview.

## Output Contract

During the interview, return one question and a brief recommendation. At the end,
provide a concise decision brief containing:

- chosen position;
- rejected alternative and reason;
- key assumption;
- decisive test or next action;
- unresolved material risk.

## Boundaries

- Use only when explicitly requested with wording such as “grill me”,
  “pressure-test”, or “red-team this plan”.
- Remain read-only: no file edits, experiments, commits, submissions, or approvals.
- Do not turn the interview into a large questionnaire, scorecard, audit report,
  or repository scan.
- Do not use Python to score answers or enumerate hypothetical cases.
- Do not create hashes, receipts, or trace packages.
- Stop once additional questions no longer change the decision.
