# NOTICE — Third-Party Attribution

PaperTrace adapts or integrates material from public projects. This file records what was reused and where the corresponding licenses live. It does not maintain local file hashes or integrity proofs.

## Adapted scientific capabilities

PaperTrace adapts selected capability skills from:

- Repository: `K-Dense-AI/scientific-agent-skills`
- Upstream license: MIT
- Pinned release: `v2.53.0`
- Pinned commit: `9c9bd2e92af12311ecd0c1a643e0931643f9ea04`
- Port date: 2026-07-02

Local descriptions are narrowed to PaperTrace use cases, outputs are mapped to the single-paper workspace, and bundled assets are retained only when they serve a current local capability. Provenance details are recorded in `.agent/references/scientific_agent_skills_source.md`.

Individual upstream skills may declare MIT, BSD-3-Clause, Apache-2.0, Matplotlib, Polars, or bundled document-tool license terms. Review the corresponding local license files before redistribution.

## Adapted `grill-me` interaction

PaperTrace adapts the one-question-at-a-time interaction pattern from:

- Repository: `mattpocock/skills`
- Upstream license: MIT
- Copyright: Copyright (c) 2026 Matt Pocock
- Pinned commit: `391a2701dd948f94f56a39f7533f8eea9a859c87`
- Upstream sources: `skills/productivity/grill-me/SKILL.md` and `skills/productivity/grilling/SKILL.md`

Local files:

```text
.agent/skills/grill-me/SKILL.md
.agent/skills/grill-me/evals/
.agent/skills/grill-me/LICENSE.txt
```

The local version is explicit, read-only, one-question-per-turn, and does not implement the resulting plan.

## Adapted anti-defensive writing support

PaperTrace adapts evidence-bounded anti-defensive revision from:

- Repository: `Kiterlin/anti-defensive-writing`
- Upstream license: MIT
- Copyright: Copyright (c) 2026 Kiterlin
- Pinned commit: `60ff7d1c2695d9b56ed5593bed1b02a3ab744cd7`
- Port date: 2026-08-30
- Upstream source: `SKILL.md`

Local files:

```text
.agent/skills/anti-defensive-writing/SKILL.md
.agent/skills/anti-defensive-writing/LICENSE.txt
.agent/skills/10-language-polish/SKILL.md
```

The local version is internal support for `10-language-polish`. It removes rhetorically empty caveats and imagined-reviewer rebuttals while preserving evidence strength, uncertainty, scope, limitations, numbers, citations, and technical meaning. It does not add a host entry, global word blacklist, prose scanner, or style score.

## Writing and onboarding inspiration

PaperTrace references `Leey21/awesome-ai-research-writing` as a public example of practical academic-writing onboarding. No prompt library is copied verbatim, and this reference does not define PaperTrace behavior.

## Optional ARIS execution backend

PaperTrace optionally includes ARIS as a Git submodule:

- Project: Auto-claude-code-research-in-sleep (ARIS)
- Upstream: `wanshuiyin/Auto-claude-code-research-in-sleep`
- Upstream license: MIT
- Copyright: Copyright (c) 2026 wanshuiyin
- Submodule path: `external/aris`
- Pinned commit: `3e49e63aae6a653067f9e2101d50457f1f7d6a2f`

The commit is a dependency version pin, not a second integrity system. PaperTrace does not copy ARIS skills into its canonical tree and does not install ARIS skills as direct Claude or Codex entrypoints.

Integration files:

```text
integrations/aris/profile.yaml
integrations/aris/adapter.py
integrations/aris/README.md
integrations/aris/NOTICE.md
```

After initialization, the full ARIS license is available at `external/aris/LICENSE`.

## Warranty

All upstream and referenced content is provided as is, without warranty. PaperTrace preserves attribution but does not imply endorsement, affiliation, or a guarantee of research quality or publication outcome.
