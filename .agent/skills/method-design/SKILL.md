---
name: method-design
description: Design the smallest method needed to reduce a key scientific uncertainty, starting from an observed failure and competing explanations and ending in a falsifiable comparison, boundary, and implementable specification.
---

# Method Design

## Purpose

Produce a method that is necessary for the research question and simple enough to
understand, implement, falsify, and ablate. Do not fill an architecture template
or add modules for apparent novelty.

## Workflow

1. State the current claim, observed failure or unresolved contradiction, largest
   uncertainty, and the decision the method must change.
2. State the favored mechanism and the strongest competing explanation.
3. Identify the smallest intervention that should change the favored mechanism
   while leaving unrelated factors matched.
4. Define the changed object, assumptions, expected signature, rejection
   signature, and condition under which the advantage should disappear.
5. Before strengthening a theoretical statement:
   - actively search for a counterexample;
   - identify the minimum assumption needed to exclude it;
   - remove assumptions not used by the reasoning;
   - check whether the remaining assumptions hold in the real experiment;
   - derive an observable prediction and failure condition.
6. Add a theoretical result only when the chain closes:

   ```text
   assumptions -> claim -> observable prediction -> experiment
   ```

   Otherwise label the mechanism as analysis, interpretation, hypothesis, or
   empirical observation.
7. Include only components that have:
   - one scientific role;
   - a simpler plausible alternative;
   - a deletion or replacement test;
   - an observable mechanism/property signature.
8. Define the decisive comparison, fair information/budget conditions, primary
   task metric, mechanism metric, boundary test, and possible outcomes.
9. State in advance how each plausible outcome changes the method, theory, claim,
   or boundary. If no outcome changes the decision, do not add the method work.
10. Remove components, fields, wrappers, registries, or configuration layers that
    do not change the scientific decision.
11. Read the final specification once for consistency among failure, mechanism,
    intervention, experiment, counterexample, and claim.

## Output Contract

Produce a concise `method_spec.yaml` and summary containing:

- current claim, key uncertainty, and observed failure;
- favored and competing explanations;
- minimal intervention and changed object;
- minimum assumptions and strongest counterexample;
- testable implication, failure condition, and experiment connection;
- expected, rejection, and boundary signatures;
- minimal components, alternatives, and deletion tests;
- fair decisive comparison, possible outcomes, decisions, and metrics;
- implementation notes only where they affect scientific behavior.

Method readiness is a scientific state, not an approval or documentation state.

## Boundaries

- Do not equate a new module, loss, layer, scale, factory, or registry with a
  scientific contribution.
- Do not add a component without a real failure mode and independent test.
- Do not require prior-card quotas, exhaustive metadata, outcome tables,
  approval-gate strings, or formal completeness with no research value.
- Do not force a theorem when only a mechanism hypothesis is supported.
- Do not preserve unnecessary assumptions merely to make a proposition look
  stronger.
- Do not write code or run experiments unless separately requested.
- Do not use Python to score method quality or validate template fullness.
- Do not add hash, receipt, manifest, provenance-chain, or integrity fields.
- Prefer the simpler method when the complex and minimal versions are
  scientifically equivalent.
