# Econometrics notebook library

An event-study command can produce a convincing plot while hiding which cohort comparisons identify each point. The same problem appears with clustered inference, shift-share designs, synthetic control, and local projections: the software can run even when the estimand or assignment logic is wrong.

These notebooks are where I work through the estimand, code a small reference version, and simulate a case in which the familiar approach fails.

## Current status

As of 10 August 2026:

- 10 notebooks execute from the repository root;
- 8 numerical tests pass in the repository's own test suite;
- the implementations use simulated data and deterministic seeds;
- no outside researcher has reproduced, used, or reviewed a notebook yet;
- the small implementations omit parts of the inference available in maintained packages.

[STATUS.md](STATUS.md) separates repository checks from outside use.

## Notebooks

| # | Topic | Question | Failure shown |
| --- | --- | --- | --- |
| 00 | [Staggered DiD failure lab](notebooks/00_staggered_did_failure_lab.ipynb) | Why can TWFE be wrong under heterogeneous effects? | Already-treated units contaminate comparisons |
| 01 | [Sun & Abraham](notebooks/01_sun_abraham_event_studies.ipynb) | How are cohort-by-event-time effects aggregated? | Support changes across horizons |
| 02 | [Callaway & Sant'Anna](notebooks/02_callaway_santanna_did.ipynb) | What is ATT(g,t), and who is the control group? | Undefined or invalid comparisons |
| 03 | [Borusyak–Jaravel–Spiess](notebooks/03_borusyak_jaravel_spiess.ipynb) | How is the untreated outcome imputed? | Fitting the counterfactual with treated observations |
| 04 | [Wild-cluster bootstrap](notebooks/04_wild_cluster_bootstrap.ipynb) | What changes with few clusters? | Over-rejection from weak cluster asymptotics |
| 05 | [Conley standard errors](notebooks/05_conley_standard_errors.ipynb) | How can dependence decay with distance? | Arbitrary geographic clusters |
| 06 | [Shift-share designs](notebooks/06_shift_share_designs.ipynb) | Are shares or shocks carrying identification? | Calling a Bartik instrument exogenous without a design argument |
| 07 | [Synthetic control](notebooks/07_synthetic_control.ipynb) | What makes a convex counterfactual credible? | Large post-treatment gaps with poor pre-treatment fit |
| 08 | [Randomization inference](notebooks/08_randomization_inference.ipynb) | Which permutations are allowed by the experiment? | Permuting assignments the design could not have produced |
| 09 | [Local projections](notebooks/09_local_projections.ipynb) | How do horizon regressions recover a response path? | Ignoring dependence from overlapping horizons |

## One reasoning note

[notes/2026-08-10-why-i-dropped-twfe.md](notes/2026-08-10-why-i-dropped-twfe.md) records why I stopped treating a standard TWFE event study as the default for staggered adoption. The key point is that changing the estimator fixes a weighting problem; it does not make treatment timing exogenous.

## Run locally

```bash
git clone https://github.com/layan985/econometrics-notebook-library.git
cd econometrics-notebook-library
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest
python scripts/smoke_run_notebooks.py
```

## What the tests check

The tests check narrow numerical properties: synthetic-control weights remain on the simplex, a stripped-down shift-share identity holds, covariance matrices have the expected shape and sign restrictions, and estimators recover the direction of effects in known-truth simulations.

They do not establish that the identifying assumptions hold in an empirical application. [METHODS_SCOPE.md](METHODS_SCOPE.md) lists what each compact implementation leaves out and points back to the original papers and maintained software.

Code and original notes are released under the MIT License.
