# scientific-slides — invocation scenarios

Realistic invocations for the single-paper workflow. Each scenario shows the
inputs read from `paper/` and the artifacts written back. Slides are always
derived communication artifacts — they cite only what is in
`paper/refs/references.bib` and show only figures grounded in
`paper/experiments/` and `paper/assets/figures/`.

## Scenario 1: Build a 15-minute conference talk deck in Beamer

Context: the paper has frozen results and finalized figures; the author must
now present at a 15-minute conference slot. Math is central, so Beamer is the
chosen path.

Prompt:
> Read `paper/refs/target_journal.md` for terminology scope, then read
> `paper/experiments/evidence_matrix.md`, `paper/experiments/statistics.md`, and
> `paper/experiments/run_ledger.md` to pick the two core findings and the three
> figures that carry them. Read `paper/refs/references.bib` and
> `paper/refs/reading_matrix.md` and select 4–6 citations for the intro/context
> slides and 3–4 for the discussion comparison. Build a slide-by-slide outline
> (hook → context → gap → approach → results → implications → closure) targeting
> ~16 slides, ~1 slide/minute, with results taking ~40–50% of the time. Then
> implement the deck starting from `assets/beamer_template_conference.tex`,
> adapting only finalized figures from `paper/assets/figures/` (larger labels,
> fewer panels, direct labeling). Cite every claim inline; if a number does not
> trace to `statistics.md` or `run_ledger.md`, flag it into
> `paper/logs/open_questions.md` instead of writing it. Compile to PDF, run
> `scripts/pdf_to_images.py` and a visual review pass, then
> `scripts/validate_presentation.py --duration 15`. Save the `.tex` and `.pdf`
> under `paper/assets/figures/slides/` and log the talk decision into
> `paper/logs/decision_log.md`.

Inputs: `paper/refs/target_journal.md`, `paper/refs/references.bib`,
`paper/refs/reading_matrix.md`, `paper/experiments/evidence_matrix.md`,
`paper/experiments/statistics.md`, `paper/experiments/run_ledger.md`,
`paper/assets/figures/`, `assets/beamer_template_conference.tex`.

Outputs: `paper/assets/figures/slides/talk.tex`, `paper/assets/figures/slides/talk.pdf`,
a slide-by-slide outline + visual-review issue log in the slides staging folder,
gaps appended to `paper/logs/open_questions.md`, talk decision logged to
`paper/logs/decision_log.md`.

## Scenario 2: AI-assisted image-to-PDF deck with visual consistency

Context: a seminar talk for a general scientific audience where visual polish
matters more than editable math; a user-provided OpenRouter key is available.
The author wants one polished slide image per call, assembled into a PDF.

Prompt:
> Define the talk context (45-minute seminar, mixed audience) and write it into
> a planning note. Read `paper/experiments/evidence_matrix.md` and
> `paper/experiments/ablation.md` to choose the core messages, and
> `paper/refs/references.bib` for the citations to surface on intro and
> discussion slides. Plan each slide (title, one main idea, visual element,
> citation). Pick a modern color palette and typography and state it once as a
> FORMATTING GOAL that is repeated in every prompt. Generate the title slide with
> `scripts/generate_slide_image.py`, then each subsequent slide attaching the
> previous slide (for style consistency) and, for results slides, attaching the
> relevant finalized figure from `paper/assets/figures/` so the model
> incorporates real data. Include citations directly in each prompt so they
> render on the slide. Combine the slides with `scripts/slides_to_pdf.py`.
> Rasterize with `scripts/pdf_to_images.py` and run the visual-review workflow
> (overflow, overlap, font ≥18pt, contrast ≥4.5:1); regenerate any failing slide.
> Use the user-provided key only via the `OPENROUTER_API_KEY` env var — never
> hardcode it. Save the final PDF and per-slide images under
> `paper/assets/figures/slides/`.

Inputs: `paper/experiments/evidence_matrix.md`, `paper/experiments/ablation.md`,
`paper/refs/references.bib`, `paper/assets/figures/`, a user-provided
OpenRouter key (out of band).

Outputs: `paper/assets/figures/slides/*.png`, `paper/assets/figures/slides/seminar.pdf`,
a planning note and visual-review issue log, citations verified against
`paper/refs/references.bib`.

## Scenario 3: Convert the paper into a journal-club critique deck

Context: the lab runs a 30-minute journal club on the group's own paper; the
presenter must lead a critical discussion of methods, results, and limitations.

Prompt:
> Read `paper/draft/methods.md` (or `paper/tex/methods.tex`) and
> `paper/experiments/reproducibility.md` to extract the study design and any
> reproducibility caveats, then read `paper/experiments/statistics.md` and
> `paper/experiments/evidence_matrix.md` to identify the strongest and the
> weakest claims. Read `paper/reviews/ai_review.md` for prior critiques already
> recorded, and `paper/logs/open_questions.md` and `paper/logs/dead_ends.md` for
> known limitations. Build a journal-club deck (see
> `references/talk_types_guide.md`): context → methods → results → critical
> analysis, where the critical-analysis slides name specific threats to
> validity and cite comparison studies from `paper/refs/references.bib`.
> Implement in PowerPoint via the pptx skill (editable, so the group can
> annotate). Validate slide count for 30 min and run the visual-review workflow.
> Save under `paper/assets/figures/slides/journal_club.*` and record any new
> critique the deck surfaces into `paper/reviews/ai_review.md` and
> `paper/logs/open_questions.md`.

Inputs: `paper/draft/methods.md` (or `paper/tex/methods.tex`),
`paper/experiments/reproducibility.md`, `paper/experiments/statistics.md`,
`paper/experiments/evidence_matrix.md`, `paper/reviews/ai_review.md`,
`paper/logs/open_questions.md`, `paper/logs/dead_ends.md`,
`paper/refs/references.bib`.

Outputs: `paper/assets/figures/slides/journal_club.pptx`, a critique outline,
new critiques appended to `paper/reviews/ai_review.md` and
`paper/logs/open_questions.md`.
