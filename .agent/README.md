# PaperTrace Agent System

This directory contains the internal Router, Skills, context limits, references,
evaluation definitions, and validation scripts.

## Directory map

| Need | Source |
|---|---|
| repository-wide behavior | `../AGENTS.md` |
| `.agent/` ownership and visibility | `AGENTS.md` |
| task → primary route | `skills/ROUTING_MATRIX.md` |
| files to read for a task | `context_cards.md` |
| Skill inventory | `skills/INDEX.md` |
| detailed research loop | `references/research_first_paper_loop.md` |
| evaluation scope and limitations | `evals/README.md` |

Only `00-router` and explicit `grill-me` are host-visible. Other Skills and ARIS
capabilities are internal.

Setup and final validation commands live in the root `README.md`; do not maintain
a second command list here.
