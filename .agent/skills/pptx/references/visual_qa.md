# Visual QA for Slides

**Assume there are problems. Your job is to find them.**

Your first render is almost never correct. Approach QA as a bug hunt, not a
confirmation step. If you found zero issues on first inspection, you weren't
looking hard enough.

## USE SUBAGENTS — fresh eyes

**⚠️ USE SUBAGENTS** — even for 2-3 slides. You've been staring at the code and
will see what you expect, not what's there. Subagents have fresh eyes.

The only subagent usage in the rest of this skill (`references/editing.md`) is
for parallel XML editing — that is NOT the same as fresh-eye visual review. For
visual inspection, spin up a separate subagent that has never seen the build
code.

## Convert Slides to Images

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

This creates `slide-01.jpg`, `slide-02.jpg`, etc.

To re-render specific slides after fixes:

```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

## Inspection Prompt

Hand the subagent this prompt plus the rendered images:

```
Visually inspect these slides. Assume there are issues — find them.

Look for:
- Overlapping elements (text through shapes, lines through words, stacked elements)
- Text overflow or cut off at edges/box boundaries
- Decorative lines positioned for single-line text but title wrapped to two lines
- Source citations or footers colliding with content above
- Elements too close (< 0.3" gaps) or cards/sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (e.g., light gray text on cream-colored background)
- Low-contrast icons (e.g., dark icons on dark backgrounds without a contrasting circle)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

For each slide, list issues or areas of concern, even if minor.

Read and analyze these images:
1. /path/to/slide-01.jpg (Expected: [brief description])
2. /path/to/slide-02.jpg (Expected: [brief description])

Report ALL issues found, including minor ones.
```

The 12-point defect taxonomy above is what makes visual QA effective: it forces
specific checks (wrapped-title vs decorative-line collision, footer/source
collisions, low-contrast icons on dark backgrounds without a contrasting circle,
narrow text-box wrapping, etc.) instead of a vague "looks fine" pass.

## Verification Loop

1. Generate slides → Convert to images → Inspect
2. **List issues found** (if none found, look again more critically)
3. Fix issues
4. **Re-verify affected slides** — one fix often creates another problem
5. Repeat until a full pass reveals no new issues

**Do not declare success until you've completed at least one fix-and-verify cycle.**
