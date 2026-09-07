---
name: repository-self-evolution
description: Adopt one verified upstream improvement only when it makes PaperTrace easier to use or materially improves research, code, experiment, or figure work; avoid new process layers and speculative hardening.
---

# Repository Self Evolution

## Purpose

Apply the smallest useful repository improvement from a verified upstream source
or observed PaperTrace problem.

## Workflow

1. Identify one current user or maintainer problem.
2. Verify the upstream behavior or local evidence relevant to that problem.
3. Prefer modifying an existing rule, skill, adapter, or script over adding a new
   subsystem.
4. Implement the smallest change that improves the real workflow.
5. Run only the affected behavior case or targeted test.
6. Update documentation only when the user action or maintenance procedure changed.

## Output Contract

Produce one concrete repository improvement, its direct user/maintainer benefit,
and one relevant validation result.

## Boundaries

- Do not add a second router, workflow tree, governance layer, dashboard, ledger,
  manifest, receipt, or reviewer role.
- Do not adopt an upstream feature solely because it is new or complex.
- Do not add broad defensive code for hypothetical compatibility states.
- Do not calculate hashes or maintain custom integrity metadata.
- Do not use Python scans as the main evidence that a documentation or skill
  improvement is useful.
