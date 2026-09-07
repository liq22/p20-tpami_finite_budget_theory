# Internal Agent Scope

The repository-wide authority is `../AGENTS.md`. This file defines only ownership
inside `.agent/`; it does not repeat repository policy.

## Local ownership

| Concern | Authority |
|---|---|
| detailed scientific reasoning | `references/research_first_paper_loop.md` |
| intent → primary mapping | `skills/ROUTING_MATRIX.md` |
| minimum task context | `context_cards.md` |
| Skill inventory | `skills/INDEX.md` |
| current research state | `../paper/paper.yaml -> research_state` |
| one-time project intake | `../paper/kickstart/new_project_intake.yaml` |
| decision history | `../paper/logs/` |

## Host visibility

- `00-router` is the normal host entry.
- `grill-me` is an explicit read-only pressure test.
- Every other Skill and optional ARIS capability remains internal.

For execution, language, validation, safety, and completion rules, follow
`../AGENTS.md`. Add local text here only when it changes ownership within
`.agent/`.
