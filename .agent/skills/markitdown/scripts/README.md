# markitdown/scripts

Bundled helper scripts ported from the upstream markitdown skill. These are
**supporting utilities** for converting office/binary documents into Markdown;
they are not training or inference code. None of them read experiments or
models, and none ship credentials.

| Script | Purpose | Inputs | Outputs | Network | Writes |
|--------|---------|--------|---------|---------|--------|
| `batch_convert.py` | Convert many files in a directory to Markdown in parallel. | `--input-dir`, `--output-dir`, optional `--extensions`, `--workers` | One `.md` per source file in `--output-dir` | No (uses local `markitdown` lib only; no LLM calls) | Writes `.md` files under the given `--output-dir`; never touches inputs |
| `convert_literature.py` | Convert scientific PDFs to Markdown and add lightweight filename-derived metadata, ready for literature review. | `--input-dir` of PDFs, `--output-dir` | Markdown files (with a small metadata header) under `--output-dir` | No | Writes only into `--output-dir` |
| `convert_with_ai.py` | Convert documents with **optional** AI-enhanced image descriptions (e.g. PPTX slide figures). | `--input`, `--output`, `--llm-model`, and an OpenRouter key via `OPENROUTER_API_KEY` env var **or** `--api-key`. **User must provide the key; never hardcode or store it.** | One `.md` file at `--output` | Yes — only when an LLM client is configured; calls OpenRouter (`https://openrouter.ai/api/v1`). No network if `--no-llm`/key omitted. | Writes only the single `--output` file |

Notes:
- The upstream `generate_schematic.py` and `generate_schematic_ai.py` were **not**
  copied: they belong to the `scientific-schematics` skill and require an image
  generation API key. Use `scientific-schematics` as the primary skill for
  diagram/schematic generation.
- All scripts assume `pip install 'markitdown[all]'` (or the per-format extras)
  is available in the environment. They are documentation-grade examples — read
  before running.
