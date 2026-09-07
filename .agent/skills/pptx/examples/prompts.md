# pptx — invocation scenarios

Realistic prompts for invoking the pptx skill inside the Auto-01-tiny-research
workspace. Each scenario shows the kind of request that should trigger this
skill and the workspace artifacts it produces or reads.

## Scenario 1: Conference talk deck from the accepted paper

> The paper was accepted at the venue in `paper/refs/target_journal.md`. Build a
> 12-minute conference talk deck: title slide with the headline result, a
> motivation/problem slide, 2 method slides, 3 results slides reusing the figures
> in `paper/assets/figures/` (especially the main result and the ablation), a
> limitations slide drawn from `paper/experiments/evidence_matrix.md`, and a
> takeaways slide. Keep every on-slide number consistent with
> `paper/experiments/statistics.md`. Save the `.pptx` and a rendered PDF into
> `paper/submission/talk/`.

This triggers pptx because a slide deck must be created from existing paper
content. With no template supplied, the skill uses the PptxGenJS from-scratch
path (`references/pptxgenjs.md`): it pulls the headline claim and figures from
`paper/experiments/evidence_matrix.md` and `paper/assets/figures/`, picks a
content-informed palette and varied per-slide layouts, runs content QA with
`markitdown`, renders slides to JPEG for visual QA (fix-and-verify cycle), and
writes the deck plus PDF preview to `paper/submission/talk/`, logging the build
in `paper/logs/change_log.md`. Figure rendering itself defers to
`matplotlib`/`scientific-visualization`; this skill only composes them onto
slides.

## Scenario 2: Adapting a group-provided template for a seminar

> My group gave me their standard seminar template (`seminar_template.pptx`).
> Make a 20-slide deck for my project: keep their title and section-divider
> layouts, fill in my problem, method, results, and next-steps from
> `paper/draft/`, embed the two figures under `paper/assets/figures/`, and
> re-style the accent color to match the paper's figure palette. Do not leave any
> placeholder text behind.

This triggers pptx because an existing template must be adapted, which is the
templated XML workflow in `references/editing.md`. The skill analyzes the
template with `scripts/thumbnail.py` and `markitdown`, plans a varied slide
mapping (not the same layout each slide), unpacks with
`scripts/office/unpack.py`, duplicates/reorders slides with
`scripts/add_slide.py`, edits each `slide{N}.xml` with the Edit tool, cleans
orphaned media with `scripts/clean.py`, repacks with
`scripts/office/pack.py`, then greps `markitdown` output for leftover
placeholders and renders slides to images for visual QA before writing the final
deck into `paper/submission/talk/`.

## Scenario 3: Summarizing a collaborator's slide deck into the review file

> A collaborator sent `collab_update.pptx` summarizing related work they want
> cited. Read it, extract the key claims and any numbers, and append a concise
> summary plus citation candidates to `paper/reviews/ai_review.md` and propose
> new entries for `paper/refs/references.bib`.

This triggers pptx because a `.pptx` is the input and its content must be
extracted. The skill uses `python -m markitdown collab_update.pptx` (and
`scripts/thumbnail.py` for a visual overview) to read the deck, then maps the
extracted claims into `paper/reviews/ai_review.md` and proposes BibTeX entries
for `paper/refs/references.bib`, flagging any number that lacks a traceable
source. It does not edit the collaborator's deck; it only reads and summarizes,
handing citation correctness off to `citation-management`.
