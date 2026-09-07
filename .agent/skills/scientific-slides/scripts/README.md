# scientific-slides/scripts

Helper scripts copied (adapted) from
K-Dense-AI/scientific-agent-skills v2.53.0 (MIT). They are optional utilities —
the skill's main output contract is hand-authored slide content grounded in the
`paper/` workspace; these scripts only automate image/PDF/validation grunt work.

## Per-script summary

| Script | Purpose | Inputs | Outputs | Network | Writes to |
| --- | --- | --- | --- | --- | --- |
| `generate_slide_image.py` | Generate one full slide (or one `--visual-only` figure) as an image via the Nano Banana Pro model. | A prompt string; optional `--attach` reference images. | One PNG (path given by `-o`). | YES — calls OpenRouter image API. | only the `-o` path given by the caller. |
| `generate_slide_image_ai.py` | Same as above with an added AI quality-review/refinement loop. | Prompt string; optional reference images. | One PNG. | YES — OpenRouter. | only the `-o` path. |
| `generate_schematic.py` | Generate a scientific schematic/diagram image from a description. | Prompt string. | One PNG. | YES — OpenRouter. | only the `-o` path. |
| `generate_schematic_ai.py` | Same, with an AI critique + refinement loop (publication-grade diagrams). | Prompt string. | One PNG. | YES — OpenRouter. | only the `-o` path. |
| `slides_to_pdf.py` | Assemble ordered slide images (PNG/JPG) into a single PDF. | One or more image paths or a directory. | One PDF (path given by `-o`). | No. | only the `-o` path. |
| `pdf_to_images.py` | Rasterize a presentation PDF into per-slide images for visual review. | A PDF path. | JPG/PNG images under an output prefix. | No. | the caller-supplied output prefix. |
| `validate_presentation.py` | Check slide count vs. duration, file size, dimensions, font sizes, Beamer compile success. | A PDF/Beamer/PPTX path and `--duration`. | Stdout report. | No. | nothing (read-only check). |

## Authentication

The four `*_ai*` / `generate_*` image scripts require an OpenRouter API key.
The key is **user-provided** — pass it via the `OPENROUTER_API_KEY` environment
variable or the `--api-key` flag. Never hardcode, echo, store, or commit a key.
If a key string is encountered anywhere in the workspace, treat it as
`<user-provided-key>` and scrub it. Get your own key at https://openrouter.ai/keys.

## Usage notes

- These scripts are convenience tooling; the single-paper workflow does not
  require them. Slides may instead be hand-authored in Beamer/PPTX.
- They write **only** to the explicit `-o` / output-prefix paths supplied by the
  caller. Point those paths at a scratch or staging area, not at frozen
  `paper/tex/` artifacts.
- Dependencies (PyMuPDF/`fitz`, Pillow, `requests`) are not vendored; install
  them on demand if you actually run a script.
