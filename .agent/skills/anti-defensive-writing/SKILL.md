---
name: anti-defensive-writing
description: Support evidence-bounded academic revision by removing rhetorically empty caveats, disclaimers, stacked hedges, imagined-reviewer rebuttals, and negative self-limitation while preserving real uncertainty, scope, limitations, claims, numbers, citations, and technical meaning.
license: MIT
metadata:
  upstream: Kiterlin/anti-defensive-writing
  upstream_commit: 60ff7d1c2695d9b56ed5593bed1b02a3ab744cd7
  upstream_path: SKILL.md
  role: supporting
---

# Anti-Defensive Writing

## Purpose

Support `10-language-polish` when scientifically stable prose is weakened by
rhetorical self-protection. Advance the evidence-bounded claim directly. Replace
empty caveats with positive scope, precise uncertainty, or one necessary
limitation.

This Skill is internal support, not a host entry or a competing primary.
Confidence must come from evidence and sentence structure, not from stronger
unsupported verbs.

## Workflow

1. Freeze the semantic invariants: claims, definitions, mechanisms, assumptions,
   findings, examples, equations, numbers, citations, terminology, uncertainty,
   and limitations.
2. Classify each suspected construction as exactly one of:
   - an empty disclaimer written for an imagined reviewer;
   - a necessary scope condition;
   - evidence-based uncertainty;
   - a real methodological limitation;
   - a useful conceptual contrast;
   - a redundant clarification.
3. Apply the minimum valid transformation:
   - delete an empty disclaimer;
   - express a scope condition positively by stating what the study examines,
     tests, or supports;
   - collapse stacked hedges into one calibrated statement and name the source of
     uncertainty when it matters;
   - state a real limitation once where it changes interpretation;
   - keep a contrast only when the contrast carries the argument;
   - delete a clarification that adds no evidence, scope, or logic.
4. Rebuild only the affected sentence or paragraph around:
   `claim -> evidence/reasoning -> necessary scope or boundary`.
5. Reread the adjacent context and verify that no semantic invariant or evidence
   strength changed.

## Detection Cues

Treat these as cues, not forbidden phrases. Keep them when they carry necessary
logic.

English cues include:

- `This paper does not claim ...`
- `We do not attempt to ...`
- `This is not to say that ...`
- `This should not be taken to mean ...`
- `The goal is not X but Y ...`
- `Although this study has limitations ...`
- `It is worth noting that ...`
- repeated `may`, `might`, `could`, `potentially`, or `possibly`

Chinese cues include:

- `本文并不试图……`
- `这并不意味着……`
- `需要说明的是……`
- `必须指出的是……`
- `值得注意的是……`
- `尽管本研究存在上述局限……`
- repeated `可能`, `或许`, `在一定程度上`, or `某种意义上`

## Rewrite Tests

A valid revision passes all four tests:

1. The main point appears before any necessary qualification.
2. Every retained hedge corresponds to a named uncertainty in evidence, design,
   inference, or scope.
3. Removing or moving a sentence does not hide a result, confound, assumption,
   or limitation needed to interpret the claim.
4. The revised evidence verb is no stronger than the original evidence permits.

Example:

```text
Defensive:
This does not mean that load has no effect on the measured signal.

Direct:
Load changes response amplitude and transmission characteristics; the invariant
concerns the fault-order relation.
```

## Output Contract

For normal revision, return the revised text directly. When the user explicitly
requests annotations, show only the changed sentence pairs and a one-line reason
for each substantive change.

Do not return hedge counts, banned-word scores, caveat inventories, reviewer
simulations, or a style audit unless explicitly requested.

## Boundaries

- Do not convert `may`, `suggests`, association, or exploratory evidence into
  `demonstrates`, causation, or a confirmed mechanism.
- Do not remove scope conditions, assumptions, confidence intervals, null or
  negative results, confounders, safety constraints, ethical limits, or legal
  qualifications that affect interpretation or use.
- Do not hide a real limitation by relocating it outside the reader's path.
- Do not apply a global word blacklist; the same phrase can be defensive in one
  sentence and necessary in another.
- Actual reviewer comments and response letters route to
  `13-reviewer-response`.
- If the scientific content is unsupported or logically incomplete, repair the
  claim with `05-claim-evidence` or the section with `08-markdown-draft` instead
  of polishing around the defect.
- Do not run repository-wide grep, Python scoring, or prose metrics for ordinary
  anti-defensive revision.

## Provenance

Adapted for PaperTrace from `Kiterlin/anti-defensive-writing` at commit
`60ff7d1c2695d9b56ed5593bed1b02a3ab744cd7` under the MIT License. See
`LICENSE.txt` and the repository-level `NOTICE.md`.
