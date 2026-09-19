# Fixed-response comparators

The `p19` path is retained from the requested experiment layout; these modules
belong to P20 and do not import the independent P19 paper. `comparators.py` owns
frozen-basis and union comparisons; `toy.py` owns the controlled nonlinear study;
`plot_motivation.py` owns the motivation diagram. Shared-basis learning remains
in `src/S01_Package/response_basis.py` with its existing direct runner.

```bash
python -m unittest discover -s src/S04_Tests -v
python experiments/p19/toy.py --output results/paired_control
python experiments/p19/plot_motivation.py --summary results/paired_control/toy_summary.json
bash scripts/build_paper.sh build/p20
```

Do not use test-candidate hindsight minima as unbiased population headroom.
The context-matched union is an exact emulation control, not a newly optimized
competitor. Plain union-OMP and routed OMP receive the same responses but impose
different support search. Their difference does not establish a class advantage.
