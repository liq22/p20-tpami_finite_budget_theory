---
name: 11-reference-audit
description: Verify the citations and source support that matter to a specific manuscript claim or final milestone, then correct the source or wording directly.
---

# 11 Reference Check

## Purpose

Ensure a cited source actually supports the nearby statement. Use only when the
user requests citation verification, citations changed materially, or a final
submission check needs it.

## Workflow

1. Identify the exact statements and citations under review.
2. Open the original source or official metadata.
3. Check authorship, title, venue, year, identifier, and the specific support for
   the manuscript statement.
4. Correct the citation, bibliography entry, or sentence directly.
5. Report only unresolved source problems that affect the paper.

## Output Contract

Produce corrected manuscript wording and bibliography entries, plus a short list
of material unresolved citations when necessary.

## Boundaries

- Do not run a full citation audit after every wording change.
- Do not generate source hashes, immutable snapshots, or audit ledgers.
- Do not use Python to count citations or infer support from metadata patterns.
- Do not report harmless formatting differences as scientific defects.
- Search snippets and secondary summaries do not replace the original source.
