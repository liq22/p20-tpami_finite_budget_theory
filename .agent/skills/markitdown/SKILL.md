---
name: markitdown
description: Convert office documents (PDF, DOCX, PPTX, XLSX, images, HTML, CSV) into clean Markdown for the single-paper workflow's reading and drafting stages. Implementation-only supporting skill; prefer scientific-visualization for figures and scikit-learn/statsmodels for tabular analysis. Do not use for LaTeX, schematics, experiments, training, or prose.
---

# MarkItDown - File to Markdown Conversion

## Purpose

This skill is the single source of truth for turning **foreign file formats** into Markdown inside the single-paper workflow. It wraps Microsoft's `markitdown` Python tool so that anything a researcher receives as a non-Markdown artifact — a colleague's DOCX draft, a journal's PPTX, a PDF reprint, an XLSX data export, an image with a figure, an HTML page — can be ingested as token-efficient text that the reading, drafting, and review skills already understand. It owns three concrete operations: (1) one-shot conversion of a single file, (2) batch conversion of a directory (e.g. a folder of literature PDFs), and (3) optional AI-enhanced image description for documents whose value is partly visual (PPTX slides, figure-heavy PDFs). It does **not** author new documents, render figures, or run statistics; it is a thin ingestion adapter that maps binary/office content onto the `paper/` workspace's Markdown-first stages.

## Use When

- A co-author, editor, or reviewer delivered a `.docx`/`.pptx`/`.xlsx`/`.pdf` and you need its text/tables in `paper/draft/` markdown or `paper/reviews/ai_review.md` before the literature or reviewer-response skills can read it.
- You are populating `paper/refs/reading_matrix.md` and the source PDFs are not yet in Markdown; run batch conversion to produce clean reading copies alongside `paper/refs/references.bib`.
- A supplementary-data file (XLSX/CSV) from a paper must be turned into a Markdown table that `paper/experiments/statistics.md` or `paper/assets/tables/` can consume.
- A scanned or image-only document (figure screenshots, photographed notes) needs OCR text extraction before `08-markdown-draft` or `11-reference-audit` can quote it.
- You need a quick, dependency-light extraction of a single PDF for triage — faster than the full tex-freeze pipeline — to decide whether a paper belongs in `paper/refs/`.

## Required Inputs

- A source file (PDF, DOCX, PPTX, XLSX, image, audio, HTML, CSV, JSON, XML, ZIP, EPUB) or a directory of such files; for `--use-plugins` or batch runs, a target `--output-dir`.
- Environment dependencies the user must provide: Python with `pip install 'markitdown[all]'` (or per-format extras like `[pdf,docx,pptx,xlsx]`), and `tesseract-ocr` on PATH for OCR of images/scanned PDFs. These are environment dependencies; never hardcode or store credentials.
- **Optional only**: for AI-enhanced image descriptions (`scripts/convert_with_ai.py`), an OpenRouter API key. The user must provide it via the `OPENROUTER_API_KEY` environment variable or `--api-key`; never hardcode or store it, and the conversion still works without any key (LLM descriptions are simply omitted). No key, token, or credential is required for the common batch/literature conversion path.

## Workflow

1. **Classify the source.** Decide single-file vs. directory vs. AI-enhanced. Single-file and directory conversions are offline and dependency-light; AI-enhanced conversion calls the network and costs money, so only reach for it when a document's value is visual (PPTX figures, image-heavy PDFs).
2. **Convert legacy/foreign formats first.** If the source is a `.doc` (legacy Word) or scanned PDF, ensure `tesseract-ocr` and `markitdown[all]` are installed; otherwise basic conversion silently drops unsupported content.
3. **Single file.** `markitdown source.pdf -o paper/draft/source.md` or via the Python API (`md.convert(path).text_content`). Read never mutates the source.
4. **Batch / literature.** Run `python .agent/skills/markitdown/scripts/batch_convert.py --input-dir <pdfs> --output-dir <mds>` (or `convert_literature.py` to add filename-derived metadata headers). Point `--output-dir` at a Markdown-first location so downstream skills can read directly.
5. **AI-enhanced images (optional).** Only when figure description matters: run `python .agent/skills/markitdown/scripts/convert_with_ai.py --input deck.pptx --output paper/draft/deck.md` with `OPENROUTER_API_KEY` set by the user. Prefer `anthropic/claude-opus-4.5`-class vision models for scientific figures. If no key is set, the script converts without image descriptions rather than failing.
6. **Clean and de-duplicate.** Markdown output is already token-efficient, but normalize excessive blank lines (`re.sub(r'\n{3,}', '\n\n', ...)`) before ingesting into long-context stages.
7. **Map outputs to the workspace.** Reading copies go to `paper/draft/` (pre-freeze) or alongside `paper/refs/reading_matrix.md`; extracted reviewer content goes to `paper/reviews/ai_review.md`; tabular data goes to `paper/assets/tables/` or feeds `paper/experiments/statistics.md`. Log every conversion batch in `paper/logs/change_log.md`.

## Output Contract

- Reads never modify the source file; all output is new Markdown written to the agreed `paper/` path.
- A converted reading copy is a single `.md` whose body is the extracted text/tables; the batch/literature variant prepends a small metadata header (`# <stem>`, `**Source**: <file>`).
- Tables from XLSX/CSV land as GitHub-flavored Markdown tables so `paper/experiments/statistics.md` and `paper/assets/tables/` can consume them verbatim.
- Every conversion batch records what was converted (input dir, output dir, file count, any per-file errors) in `paper/logs/change_log.md`; OCR/parse failures are surfaced, not silently dropped.

## Validation

- Run `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only markitdown` to confirm this skill file conforms to the house contract.
- Run `python src/S03_Scripts/validate_project.py` to confirm the repo's paper-workspace invariants still hold after any Markdown artifact is written.
- After conversion, sanity-check one output `.md` (open it; confirm headings/tables render) — a successful parse does not guarantee semantic completeness, especially for scanned PDFs where OCR quality varies.
- Confirm no source file was modified (`git status` on the input path) — ingestion is strictly non-destructive.

## Boundaries

- This skill is an **implementation-only supporting skill**. It is the secondary tool for getting documents into Markdown; the relevant planning/primary skills should be preferred: figure and diagram **generation** belongs to `scientific-visualization` / `scientific-schematics`, classical tabular ML analysis to `scikit-learn`, deep-learning training engineering to `pytorch-lightning`, Bayesian modeling to `pymc`.
- It does **not** author new LaTeX, freeze/formalize `.tex` (that is `09-tex-freeze-formalize`), run experiments, train or infer models, search literature, or polish prose.
- It does not generate schematics; the upstream `generate_schematic*.py` scripts were intentionally **not** ported — use `scientific-schematics` for diagrams.
- It never modifies a source document in place and never stores credentials; the OpenRouter key (when used) lives only in the user's environment for the duration of a conversion.

## Stop With

- Clean Markdown at the agreed `paper/` path (reading copy in `paper/draft/`, reviewer content in `paper/reviews/ai_review.md`, or table in `paper/assets/tables/`), plus an entry in `paper/logs/change_log.md`.
- A clear hand-off note when a source cannot be converted (missing `markitdown`/`tesseract`, corrupt file, unsupported format) rather than shipping a half-extracted Markdown file.
- A pointer to `scientific-visualization` / `scientific-schematics` when the underlying need is to **create** a figure rather than extract one.

## References

- Bundled docs: `references/api_reference.md` (full Python/CLI API), `references/file_formats.md` (per-format notes and optional extras), `assets/example_usage.md` (worked examples). The helper scripts (`batch_convert.py`, `convert_literature.py`, `convert_with_ai.py`) and their purpose/inputs/outputs/network/writes table are documented in `scripts/README.md`.
- Workspace targets: `paper/refs/reading_matrix.md`, `paper/refs/references.bib`, `paper/draft/`, `paper/reviews/ai_review.md`, `paper/assets/tables/`, `paper/experiments/statistics.md`, `paper/logs/change_log.md`.
- Upstream tool: Microsoft MarkItDown — https://github.com/microsoft/markitdown , https://pypi.org/project/markitdown/ .
- Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT); see NOTICE.md and .agent/references/scientific_agent_skills_source.md.
