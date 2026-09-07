# open-notebook — invocation scenarios

Realistic prompts for invoking the open-notebook implementation/tool skill
inside the Auto-01-tiny-research workspace. Each scenario shows the kind of
request that should trigger this skill, the external service it depends on,
and the workspace artifacts it must (and must not) touch. Remember: this skill
drives an **external, user-deployed** Open Notebook server; it is auxiliary to
the repo's own `paper/refs/` system of record.

## Scenario 1: Build a searchable corpus from a heterogeneous reference pile

> I have ~40 sources for the paper — a mix of arXiv PDFs, journal HTML pages,
> two recorded talks, and a few .docx reports — and `paper/refs/references.bib`
> alone can't hold the full text. I've deployed Open Notebook at
> `OPEN_NOTEBOOK_URL`. Stand up a notebook scoped to this paper's research
> question, ingest all 40 sources, and let me ask synthesis questions with
> citations before I promote curated entries into `paper/refs/`.

This triggers open-notebook: the user has a deployed server and wants to build
a multi-format, searchable external corpus as a precursor to curating
`paper/refs/`. The skill creates a notebook (recording its ID and purpose in
`paper/logs/decision_log.md`), ingests URLs/PDFs/audio/docx via
`/api/sources` (see `scripts/source_ingestion.py`), waits for full-text + vector
indexing, and exposes `/api/search` for cited synthesis queries. **Outputs**:
a decision-log entry naming the notebook; optional synthesis notes copied into
`paper/experiments/insights.md` and `paper/logs/open_questions.md`, each with
provenance (notebook ID + source ID). **Do NOT** let the notebook become the
canonical reference list — every source kept for the paper must also be entered
into `paper/refs/references.bib` via `citation-management`. **Do NOT** write
into `paper/tex/` or `paper/submission/`. If `OPEN_NOTEBOOK_URL` is not
provided or the server is unreachable and the user won't deploy it, stop.

## Scenario 2: Answer a reviewer synthesis question with cited chat

> Reviewer 2 asks "how does the field's evidence on X compare across the
> studies in your corpus?" (`paper/reviews/response_to_reviewers.md`,
> comment R-04). I already have the Open Notebook corpus from Scenario 1.
> Use context-aware chat over the full source set to draft a cited synthesis
> I can adapt into the response-to-reviewers.

This triggers open-notebook: the request is a context-aware synthesis over an
external corpus with per-source citations — exactly what `/api/chat/execute`
(with `include_sources: true`) provides (see `scripts/chat_interaction.py`).
The skill opens a chat session on the existing notebook, runs the reviewer's
question, and returns an answer with source citations. **Outputs**: a draft
synthesis passage placed into `paper/reviews/response_to_reviewers.md` under
R-04, plus a reproducibility note in `paper/experiments/reproducibility.md`
recording the AI provider/model id and date used (since this text will appear
in the paper). **Do NOT** paste AI text into the paper without a human
checking the cited sources — if a citation cannot be tied to a concrete source
in the notebook (and ideally in `paper/refs/references.bib`), flag it in
`paper/logs/open_questions.md` rather than asserting it. **Do NOT** use this
skill for the statistical/methodological substance of the rebuttal (use
`statistical-analysis` / `scikit-learn` / `pymc` as appropriate); open-notebook
only supplies the literature-synthesis layer.
