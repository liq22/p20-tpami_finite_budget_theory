# citation-management — bundled scripts

These scripts are copied (adapted) from
`K-Dense-AI/scientific-agent-skills` (MIT) and live under
`.agent/skills/citation-management/scripts/`. They are reference implementations
of the workflow described in `SKILL.md`; prefer running them inside a dry-run
and confirming writes before touching `paper/refs/references.bib`.

## Inventory

| Script | Purpose | Inputs | Outputs | Network | Writes |
|---|---|---|---|---|---|
| `doi_to_bibtex.py` | Convert one or more DOIs to a BibTeX entry via CrossRef. | DOI(s) on CLI or `--input file` (one DOI per line). | BibTeX to stdout or `--output file`. | Yes — CrossRef `api.crossref.org`. | Only if `--output` is given. |
| `extract_metadata.py` | Extract full metadata from DOI / PMID / arXiv ID / URL. | `--doi`, `--pmid`, `--arxiv`, `--url`, or `--input file`. | BibTeX/JSON/YAML to stdout or `--output file`. | Yes — CrossRef, NCBI E-utilities, arXiv, DataCite. | Only if `--output` is given. |
| `search_pubmed.py` | Search PubMed via NCBI E-utilities. | Query string (MeSH, field tags, Boolean). | JSON or BibTeX to stdout or `--output file`. | Yes — NCBI E-utilities. | Only if `--output` is given. |
| `search_google_scholar.py` | Search Google Scholar. Needs `scholarly` lib. | Query string, year filters, `--sort-by`. | JSON or BibTeX to stdout or `--output file`. | Yes — Google Scholar (rate-limited; may be blocked). | Only if `--output` is given. |
| `format_bibtex.py` | Format, sort, deduplicate, and validate BibTeX syntax. | `references.bib`. | Formatted BibTeX to stdout or `--output file`; optional `--report`. | No (purely local). | Only if `--output`/`--report` given. |
| `validate_citations.py` | Validate accuracy, completeness, duplicates, venue citation-count standards, and manuscript↔bib cross-check. | `references.bib`; optional `--manuscript paper.md`. | JSON report to stdout or `--report file`; optional `--output` auto-fixed BibTeX. | Yes — DOI resolution via doi.org and CrossRef (when checking DOIs). | Only if `--output`/`--report` given. |

## Notes

- Two upstream scripts were intentionally NOT copied: `generate_schematic.py`
  and `generate_schematic_ai.py`. They belong to a separate
  `scientific-schematics` skill scope, require an `OPENROUTER_API_KEY`, and are
  out of scope for citation management.
- Any API key (e.g. an OpenRouter key for an LLM-assisted step, or
  `NCBI_API_KEY` / `NCBI_EMAIL` for higher E-utilities rate limits) is
  **user-provided out of band**; never hardcode, echo, or persist a key, token,
  or credential in these scripts, this directory, or any workspace file. Treat
  any encountered key string as `<user-provided-key>`.
- Scripts that hit the network can be slow or rate-limited; run searches in
  small batches and cache results into `paper/refs/` rather than re-querying.
- Inputs from the workspace: identifiers/queries come from
  `paper/refs/reading_matrix.md`; canonical output target is
  `paper/refs/references.bib`.
