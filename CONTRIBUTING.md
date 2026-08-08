# Contributing

Contributions should increase econometric depth, not notebook count.

A new method note must contain an explicit estimand, identification assumptions separated from estimation choices, a derivation or score/moment condition, a simulation with known ground truth, a transparent reference implementation where feasible, a failure simulation, a researcher checklist, original scholarly references, and automated numerical tests.

Before opening a PR run:

```bash
pytest
python scripts/smoke_run_notebooks.py
```

In the PR body explain the estimand/design, numerical invariant, failure case, anchoring paper(s), and any deliberate gaps between reference code and production software.

Do not write “here is how to run package X.” Write the econometrics first, then the implementation.
