# liteparse — example invocation scenarios

Realistic, single-paper-workflow prompts that should trigger this skill. Each
ends with the `paper/` artifact the skill is expected to produce or update.

## Scenario 1: Ingest a methods PDF into the reading matrix

The core method you are critiquing is described in a 30-page PDF that the user
just dropped into the repo. The user asks:

> "Pull the text out of `smith_2024_methods.pdf` so I can add it to the reading
> matrix. It's a born-digital PDF, so skip OCR for speed. Put the parsed text
> somewhere under `paper/refs/` and note it in the decision log."

Expected actions: confirm LiteParse is the right tool over markitdown/pdf
(`references/choosing_a_parser.md`); `uv pip install "liteparse==2.0.0"` if
needed; `lit parse smith_2024_methods.pdf --no-ocr -o
paper/refs/parsed/smith_2024_methods.txt`; add a row to
`paper/refs/reading_matrix.md`; record the parse in
`paper/logs/decision_log.md` (file, `--no-ocr`, output path).

## Scenario 2: Batch-parse a literature folder into JSON for citation grounding

The user has a folder of 40 supplementary PDFs and wants bounding-box JSON so
later citations can be grounded to exact page regions. The user asks:

> "Batch-parse everything in `./literature/` to JSON with bounding boxes,
> recursively, and drop it under `paper/refs/parsed/`. We'll use the bboxes to
> ground citations later."

Expected actions: `lit batch-parse ./literature paper/refs/parsed --format json
--recursive` (or `python scripts/batch_parse_dir.py ./literature
paper/refs/parsed --format json --recursive`); spot-check one JSON file to
confirm `pages[].text_items[]` carry non-empty `text` and valid bboxes (per
`references/output_formats.md`); note the corpus location in
`paper/logs/decision_log.md` and update `paper/refs/reading_matrix.md` for the
newly available sources.

## Scenario 3: Render figure pages as PNG for a multimodal reviewer

A figure in the source paper is too complex for text extraction to capture, and
the reviewer agent needs to actually see the page. The user asks:

> "Give me PNG renders of pages 4 and 5 of `smith_2024_methods.pdf` at 150 DPI
> so the reviewer can look at the figures. Put them under
> `paper/assets/figures/source_pages/`."

Expected actions: `lit screenshot smith_2024_methods.pdf --target-pages "4,5"
--dpi 150 -o paper/assets/figures/source_pages/`; confirm the two PNGs exist
and are non-empty; record the render in `paper/logs/decision_log.md`.

## Scenario 4: OCR a scanned protocol PDF

A lab protocol arrives as a low-quality scanned PDF. The user asks:

> "This `protocol_scan.pdf` is scanned and OCR is picking up garbage. Parse it
> to text with French OCR and higher DPI, output under `paper/refs/parsed/`."

Expected actions: `lit parse protocol_scan.pdf --ocr-language fra --dpi 300 -o
paper/refs/parsed/protocol_scan.txt`; eyeball the first page against the
original to confirm OCR quality is now sufficient (bump DPI further or point at
a user-run `--ocr-server-url` if not); record options and output path in
`paper/logs/decision_log.md`.
