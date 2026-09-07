# Internal Routing Matrix

This is the sole intent → primary mapping used by `00-router`. It is not a host
Skill menu. Repository-wide execution rules remain in `../../AGENTS.md`.

| User intent | Internal primary |
|---|---|
| broad or unclear product task | `00-router` |
| establish current research state | `01-project-brief` |
| generate structural ideas or initialize the core innovation card | `scientific-brainstorming` |
| formalize one selected idea | `hypothesis-generation` |
| choose or revise direction and claim tree | `02-research-question` |
| define evidence-bounded claim strength | `05-claim-evidence` |
| design or simplify a method | `method-design` |
| position literature or revise a competition section | `03-literature-deep-research` |
| produce a broader thematic literature synthesis | `literature-review` |
| implement, fix, refactor, or optimize code | `code-change` |
| explain an existing code subsystem | `code-module-xray` |
| design a claim-testing experiment | `experimental-design` |
| execute an experiment | `06-experiment-ops` |
| analyze collected data | `statistical-analysis` |
| decide sample size or minimum detectable effect | `statistical-power` |
| independently inspect an experiment or method | `07-experiment-audit` |
| pressure-test one claim or explanation | `scientific-critical-thinking` |
| review a manuscript | `peer-review` |
| plan, generate, or revise a figure/table | `15-figure-table-design` |
| draft or restructure a manuscript section | `08-markdown-draft` |
| polish stable language | `10-language-polish` |
| remove defensive framing from stable prose | `10-language-polish` with `anti-defensive-writing` support |
| run an explicit camera-ready language check | `10-language-polish` |
| verify citations | `11-reference-audit` |
| formalize confirmed Markdown into TeX | `09-tex-freeze-formalize` |
| prepare submission files or explicitly inspect readiness | `12-submission-pack` |
| respond to real reviewer comments | `13-reviewer-response` |
| perform a safety-only decision for a concrete high-risk action | `14-agent-safety` |
| improve PaperTrace itself | `repository-self-evolution` |

## Route distinctions

- `scientific-brainstorming` generates alternatives; `hypothesis-generation`
  formalizes one; `02-research-question` decides whether to retain, revise,
  merge, or eliminate it.
- `code-change` modifies executable behavior; `code-module-xray` explains it.
- `experimental-design` specifies a comparison; `06-experiment-ops` runs it;
  `07-experiment-audit` independently inspects it only when explicitly requested.
- `08-markdown-draft` changes scientific reasoning or structure;
  `10-language-polish` changes stable expression without changing meaning.
- `peer-review` identifies manuscript problems; `13-reviewer-response` performs
  the evidence and manuscript changes required by real reviews.
- `12-submission-pack` may inspect readiness only when that inspection is the
  explicit product; it never submits without author authorization.

Primary outputs and forbidden process-only substitutes are defined by each
selected `SKILL.md`, not duplicated here.
