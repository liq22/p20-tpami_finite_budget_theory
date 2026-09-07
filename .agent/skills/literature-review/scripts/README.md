# literature-review scripts (ported)

Optional helper scripts for the literature-review skill. These are convenience
utilities for post-processing search results and verifying citations; the skill
is fully usable by manually screening results and checking DOIs against CrossRef.
These scripts do NOT perform the web/database search itself — search is done with
the available web-search tooling and the result JSON is then fed here.

Two upstream scripts were intentionally NOT ported (`generate_schematic.py`,
`generate_schematic_ai.py`): they generate figures via a remote image model
keyed on `OPENROUTER_API_KEY`, which is out of scope for a literature-review
skill (figure generation belongs to the figure/table-design skills) and would
introduce a secret-bearing network dependency.

## search_databases.py

- **Purpose:** Post-process and aggregate literature search results exported as
  JSON — deduplicate by DOI (title fallback), optionally rank/filter, and emit a
  formatted markdown or JSON summary. Used after you have already collected raw
  result lists from databases/search tools.
- **Inputs:** One JSON file (or several combined into one) of search results.
  Flags: `--deduplicate`, `--rank {citations,date}`, `--year-start`,
  `--year-end`, `--format {markdown,json}`, `--output`, `--summary`.
- **Outputs:** The formatted summary at `--output` (or stdout). Defaults to
  markdown. Writes only the path you give it.
- **Network:** None. Pure local processing of the provided JSON.
- **Writes:** Only the `--output` file. Does not touch `paper/` or any
  repo-tracked path; move the produced summary into `paper/refs/` yourself.
- **Run:** `python .agent/skills/literature-review/scripts/search_databases.py combined_results.json --deduplicate --format markdown --output paper/refs/search_results.md`

## verify_citations.py

- **Purpose:** Extract every DOI from a markdown document, resolve each via
  `https://doi.org/api/handles/...` and `https://api.crossref.org/works/...`,
  and produce a verification report plus formatted citations. This is the
  citation-verification backbone of the skill.
- **Inputs:** A markdown file path (the review draft or `paper/draft/*.md`).
  Reads DOIs out of the document text.
- **Outputs:** A JSON citation report written next to the input
  (`<input>_citation_report.json`) and formatted citations to stdout/file.
- **Network:** Yes — outbound HTTPS to `doi.org` and `api.crossref.org` only.
  No authentication, no API key required. Requires the `requests` package.
- **Writes:** The `<input>_citation_report.json` file beside the input, plus any
  `--output` you specify. Does not modify `paper/refs/references.bib` directly;
  review the report and update the bib by hand or via the writing skill.
- **Run:** `python .agent/skills/literature-review/scripts/verify_citations.py paper/draft/related_work.md`
