---
name: liteparse
description: 'Implementation tool skill: local layout-aware parsing of PDFs/Office/images via LiteParse (text, bbox JSON, OCR, page PNGs). Use to extract cited text from a methods PDF or batch-ingest a literature folder. Do not use for PDF merge/forms (pdf), EPUB/audio (markitdown), or cloud parsing (LlamaParse). Supporting tool; planning skill preferred.'
---

# LiteParse — local document parsing

## Purpose

This skill is the single source of truth for **local, layout-aware text extraction** in the single-paper workflow. It wraps the LiteParse library (Rust core, Python/Node bindings; the `lit` CLI) and its bundled Tesseract OCR, and treats document work as three operations: parse a file to layout-preserved text, parse it to structured JSON with per-item bounding boxes / font metadata / confidence, and render page screenshots (PNG) for multimodal agents. It does **not** produce Markdown and does **not** call cloud LLMs. It maps onto the paper workspace wherever a PDF or Office source must become searchable text or citable coordinates — pulling text out of a methods/supplement PDF into `paper/refs/`, batch-ingesting a literature folder, grounding a citation with a bounding box, or producing page PNGs a vision reviewer can read. Examples target **liteparse 2.0.0** (the V2 / main branch); the legacy V1 branch is out of scope.

## Use When

- A methods paper, supplement, or protocol arrives as a PDF (or DOCX/image) and its text must be ingested into `paper/refs/reading_matrix.md` or cited in `paper/draft/`.
- You need **bounding boxes** for citation grounding, layout-aware chunking, or joining extracted text with figure regions in `paper/assets/figures/`.
- A scanned PDF or image needs **OCR** (bundled Tesseract, or a user-run HTTP OCR server) before its text is usable.
- A multimodal reviewer or figure-design step needs **page screenshots** (PNG) of a PDF that text extraction alone cannot represent.
- You must **batch-parse** a folder of literature PDFs into a uniform `text`/`json` corpus before building `paper/refs/references.bib` or `paper/experiments/evidence_matrix.md`.
- You need to parse only a page subset (`target_pages`) or a password-protected PDF.

## Required Inputs

- A source file path (or raw PDF bytes) to parse; supported extensions are listed in the Multi-Format Inputs table below.
- **liteparse 2.0.0** installed (`uv pip install "liteparse==2.0.0"`) and the `lit` CLI on PATH; optional **LibreOffice** (`soffice`) for Word/Excel/PowerPoint/OpenDocument inputs and **ImageMagick** (`convert`/`magick`) for image inputs. Install commands live in `references/ocr_and_formats.md`.
- An output location under `paper/` (e.g. `paper/refs/`, `paper/logs/`) — parsed artifacts must land in the workspace, not in scratch dirs.
- For offline OCR, `TESSDATA_PREFIX` pointing at a directory of `.traineddata` files — the user must provide this path; never hardcode or store it. **No API keys, tokens, or cloud credentials are required or accepted** — LiteParse is fully local. Any `OPENROUTER_API_KEY`-style secret a user volunteers is out of scope and must be `<user-provided-key>` if it ever appears.

## Workflow

1. **Pick the parser.** Confirm LiteParse is the right tool against `references/choosing_a_parser.md` (coordinates, fast local parse, page PNGs, or batch PDF corpus → LiteParse; Markdown/EPUB/audio → markitdown; merge/split/forms → pdf skill; dense tables/handwriting at scale → LlamaParse). If a non-LiteParse tool fits, hand off.
2. **Install once.** `uv pip install "liteparse==2.0.0"`; verify with `lit --help` and `python -c "import liteparse; print(liteparse.__version__)"`. Install LibreOffice / ImageMagick only if the input is Office or an image.
3. **Choose the output shape.** Layout-preserved text for full-document reads or chunkers that need no coordinates; structured JSON (`--format json`) for layout-aware RAG, citation grounding, or screenshot+text joins. Field layout is in `references/output_formats.md`.
4. **Parse with sane options.** Add `--no-ocr` on born-digital PDFs (largest speedup), use `target_pages` for methods/supplement sections only, and scale OCR with `num_workers`. Full CLI flags are in `references/cli_reference.md`; the Python/TS API and `search_items` are in `references/api_reference.md`.
5. **OCR and encrypted inputs.** OCR is on by default with bundled Tesseract; set `ocr_language` / `--ocr-language` for non-English, or point at a user-run HTTP OCR server via `--ocr-server-url` (the server is user-provided; never hardcode its URL). For password-protected PDFs pass `password` / `--password` (user-provided; never store).
6. **Screenshots when pixels matter.** `lit screenshot document.pdf --target-pages "1,3,5" -o ./screenshots` (or `parser.screenshot(...)`); combine JSON parse + screenshots when an agent needs both coordinates and pixels for the same pages.
7. **Batch.** For folder-scale jobs use `lit batch-parse ./papers ./parsed --format json --recursive` or the bundled `python scripts/batch_parse_dir.py ./papers ./parsed --format json --recursive` (local only, no network).
8. **Map outputs to the workspace.** Write extracted text/JSON under `paper/` (e.g. parsed methods text into `paper/refs/`, page PNGs into `paper/assets/figures/source_pages/`), update `paper/refs/reading_matrix.md` for newly ingested sources, and record the parse run in `paper/logs/decision_log.md`.

## Output Contract

- Text output is layout-preserved plain text; JSON output is per-page `text_items` each carrying `text`, position (`x`, `y`, `width`, `height`), `font_name`, `font_size`, and optional `confidence` — schema in `references/output_formats.md`.
- Parsing never modifies the source file; it only reads. Batch runs write only to the declared output directory.
- Extracted text destined for the workspace lands in `paper/refs/` (reading matrix, references) or `paper/draft/` markdown; never into ad-hoc scratch paths.
- Page screenshots are PNG files written to the requested directory; when they feed the workspace they go under `paper/assets/figures/source_pages/`.
- Every parse run that ingests a new source records what was parsed and where the artifact lives in `paper/logs/decision_log.md` (and `paper/logs/change_log.md` if it alters an existing artifact).

## Validation

- Run `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only liteparse` to confirm this skill file conforms to the house contract.
- Run `python src/S03_Scripts/validate_project.py` to confirm the repo's paper-workspace invariants still hold after any parsed artifact is written under `paper/`.
- Smoke-test the install before a real parse: `lit --help` and `python -c "import liteparse; print(liteparse.__version__)"` must succeed.
- On a representative source, confirm the chosen output shape is correct: `grep` a known phrase in text output, or load the JSON and assert `len(result.pages) > 0` and `text_items[0]` has non-empty `text` and a valid bbox.
- If OCR was used, eyeball at least one parsed page against the original to confirm OCR quality is sufficient for downstream use; bump `--dpi` or switch `--ocr-language` if not.

## Boundaries

- This is an **implementation / supporting tool skill**. It parses documents only; it does not plan experiments, analyze data, generate figures, or write prose. Prefer the relevant planning skill as primary — plotting/figure design defers to scientific-visualization and `15-figure-table-design`, classical ML analysis to scikit-learn, deep-learning training engineering to pytorch-lightning, Bayesian modeling to pymc.
- It does **not** produce Markdown (use markitdown), merge/split/rotate/watermark/fill forms (use the pdf skill), or handle audio/video/EPUB/HTML.
- It does **not** call any cloud API, read any credentials, or accept secrets; if a task seems to need cloud table/handwriting parsing, defer to LlamaParse (user signs up separately).
- It does not modify source files in place and does not write outside the declared output directory or `paper/`.
- Heavy ML training/inference scripts are not shipped here; only the lightweight, local-only `scripts/batch_parse_dir.py` wrapper is bundled.

## Stop With

- The requested text/JSON/PNG artifact at its declared `paper/` path, plus a `paper/logs/decision_log.md` entry noting what was parsed, the options used, and where the output lives.
- A reading-matrix update (`paper/refs/reading_matrix.md`) when a new source was ingested into the literature set.
- A clear hand-off note when a parse cannot be produced (missing liteparse/LibreOffice/ImageMagick, malformed or encrypted source without a password, or an out-of-scope input that belongs to markitdown / pdf / LlamaParse) rather than shipping a broken artifact.

## References

- Bundled docs: `references/choosing_a_parser.md` (LiteParse vs MarkItDown / pdf / LlamaParse), `references/api_reference.md` (Python/TS API, types, `search_items`), `references/cli_reference.md` (full `lit` flags), `references/output_formats.md` (JSON schema, bboxes, confidence), `references/ocr_and_formats.md` (Tesseract, HTTP OCR, LibreOffice, ImageMagick, `TESSDATA_PREFIX`).
- Bundled script: `scripts/batch_parse_dir.py` with `scripts/README.md` (purpose / inputs / outputs / network / writes).
- Workspace targets: `paper/refs/reading_matrix.md`, `paper/refs/references.bib`, `paper/draft/`, `paper/assets/figures/source_pages/`, `paper/logs/decision_log.md`, `paper/logs/change_log.md`, `paper/experiments/evidence_matrix.md`.
- Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT); see NOTICE.md and `.agent/references/scientific_agent_skills_source.md`.
