---
name: docx
description: Read, create, or edit a Word document when the .docx file itself is the requested research, review, collaboration, or submission deliverable.
---

# DOCX

## Purpose

Produce or extract the requested Word content while preserving meaning and basic
document validity. Content and a usable `.docx` are the product.

## Workflow

1. Classify the task as read, create, or edit and identify the exact content to
   preserve or change.
2. Read/extract only the needed text, tables, comments, or tracked changes.
3. For creation, establish the document structure and content before detailed
   styles.
4. For editing, work on a copy and preserve unaffected content and formatting.
5. Apply only the page, heading, table, image, and citation rules needed by the
   user or venue.
6. Save the `.docx`, open or render it once, and check the affected content,
   tables, figures, and page flow.
7. Use structural validation only when XML or package internals were modified.

## Output Contract

Produce the requested `.docx` or extracted content at the agreed path. State any
content that could not be recovered or represented accurately.

## Boundaries

- Do not prioritize fonts, spacing, page dimensions, tracked-change metadata, or
  XML details before the document content is correct.
- Do not run the project validator or skill validator for a normal document edit.
- Do not create a change log, review report, or multiple preview variants unless
  explicitly requested.
- Do not write throwaway Python for work that the document tool already handles;
  use code only when it creates or repairs the actual file.
- Do not add defensive XML branches for formats not present in the source.
- Stop when the document opens correctly and the requested content is accurate and
  readable.
