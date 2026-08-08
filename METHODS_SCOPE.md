# Methods Scope and Validation Policy

## What the code is

The `econnotes` module is a collection of small, inspectable reference implementations used to expose econometric algebra in simulations. Its primary purpose is to make every notebook auditable.

## What the code is not

It is not a substitute for production packages in published empirical work. In particular:

- the Sun–Abraham notebook uses a never-treated comparison version and a deliberately simple displayed variance aggregation;
- the Callaway–Sant'Anna implementation demonstrates a panel doubly-robust group-time score with a simple nuisance-model setup rather than every estimator/inference option in the authors' package;
- the BJS implementation demonstrates FE counterfactual imputation but not the full production inference machinery;
- the wild-cluster bootstrap is a transparent null-imposed bootstrap-t implementation rather than a comprehensive small-sample package;
- the Conley routine is cross-sectional Euclidean spatial HAC, not a general latitude/longitude panel estimator;
- the shift-share identity is shown in a no-controls/no-intercept form so the shock-level algebra is exact and visible;
- randomization inference currently implements complete random assignment; blocked, paired, and cluster mechanisms should be added as separate functions;
- local projections use HAC standard errors but not simultaneous confidence bands.

## Validation standard

A new notebook is not accepted unless it includes a named estimand, identifying assumptions, derivation, known-truth simulation, executable implementation, failure case, numerical invariant, and original-paper citation.

## Reproducibility rule

Every committed notebook should execute from repository root in a fresh environment using `python scripts/smoke_run_notebooks.py`. CI is expected to fail if a notebook stops executing.
