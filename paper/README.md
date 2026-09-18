# P20 manuscript

The active source is [draft/main.md](draft/main.md). The current argument asks
when coordinates improve finite-query response explanations after matching
response semantics, information and support-search effects.

- [Literature matrix](refs/LITERATURE_MATRIX.md): 33 original-paper body readings,
  classical foundations and separately identified abstract-only neighbors.
- [Scientific chain](experiments/SCIENTIFIC_CHAIN.md): contributions, comparators,
  actual synthetic evidence and the remaining independent real-data test.
- [Theory](theory/04_COMPARATOR_GEOMETRY_AND_ROUTING.md): fixed-union containment
  and finite-query emulation, complementing the three response-geometry notes.
- [Figure](assets/figures/README.md): editable source and regeneration.

Build a reading PDF with `bash scripts/build_paper.sh build/p20`. This does not
freeze Markdown, change the formal source or authorize submission. Run the
scientific tests with `python -m unittest discover -s src/S04_Tests -v`.
PHMFactory integration, native external benchmarks and faithful SOTA comparisons
remain separate unfinished experiments.
