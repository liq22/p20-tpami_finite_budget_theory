# PaperTrace Idea Innovation Patterns

This is an optional design reference. It is not manuscript evidence, a required
candidate taxonomy, a promotion gate, or proof of novelty.

## Use

1. Start from the observed failure, contradiction, or unresolved boundary.
2. Use one or two applicable lenses only when they reveal a genuinely different
   changed research object or mechanism.
3. Assign a label only after the core before → after transformation is clear.
   Omit the label when it does not help the decision.
4. Stop when another candidate repeats an existing core mechanism.
5. Verify the closest prior and design a discriminating test; pattern membership
   provides neither novelty nor support.

## Five optional meta-patterns

| ID | Search lens | Core move |
|---|---|---|
| `M1` | Assumption and boundary reconstruction | Replace an invalid assumption, redefine the problem, or characterize and cross a limit |
| `M2` | Representation, operator, and optimization transformation | Change the primitive, operator, shared space, equivalence class, or search geometry |
| `M3` | Structural and supervisory internalization | Guarantee a property by construction or create supervision for a named property |
| `M4` | Mechanism decomposition and specialized solving | Decompose identifiable heterogeneity or assign typed subproblems to specialized solvers |
| `M5` | Dynamic mechanism reconstruction and diagnosis | Make a fixed mechanism conditional or isolate its contribution from confounders |

## Optional detailed lenses

| ID | Core move | Minimum distinguishing evidence | Common false positive |
|---|---|---|---|
| `P01` | Audit and replace a core assumption | Old assumption, counterexample, weaker replacement, changed validity | Generic robustness augmentation |
| `P02` | Reframe as a solvable object | Formal object, mapping, operational variables, proof/evaluation interface | Renaming a standard task |
| `P03` | Characterize and surpass a limit | Bound and conditions, limiting mechanism, boundary-targeted test | Average improvement only |
| `P04` | Substitute operator or representation | Defect of old primitive, independent new primitive, primitive-level test | Swapping a standard layer |
| `P05` | Unify heterogeneous inputs in one space | Shared geometry or semantics and preserved relations | Concatenation or resampling |
| `P06` | Prove an equivalence | Explicit mappings, validity conditions, new prediction or algorithm | Calling methods similar |
| `P07` | Relax discrete search | Original objective, controlled relaxation, valid recovery | Unchecked differentiable surrogate |
| `P08` | Encode structure by construction | Named property, architectural guarantee, soft-constraint comparison | Adding a penalty |
| `P09` | Create supervisory signal | Signal source, bias/noise analysis, mechanism link | Ordinary pseudo-labelling |
| `P10` | Target a property with a pretext objective | Named property, objective link, property metric, generic baseline | Changing a pretext hyperparameter |
| `P11` | Decompose for differentiated treatment | Interpretable split, conflicting needs, reliable routing, matched comparison | Arbitrary clustering |
| `P12` | Delegate typed subproblems | Subproblem types, solver rule, interfaces, error ownership | Multi-agent voting |
| `P13` | Liberate a fixed generative component | Fixed bottleneck, adaptive parameterization, stability or identifiability | Making one scalar trainable |
| `P14` | Adapt by conditioning | Meaningful condition, fixed base model, unseen-condition test | Frozen backbone plus ordinary head |
| `P15` | Isolate a mechanism from confounders | Matched on/off test, negative control, failure signature | Unmatched ablation |

## Candidate minimum

A candidate needs only:

```text
research object
before → after
mechanism sketch
observable prediction
rejection condition
closest-neighbour delta or unresolved search question
bounded kill test
claim boundary
decision
```

Keep no more than four mechanism-distinct candidates. One or zero is valid when
the evidence does not support a broader search. Only one provisional
front-runner is formalized, with one strongest competing explanation and one
decisive test.

Author approval is recorded only in `paper/paper.yaml -> idea_selection`.
