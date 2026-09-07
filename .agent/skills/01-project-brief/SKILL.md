---
name: 01-project-brief
description: "Establish or revise the minimum research state needed for the next scientific action: problem boundary, strongest evidence, failure, mechanism, claims, missing experiment, scope, and consequential author decisions."
---

# 01 Project Brief

## Purpose

Create a concise scientific state that makes the next research action obvious. Initialization is not a metadata-completion or approval workflow.

## Workflow

1. Define the problem:

   ```text
   Object
   Environment
   Observation
   Task or decision
   Failure or unresolved contradiction
   Desired understanding
   ```

2. Establish only the state needed for the next decision:

   ```text
   Research question
   Current strongest result and evidence
   Main failure
   Favored mechanism
   Strongest competing explanation
   Largest unresolved uncertainty
   Most informative next action
   Stopping condition
   ```

3. Resolve only contradictions that would change the method, experiment, interpretation, or manuscript scope.
4. Update current state in `paper/paper.yaml`. Use `paper/kickstart/new_project_intake.yaml` only as an optional one-time record of user-provided starting facts; do not synchronize it afterward. Leave unknowns as `TODO` or `unknown`.
5. Record an author decision only when the author actually made one and it affects direction, formal-source transition, or submission.
6. Read the resulting state once for scientific consistency and stop.

## Output Contract

Produce a usable current state with:

- one bounded research question;
- observed failure or unresolved contradiction;
- favored and competing explanations;
- current evidence and permitted claim strength;
- the smallest required experiment, analysis, literature check, or code change;
- in-scope/out-of-scope boundary;
- one next substantive action and stopping condition.

## Boundaries

- Do not create a second repository-level state file.
- Do not require title, venue, author metadata, all claims, or compliance fields before research can begin.
- Do not create status reports, dashboards, ledgers, approval packages, or blocker documents instead of updating the current state.
- Do not turn early hypotheses into approved claims because a template is complete.
- Do not polish titles or metadata while the problem, failure, and mechanism are unclear.
- Do not run Python for ordinary YAML or prose inspection unless the schema or validator itself changed.
- Do not require hashes, receipts, independent-review records, or machine proof of human decisions.
