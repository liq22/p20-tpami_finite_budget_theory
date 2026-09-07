---
name: 10-language-polish
description: Improve stable manuscript language, including explicit anti-defensive revision, without changing or deleting claims, mechanisms, examples, equations, numbers, citations, terminology, evidence strength, uncertainty, limitations, or conclusion boundaries.
---

# 10 Language Polish

## Purpose

Improve expression only after the scientific content is stable. Normal polish
returns revised prose, not a language audit or an implicit content rewrite.

When the user explicitly targets defensive writing, remove rhetorical
self-protection while preserving every qualification that affects validity,
evidence strength, interpretation, or use.

## Workflow

1. Identify the target text's scientific atoms: claims, definitions, mechanisms,
   assumptions, findings, examples, equations, numbers, citations, terminology,
   uncertainty, and limitations.
2. Preserve that content set and its strength.
3. For explicit anti-defensive revision, load
   `../anti-defensive-writing/SKILL.md`. Classify each candidate as an empty
   disclaimer, necessary scope condition, evidence-based qualification, real
   limitation, useful contrast, or redundant clarification. Delete only the
   empty/redundant items; express scope positively; collapse stacked hedges into
   one calibrated statement; keep real limitations where they affect
   interpretation.
4. Improve syntax, transitions, concision, and domain-native terminology.
5. Replace vague generic nouns only when the intended scientific object is clear.
   Do not perform blind global replacements.
6. Remove workflow/repository wording that accidentally entered prose, but move
   methodologically necessary search/coding details to the appropriate Methods or
   supplement rather than deleting them.
7. Compare original and revision once. If meaning cannot be preserved, stop and
   name the ambiguity instead of guessing.

An explicitly requested compression is not ordinary polish. It must first
identify what must remain and then report any claim, example, citation, mechanism,
or boundary that was merged, moved, weakened, or removed.

For an explicitly requested camera-ready check, inspect abbreviations, notation,
and venue formatting and compile once when TeX changed.

## Output Contract

For normal polish and anti-defensive revision, return the revised text directly
and preserve scientific content exactly. For explicit compression, return the
revised text plus a short semantic-change note. For explicitly requested
anti-defensive annotations, return only changed sentence pairs and a one-line
reason. Mention a content ambiguity only when author judgment is required.

## Boundaries

- Do not polish unsupported or logically incomplete content instead of fixing it.
- Do not delete unique technical content merely to make prose shorter.
- Do not replace calibrated evidence verbs with stronger ones or erase real
  uncertainty, assumptions, confounders, null results, or limitations.
- Do not use a global banned-word list; a hedge or contrast can carry necessary
  scientific meaning.
- Actual reviewer comments and response letters route to
  `13-reviewer-response`.
- Do not add abstract nouns, balanced lists, disclaimers, or framework language
  merely to sound academic.
- Do not insert snapshot dates, record counts, coding statuses, promotion rules,
  repository paths, gates, ledgers, or Agent workflow into an Abstract or normal
  scientific prose.
- Do not produce terminology inventories, grep reports, scoring tables, hedge
  counts, or readiness matrices unless explicitly requested.
- Do not use Python to evaluate prose, count stylistic patterns, or scan ordinary
  Markdown.
- Do not run repository-wide tests for a prose-only change.
