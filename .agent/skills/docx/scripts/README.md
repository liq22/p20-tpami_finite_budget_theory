# DOCX helper scripts

These local helpers read, unpack, edit, repack, validate, and convert Office files.
Use only the script needed for the actual document task.

```text
accept_changes.py        accept tracked changes through LibreOffice
comment.py               add DOCX comment XML

office/unpack.py        unpack and simplify an Office archive
office/pack.py          repack an edited archive
office/validate.py      check package/XML structure when internals changed
office/soffice.py       run headless LibreOffice with a minimal environment
```

## Usage principle

- Content extraction or creation comes first.
- Run `office/validate.py` only after package/XML-level edits; normal high-level
  document creation needs only an open/render check.
- `office/soffice.py` assumes a normal working LibreOffice installation. It does
  not compile custom sandbox shims or maintain hash files.
- Do not run every helper as a standard pipeline.

The scripts perform no network requests. They write only the explicitly requested
output or unpacked working directory.
