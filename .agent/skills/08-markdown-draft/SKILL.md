---
name: 08-markdown-draft
description: Draft or revise one manuscript section from verified scientific content while preserving claims, mechanisms, examples, sources, and boundaries and keeping repository/process language outside the paper.
---

# 08 Markdown Draft

## Purpose

Write the requested section itself. A manuscript revision may improve scientific
logic, but it must not silently delete unique content or translate internal
workflow language into academic prose.

## Workflow

1. Fix the editing mode before changing text:
   - **scientific revision** may change claims, structure, mechanisms, or
     boundaries when results/sources justify it;
   - **language revision** changes expression only;
   - **compression** runs only when explicitly requested and must preserve or
     disclose every removed scientific element.
2. Before a broad rewrite, identify internally the section's scientific atoms:

   ```text
   claim / definition / mechanism / assumption
   empirical finding / engineering example / boundary / citation
   equation / number / terminology
   ```

3. Confirm the content basis: verified sources, actual method/implementation,
   completed results and uncertainty, and explicitly unresolved hypotheses.
4. Repair argument order before sentence editing. Use the domain's concrete
   objects and operations rather than generic control vocabulary.
5. Draft full prose with fact, inference, exploratory interpretation, and
   hypothesis at visibly different strengths.
6. Apply section-specific logic:
   - Introduction: real problem, current capability, specific unresolved issue,
     scientific insight, supported contribution;
   - Related Work: assumptions, mechanisms, results, limitations, and relation to
     the present question;
   - Methods: problem, assumptions, mechanism, formulation, algorithm, essential
     implementation;
   - Results: question, observation, quantitative result, interpretation and
     remaining uncertainty;
   - Discussion: mechanism, conditions, failures, alternatives, literature and
     implication;
   - Abstract: problem, gap, scope/idea, main findings, implication;
   - Conclusion: bounded knowledge gained.
7. Move search/coding dates, dynamic corpus counts, source-status categories,
   repository paths, promotion rules, and other process detail to Review Methods
   or supplementary material when methodologically necessary. Do not put them in
   the Abstract or headline contribution.
8. Prefer the actual PHM/scientific noun—measurement, diagnostic indicator,
   fault hypothesis, prognostic estimate, uncertainty interval, source support,
   field outcome—over repeated generic words such as `evidence`, `object`,
   `witness`, `lens`, `handoff`, or `authority` when a more precise term exists.
9. Compare the revision with the original. If a claim, mechanism, example,
   equation, number, citation, or boundary was removed or changed, state that
   change separately rather than hiding it as polish.
10. Verify only changed facts, numbers, equations, citations, and conclusions.

## Output Contract

Produce the revised manuscript section in natural, domain-native academic
language. For scientific revision or explicit compression, also provide a short
list of any substantive elements removed, moved, weakened, or added. For pure
language revision, the scientific content set must remain unchanged.

## Boundaries

- Do not replace section revision with a plan, paragraph inventory, checklist,
  audit report, or formatting pass.
- Do not silently remove a unique claim, mechanism, assumption, example,
  citation, negative result, or limitation to make prose shorter.
- Do not turn repository/coding state into a scientific finding. Abstracts do not
  report snapshot dates, record counts, internal statuses, paths, gates, ledgers,
  review workflow, or validation procedure unless the study's actual method
  makes one detail indispensable—and then it belongs primarily in Methods.
- Do not globally replace `evidence` or another word; identify the intended
  scientific object sentence by sentence.
- Do not insert factories, managers, registries, caches, hashes, manifests, or
  logging infrastructure into Methods unless they are the research object.
- Internal IDs, paths, statuses, gates, ledgers, backends, and Agent execution
  language stay outside manuscript prose and captions.
- Python prose scoring, heading counts, and ordinary Markdown scans are outside
  this skill.
