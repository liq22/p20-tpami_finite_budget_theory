# markitdown - invocation scenarios

Realistic single-paper-workflow scenarios for the markitdown skill. Each scenario
states the trigger, the source, the workspace target, and the command. Replace
angle-bracket placeholders with real paths before running.

## Scenario 1: Ingest a reviewer's Word document into ai_review.md

A journal editor returned reviewer comments as a `.docx` with tracked changes.
The reviewer-response skill needs plain Markdown to quote and address each
comment, so convert first.

- Source: `~/Downloads/reviewer2_comments.docx`
- Target: `paper/reviews/ai_review.md`
- Command:
  ```bash
  pip install 'markitdown[docx]'   # if not already installed
  markitdown ~/Downloads/reviewer2_comments.docx -o paper/reviews/ai_review.md
  ```
- Then: open `paper/reviews/ai_review.md`, confirm every numbered comment and the
  tracked-change text survived, and hand off to the `13-reviewer-response` skill.
- Log the ingestion in `paper/logs/change_log.md`.

## Scenario 2: Batch-convert a folder of literature PDFs for the reading matrix

You have ~20 candidate PDFs to triage for `paper/refs/reading_matrix.md`. Reading
each PDF is slow and token-heavy; converting them to Markdown lets the literature
skills compare them cheaply.

- Source: `paper/refs/pdfs/*.pdf`
- Target: `paper/refs/md/` (one `.md` per PDF, with a metadata header)
- Command:
  ```bash
  python .agent/skills/markitdown/scripts/convert_literature.py \
      --input-dir paper/refs/pdfs --output-dir paper/refs/md
  ```
- Then: skim the converted `.md` files, rank them, and write the keepers into
  `paper/refs/reading_matrix.md` with their BibTeX keys from
  `paper/refs/references.bib`. Surface any OCR failures (scanned-only PDFs) in
  `paper/logs/open_questions.md` rather than dropping them silently.

## Scenario 3: Turn a supplementary XLSX data export into a Markdown table

A cited paper's supplementary data shipped as `supp_table_s3.xlsx`; you need its
contents as a Markdown table so `paper/experiments/statistics.md` can reference
the same numbers during ablation analysis.

- Source: `paper/assets/tables/source/supp_table_s3.xlsx`
- Target: `paper/assets/tables/supp_table_s3.md`
- Command:
  ```bash
  pip install 'markitdown[xlsx]'
  markitdown paper/assets/tables/source/supp_table_s3.xlsx \
      -o paper/assets/tables/supp_table_s3.md
  ```
- Then: verify the column headers and numeric cells survived conversion (XLSX
  formatting/merged cells sometimes collapse), and cite the table in
  `paper/experiments/ablation.md` with its source path recorded in
  `paper/logs/change_log.md`.
