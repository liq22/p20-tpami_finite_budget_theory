# PPTX helper scripts

Use these local helpers only when they directly create or repair the requested
PowerPoint file.

```text
clean.py                 remove unreferenced package parts when needed
add_slide.py             add or duplicate a slide in an unpacked deck
thumbnail.py             create a quick template/contact-sheet view
office/unpack.py         unpack an Office archive
office/pack.py           repack an edited archive
office/validate.py       check package/XML structure after low-level edits
office/soffice.py        run headless LibreOffice with a minimal environment
```

## Usage principle

- Establish slide content and story before low-level package work.
- Prefer normal deck creation/editing over unpacking XML.
- Use `office/validate.py` only after package/XML edits.
- Render or open the affected slides once; do not run repeated visual-review loops
  without a concrete defect.
- `office/soffice.py` assumes a normal working LibreOffice installation. It does
  not compile custom sandbox shims or maintain hash files.
- Do not run every helper as a standard pipeline.

The scripts make no network requests and write only the requested output or
explicit unpacked working directory.
