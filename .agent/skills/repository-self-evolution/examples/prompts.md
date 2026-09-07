# repository-self-evolution examples

## Scenario 1 — Decide one upstream adoption

User:

```text
Check the latest release of the named reference repository and decide whether one
specific changed pattern should be adopted in PaperTrace. Use official GitHub
files. Return the smallest local target and reason; do not scan every reference
repository and do not edit files.
```

Expected behavior:

- Inspect one named upstream change.
- State its practical PaperTrace effect.
- Choose `reference_only`, `adapt_existing`, `optional_backend`, or `reject`.
- Name one smallest local target.
- Return a concise proposal rather than a repository-wide triage report.

## Scenario 2 — Apply one approved local rule update

User:

```text
Apply the approved update to .agent/references/research_quality_patterns.md.
Use the smallest edit, add a focused test only if behavior changes, and do not add
new skills, workflows, or paper files. Do not create a PR.
```

Expected behavior:

- Read only the approved target and the exact upstream source.
- Apply one bounded change.
- Do not import an external skill tree.
- Do not modify `paper/`.
- Report the direct effect and focused validation.

## Scenario 3 — Review an ARIS pin update

User:

```text
Compare the currently pinned ARIS commit with commit <sha> for the allowlisted
analyze-results and figure-spec capabilities. Update the submodule pin only if the
PaperTrace adapter remains compatible. Do not run ARIS installers, expose ARIS
skills, or enable high-level pipelines.
```

Expected behavior:

- Read `integrations/aris/profile.yaml` and the two selected upstream skills only.
- Check license, paths, helper compatibility, and allowlist boundaries.
- Update the gitlink and profile pin together only after focused checks pass.
- Preserve Core mode, hidden host exposure, and explicit-review boundaries.
- Report compatibility and tests; do not create additional workflow documents.
