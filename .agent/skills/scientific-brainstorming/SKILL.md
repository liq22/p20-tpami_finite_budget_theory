---
name: scientific-brainstorming
description: Generate a small set of structurally different, scientifically meaningful research candidates and, when requested, synthesize one provisional front-runner into a falsifiable core innovation decision card.
---

# Scientific Brainstorming

## Purpose

Generate research directions that change a problem assumption, formal object,
representation, operator, supervision, structure, decomposition, generative
mechanism, adaptation mechanism, or diagnostic—not merely a model name, module
count, parameter count, dataset, or training budget.

Idea patterns are optional search lenses. They do not need to appear in the
output and never count as novelty evidence.

## Modes

### Candidate scan

Generate no more than four mechanism-distinct candidates and update
`paper/kickstart/idea_candidates.yaml`. Use two to four only when genuine
alternatives exist; one or zero is valid when the evidence supports no broader
search.

### Core innovation initialization

When the user invokes `@初始化入口`, asks to initialize the Idea stage, or asks
for a core innovation document:

1. record only the minimum known intake facts;
2. generate and prune no more than four candidates;
3. select one provisional front-runner only when current evidence supports it;
4. use `hypothesis-generation` as the only supporting Skill when formal
   competing mechanisms are needed;
5. update the one-page `paper/kickstart/core_innovation.md` decision card.

A provisional front-runner is not an approved paper direction.

## Workflow

1. State the observed problem, failure, contradiction, or unexplained boundary.
   If none is known, write `unknown`, leave the front-runner unselected, and make
   obtaining discriminating evidence the next action.
2. Separate observed facts, current inference, favored mechanism, strongest
   competing explanation, largest uncertainty, and novelty risk.
3. Use an applicable M1–M5 or P01–P15 lens only when it helps expose a different
   changed object. Do not require a pattern ID in the product.
4. Generate only mechanism-distinct candidates. For each candidate, state:
   - research object;
   - before → after core change;
   - mechanism sketch;
   - observable prediction;
   - rejection condition;
   - closest-neighbour delta or unresolved search question;
   - bounded kill test;
   - claim boundary.
5. Eliminate candidates whose difference is only scale, wording, a standard
   module replacement, dataset substitution, or workflow decoration. Merge
   candidates with the same core change and stop when the next candidate repeats
   an existing mechanism.
6. Compare the remaining candidates without a weighted score:
   important failure → depth of changed object → irreducible prior-art difference
   → mechanism specificity → falsifiability → bounded feasibility.
7. Formalize at most one provisional front-runner. Keep one strongest competing
   explanation, one divergent-prediction pair, one main confound, and one
   confound-isolating decisive test.
8. Verify only the closest prior needed for the decision. Mark it `unverified`
   when the original source cannot be checked; do not claim novelty from a
   pattern label.
9. Predeclare how positive, null, contradictory, and boundary-only outcomes
   change the direction. Null or contradictory evidence must revise, downgrade,
   or eliminate the claim.

## Output Contract

### Candidate scan

Update `paper/kickstart/idea_candidates.yaml` with no more than four concise
candidates and a retain/revise/merge/downgrade/eliminate recommendation. Do not
add weak candidates to reach a count.

### Core innovation initialization

Update only as needed:

```text
paper/kickstart/new_project_intake.yaml
paper/kickstart/idea_candidates.yaml
paper/kickstart/core_innovation.md
```

The core document is a one-page decision card containing:

- observed problem or unresolved contradiction;
- current claim at risk;
- before → after core change;
- one provisional front-runner, when supported;
- favored mechanism and strongest competing explanation;
- closest verified prior and irreducible delta;
- divergent prediction;
- one decisive test;
- scope or boundary;
- next action and stop/rejection condition.

Return the changed files, the current decision, the decisive next action, and at
most one remaining uncertainty.

## Boundaries

- Do not invent a failure, result, prior-art gap, novelty claim, or author
  decision.
- Do not require a fixed candidate count or generate variants after mechanisms
  repeat.
- Do not treat M/P patterns as required output, a quota, score, gate, or novelty
  proof.
- Do not add formula placeholders. Include mathematics only when it is already
  defined and changes the decision.
- Do not use Python to enumerate idea combinations or score creativity.
- Do not generate long speculative packets for weak candidates.
- Do not write manuscript prose, implement code, run experiments, or approve the
  paper direction in this Skill.
- Do not reopen broad brainstorming after one candidate enters formal hypothesis
  testing unless new evidence invalidates its core assumption.
- Do not create hashes, receipts, evidence packages, dashboards, schemas, or
  process layers around idea exploration.
