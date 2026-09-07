---
name: hypothesis-generation
description: Turn one selected research candidate into provenance-aware competing mechanisms, divergent predictions, and one decisive experiment whose possible outcomes can reject or revise the favored explanation.
---

# Hypothesis Generation

## Purpose

Convert one promising idea into a falsifiable scientific question and experiment
without rewriting exploratory or post-hoc explanations as pre-result hypotheses.

## Workflow

1. Fix the selected candidate, current claim at risk, and largest unresolved
   uncertainty.
2. State how the favored hypothesis arose:

   ```text
   H0: proposed before observing the relevant result
   H1: inspired by exploratory evidence
   H2: independently confirmed by new evidence
   H3: still a post-hoc interpretation
   ```

3. Write the favored mechanism and the strongest competing explanation.
4. Derive observations that differ between the hypotheses.
5. Identify the main confound that could mimic the expected result.
6. Design the smallest comparison that controls that confound and can reject the
   favored mechanism.
7. Define before execution what positive, null, contradictory, and boundary
   outcomes would mean for the claim.
8. If no plausible outcome changes the scientific decision, stop rather than
   manufacturing another experiment.
9. State the independent confirmation needed when the hypothesis is H1 or H3 and
   supports a central claim.

## Output Contract

Produce:

- current claim and key uncertainty;
- hypothesis provenance H0/H1/H2/H3;
- favored and competing mechanisms;
- divergent predictions;
- main confound and rejection condition;
- decisive experiment, independent unit, and metric;
- interpretation of positive, null, contradictory, and boundary outcomes;
- independent confirmation requirement, when applicable.

## Boundaries

- Do not require 3–5 hypotheses when two capture the real scientific alternatives.
- Do not require prior-card IDs, taxonomy labels, formal gate scores, or a complete
  experiment suite.
- Do not reopen broad brainstorming after one candidate is selected.
- Do not use Python to enumerate hypotheses or score plausibility.
- Do not relabel an exploratory-inspired or post-hoc hypothesis as pre-result.
- Do not approve the direction, implement code, or run the experiment.
