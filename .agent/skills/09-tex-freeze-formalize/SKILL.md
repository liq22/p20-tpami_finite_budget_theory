---
name: 09-tex-freeze-formalize
description: Convert an author-approved Markdown manuscript into a compilable TeX paper while preserving scientific content, citations, figures, tables, equations, and section meaning.
---

# 09 TeX Formalization

## Purpose

Produce the formal TeX manuscript. Freeze notes and checklists are supporting
records, not substitutes for conversion and compilation.

## Workflow

1. Confirm the author approved the Markdown-to-TeX transition.
2. Convert the actual sections, citations, equations, figures, and tables.
3. Preserve wording, numbers, references, and conclusion strength unless a real
   TeX constraint requires a visible edit.
4. Compile once and repair direct errors such as missing files, broken references,
   or invalid syntax.
5. Open the resulting PDF and inspect the affected pages.
6. Record the transition briefly and stop.

## Output Contract

Produce:

- compilable TeX source;
- the resulting PDF;
- corrected references and included assets;
- one concise note for any unresolved content issue.

## Boundaries

- Do not rewrite scientific content as part of routine conversion.
- Do not spend cycles on spacing, line breaks, or typography that do not affect
  readability or venue requirements.
- Do not build freeze audit packages, hashes, or receipts.
- Do not run repeated full validations after a successful compile and page check.
