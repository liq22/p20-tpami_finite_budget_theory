# research-grants — Invocation Scenarios

Realistic examples of how to call this skill in the single-paper workspace. Each
scenario assumes the research project already has evidence in
`paper/experiments/` and prior work in `paper/refs/`.

## Scenario 1: NIH R01 Specific Aims + Research Strategy

> Context: The lab has pilot data on a new biomarker and is responding to a
> NIH parent R01 announcement. Deadline in 10 weeks.

```
Draft an NIH R01 application for PAR-25-xxx (NIGMS). The project context is in
paper/refs/target_journal.md and our pilot data lives in
paper/experiments/evidence_matrix.md (rows B1-B4) and
paper/assets/figures/pilot_panel.png.

Produce, under paper/draft/:
  1. grant_nih_aims.md — a 1-page Specific Aims page (gap -> long-term goal ->
     central hypothesis -> 3 aims with sub-aims -> payoff).
  2. grant_nih_narrative.md — the 12-page Research Strategy with Significance,
     Innovation, Approach (preliminary data, design/methods, expected outcomes,
     pitfalls/alternatives). Cite only entries already in paper/refs/references.bib.
  3. grant_nih_budget_justification.md — modular budget ($250k/yr increments),
     NIH salary cap applied, 1 month PI effort.

Then run a mock NIH review (Significance/Innov/Approach/Investigator/Environment,
1-9 scale) and log gaps in paper/logs/open_questions.md. Do not invent preliminary
data; flag any unsupported claim.
```

## Scenario 2: NSF CAREER proposal with Broader Impacts

> Context: Early-career PI targeting the NSF CAREER program; needs Intellectual
> Merit + Broader Impacts of equal weight, 15-page Project Description.

```
Draft an NSF CAREER proposal (PAPPG 24-1) for the CISE directorate. Use
paper/refs/reading_matrix.md for the related-work framing and
paper/experiments/evidence_matrix.md for preliminary results.

Write under paper/draft/:
  1. grant_nsf_summary.md — Project Summary with separate Overview, Intellectual
     Merit, and Broader Impacts headings (1 page).
  2. grant_nsf_narrative.md — 15-page Project Description integrating Broader
     Impacts throughout (education, broadening participation, open-source/data
     dissemination) plus a Results from Prior NSF Support section (<=5 pages).
  3. grant_nsf_broader_impacts.md — a concrete, measurable BI plan with timeline
     and assessment metrics (use references/broader_impacts.md).
  4. grant_nsf_timeline.md — 5-year phased Gantt with milestones.

Also generate one optional workflow diagram via scientific-schematics
--doc-type grant into paper/assets/figures/. I have set OPENROUTER_API_KEY in my
environment; never print or store it.
```

## Scenario 3: DARPA BAA technical volume + resubmission response

> Context: Responding to a DARPA BAA after an unfunded first round; needs a
> phase-based technical volume and a point-by-point response to PM feedback.

```
Draft a DARPA technical volume for BAA HR001125Sxxxx (DSO). Prior submission
feedback is in paper/reviews/. Produce under paper/draft/:
  1. grant_darpa_narrative.md — technical challenge, innovation (frame "what if
     we succeed / who cares"), approach, phase-based schedule with go/no-go exit
     criteria, deliverables/metrics, team, risk mitigation.
  2. grant_darpa_budget_justification.md — detailed budget by phase and task.
  3. grant_darpa_timeline.md — quarterly milestones and demonstrations.

Then write a point-by-point response to the prior critiques into
paper/reviews/response_to_reviewers.md and record the diff in
paper/logs/change_log.md. Flag any critique we cannot yet address in
paper/logs/open_questions.md.
```
