# pdf skill — invocation scenarios

Realistic single-paper scenarios that should trigger the `pdf` skill. Each names
the workspace artifact the skill is expected to read or produce.

## Scenario 1: Extract text from a co-author's PDF draft into markdown

A co-author emailed `manuscript_v2.pdf`. The user wants its text ingested into
the paper workspace so the markdown-draft skill can keep editing it.

Prompt: "Read `~/Downloads/manuscript_v2.pdf`, extract the full text preserving
section headings and the two results tables, and write the markdown to
`paper/draft/manuscript_from_pdf.md`. Note in `paper/logs/change_log.md` that
this is an unedited ingest from the co-author's PDF. Use layout-preserving
extraction and OCR only if the PDF is scanned."

Triggered behavior: text/table extraction (`pdfplumber` / `pdftotext -layout`),
optional OCR via `pdf2image` + `pytesseract`, write to `paper/draft/`, log to
`paper/logs/change_log.md`. Source PDF is never modified.

## Scenario 2: Build the camera-ready submission PDF from the frozen TeX

After `09-tex-freeze-formalize`, the user needs the final submission PDF plus a
cover-letter PDF for upload to the journal portal.

Prompt: "Compile `paper/tex/main.tex` to `paper/submission/manuscript.pdf`,
generate `paper/submission/cover_letter.pdf` from the cover-letter markdown,
then merge the cover letter in front of the manuscript into
`paper/submission/upload_bundle.pdf`. Verify page count and that the merged
file opens without errors before recording it in `paper/submission/`."

Triggered behavior: PDF creation (LaTeX build or `reportlab`), merge via `pypdf`
/`qpdf`, validate the result, write to `paper/submission/`.

## Scenario 3: Recover an appendix table from a scanned reviewer PDF

A reviewer response arrived as a scanned PDF; the user needs one table
re-digitized for `paper/reviews/response_to_reviewers.md`.

Prompt: "OCR page 3 of `paper/reviews/reviewer2_scan.pdf`, extract the table of
requested revisions into markdown, and append it to
`paper/reviews/response_to_reviewers.md` under a new `## Reviewer 2 requests`
section. Do not edit the source scan."

Triggered behavior: `pdftoppm`/`pdf2image` → `pytesseract` OCR →
`pdfplumber` table extraction on the rendered page → append to the response
markdown. Read-only on the source PDF.
