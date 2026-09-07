---
name: pdf
description: Read, create, or transform a PDF when the PDF content or file is the requested research, review, collaboration, or submission deliverable.
---

# PDF

## Purpose

Recover, create, or transform the requested PDF content accurately. A readable
PDF or correctly extracted content is the product.

## Workflow

1. Classify the task as read, create, merge/split/rotate, form-fill, or OCR.
2. Identify the exact pages, fields, text, tables, or figures needed.
3. Use direct extraction first; use OCR only for pages that are actually image-only.
4. Create or transform the file while preserving the requested order and content.
5. Open or render the affected pages once and check readability, completeness,
   figures/tables, and page order.
6. Repair only concrete extraction or rendering errors.

## Output Contract

Produce the requested PDF or extracted content at the agreed path, with a concise
note for unreadable or uncertain source material.

## Boundaries

- Do not OCR an entire document when direct text extraction works.
- Do not begin with page styling, watermarks, compression, metadata, or format
  conversion unless requested or necessary for use.
- Do not run repository validators for routine PDF work.
- Do not create page-by-page audit logs, multiple render variants, or exhaustive
  visual checks without a concrete defect.
- Use code only when it processes the actual PDF; do not generate proof-of-work or
  file hashes.
- Stop when the requested content is accurate and the PDF opens correctly.
