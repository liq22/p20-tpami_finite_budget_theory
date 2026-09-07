# docx — example invocation scenarios

Realistic, single-paper-workflow prompts that should trigger this skill. Each
ends with the `paper/` artifact the skill is expected to produce or update.

## Scenario 1: Build the journal cover letter as a Word file

The target venue in `paper/refs/target_journal.md` requires the cover letter as
a `.docx`. The user asks:

> "The editor wants our cover letter as a Word document. Take
> `paper/submission/cover_letter.md`, format it as US Letter with one-inch
> margins, Arial 11, and our letterhead, and write
> `paper/submission/cover_letter.docx`. Then validate it."

Expected actions: read the markdown source and `target_journal.md` formatting
constraints; build the document with `docx-js` (explicit page size 12240 × 15840
DXA, overridden `Heading1/2` styles, tab-stop letterhead, `PageNumber` footer);
run `python scripts/office/validate.py paper/submission/cover_letter.docx`; log
the new artifact in `paper/logs/change_log.md`.

## Scenario 2: Read a reviewer's tracked-changes Word file into the review log

A reviewer returned the manuscript as a `.docx` full of tracked changes and
comments. The user asks:

> "The reviewer sent back `manuscript_review.docx` with tracked changes. Pull
> the text and all their comments into `paper/reviews/ai_review.md` so we can
> plan the response, and don't modify the original."

Expected actions: extract text with `pandoc --track-changes=all
manuscript_review.docx -o /tmp/review.md`; unpack with `python
scripts/office/unpack.py manuscript_review.docx unpacked/` to read
`word/comments.xml`; consolidate reviewer comments and edits into
`paper/reviews/ai_review.md`; leave the source `.docx` untouched.

## Scenario 3: Produce the response-to-reviewers as a Word document

During the reviewer-response stage the user asks:

> "Generate `paper/reviews/response_to_reviewers.docx` from
> `paper/reviews/response_to_reviewers.md` — point-by-point, each reviewer
> comment as a numbered item, our reply in bold underneath. Acceptable for
> journal upload."

Expected actions: build the `.docx` with `docx-js` using `LevelFormat.DECIMAL`
numbering for reviewer comments, bold `TextRun` replies, dual-width tables where
a table is used, and the venue's page size from `target_journal.md`; validate
with `scripts/office/validate.py`; confirm via a `soffice → pdftoppm` render
that numbering and bold render correctly; update `paper/logs/change_log.md`.

## Scenario 4: Insert a finalized figure into a collaborator's Word draft

A co-author maintains the draft as `.docx` (not LaTeX). The user asks:

> "Drop the final version of `paper/assets/figures/fig1_ablation.png` into
> `paper/draft/collab_draft.docx` at the 'Results' section, captioned
> 'Figure 1: Ablation over learning rate.' Track the insertion as author
> 'Claude' and don't touch anything else."

Expected actions: copy the draft to a working file; `python
scripts/office/unpack.py collab_draft.docx unpacked/`; add the image to
`word/media/`, register the relationship and content type, and insert a
`<w:drawing>` block wrapped in a tracked-change `<w:ins w:author="Claude">`;
repack with `python scripts/office/pack.py unpacked/
paper/draft/collab_draft.docx --original collab_draft.docx`; validate; log the
edit in `paper/logs/change_log.md`.
