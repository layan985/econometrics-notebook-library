# Econometrics Notebook Library

**Research-grade computational notes on modern applied econometrics.**

**Author:** **Layan Oraidi** (also appearing in some award and academic records as **Layan Aloreidi**) · ORCID: https://orcid.org/0009-0005-0202-2582

This is not a beginner tutorial repository. Each notebook follows the same discipline:

> **intuition → estimand → derivation → simulation → implementation → failure mode → research checklist**

The goal is to make modern empirical methods inspectable from first principles rather than hide them behind package calls.

## Library

| # | Notebook | Core question | Failure it is designed to expose |
|---|---|---|---|
| 00 | [Staggered DiD Failure Lab](notebooks/00_staggered_did_failure_lab.ipynb) | Why can a clean TWFE event study be wrong? | Contamination under heterogeneous dynamic effects |
| 01 | [Sun & Abraham](notebooks/01_sun_abraham_event_studies.ipynb) | How do cohort × event-time effects become an IW event study? | Hidden support/composition changes across horizons |
| 02 | [Callaway & Sant'Anna](notebooks/02_callaway_santanna_did.ipynb) | How do we estimate and aggregate ATT(g,t)? | Undefined estimands and invalid control-group choices |
| 03 | [Borusyak–Jaravel–Spiess](notebooks/03_borusyak_jaravel_spiess.ipynb) | How does untreated-outcome imputation identify dynamic effects? | Counterfactual models fit using treated observations |
| 04 | [Wild-cluster bootstrap](notebooks/04_wild_cluster_bootstrap.ipynb) | What changes when cluster asymptotics are weak? | Over-rejection with few/few-treated clusters |
| 05 | [Conley SEs](notebooks/05_conley_standard_errors.ipynb) | How do we allow dependence to decay with distance? | Treating spatial dependence as arbitrary cluster labels |
| 06 | [Shift-share designs](notebooks/06_shift_share_designs.ipynb) | Are shares or shocks carrying identification? | Calling a Bartik instrument exogenous without a design argument |
| 07 | [Synthetic control](notebooks/07_synthetic_control.ipynb) | What is a convex counterfactual and how is it stress-tested? | Dramatic post gaps with poor pre-treatment fit |
| 08 | [Randomization inference](notebooks/08_randomization_inference.ipynb) | What makes a permutation distribution exact? | Permuting labels in ways the original design never allowed |
| 09 | [Local projections](notebooks/09_local_projections.ipynb) | How do horizon-specific regressions recover dynamic responses? | OLS inference with overlapping-horizon residual dependence |

## What makes this different

### Estimands before estimators

Every note starts by defining the causal/statistical object being estimated. Software syntax appears only after the identification and aggregation choices are explicit.

### Transparent implementations with package validation

`econnotes/` contains compact implementations of the main algebra used in the simulations: interaction-weighted event studies, group-time doubly robust scores, null-imposed wild-cluster bootstrap-t, spatial HAC covariance, shift-share/shock-level IV equivalence, simplex-constrained synthetic control, Fisher randomization inference, and Jordà local projections. The BJS notebook is deliberately different: it uses the maintained `did-imputation` package for reported estimates and uncertainty, while reproducing the point-estimator mechanics directly in visible notebook cells.

The stable public API is `econnotes.core`; the implementation is organized internally by method family for inspectability. The compact routines are **reference implementations, not replacements for production econometrics packages** for publication-grade inference.

### Failure simulations

The notebooks are built to make estimators fail in informative ways. A method is not learned until its invalid use case is also reproducible.

### Reproducibility as a first-class object

- deterministic seeds
- source-clean notebooks executed from scratch in CI
- `pytest` numerical invariants
- notebook smoke execution
- GitHub Actions CI
- Quarto website configuration
- MIT license
- machine-readable citation metadata

## Reproduce locally

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

To render the website after installing Quarto:

```bash
quarto render
```

## Numerical tests

The test suite checks identities and design properties rather than only checking that functions run. Examples include:

- region-level shift-share IV equals its shock-level representation in the stripped-down design;
- synthetic-control weights remain on the simplex and reproduce an exact convex combination;
- Conley covariance is symmetric with nonnegative diagonal entries in the simulation;
- randomization inference assigns a larger p-value to the true constant additive sharp null than to a false zero-effect null;
- the maintained BJS Python implementation matches the notebook's visible three-step point-estimator reconstruction to numerical tolerance;
- BJS and Callaway–Sant'Anna simulations recover positive, increasing treatment effects;
- local projections recover the sign and short-horizon magnitude of a known impulse response.

## Scope and implementation policy

The library separates **pedagogical transparency** from **production inference**. Several compact covariance calculations deliberately omit complications that a mature package handles. The notes flag these boundaries explicitly.

For empirical research, use the original authors' or well-vetted community implementations, read their documentation, and validate software defaults against the estimand in the paper.

See [METHODS_SCOPE.md](METHODS_SCOPE.md).

## Core references

- Sun, L. & Abraham, S. (2021). *Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects*. Journal of Econometrics.
- Callaway, B. & Sant'Anna, P. H. C. (2021). *Difference-in-Differences with Multiple Time Periods*. Journal of Econometrics.
- Borusyak, K., Jaravel, X. & Spiess, J. (2024). *Revisiting Event-Study Designs: Robust and Efficient Estimation*. Review of Economic Studies.
- Cameron, A. C., Gelbach, J. B. & Miller, D. L. (2008). *Bootstrap-Based Improvements for Inference with Clustered Errors*. Review of Economics and Statistics.
- Conley, T. G. (1999). *GMM Estimation with Cross Sectional Dependence*. Journal of Econometrics.
- Goldsmith-Pinkham, P., Sorkin, I. & Swift, H. (2020). *Bartik Instruments: What, When, Why, and How*. American Economic Review.
- Borusyak, K., Hull, P. & Jaravel, X. (2022). *Quasi-Experimental Shift-Share Research Designs*. Review of Economic Studies.
- Abadie, A., Diamond, J. & Hainmueller, J. (2010). *Synthetic Control Methods for Comparative Case Studies*. JASA.
- Jordà, Ò. (2005). *Estimation and Inference of Impulse Responses by Local Projections*. American Economic Review.

Full bibliographic metadata is in [`references.bib`](references.bib).

## Extension track

The next release should add de Chaisemartin–D'Haultfœuille DiD, stacked/two-stage DiD, triple differences, regression discontinuity inference, weak-IV diagnostics, leave-one-out shift-share shocks and Rotemberg weights, spatial × serial HAC, LP-IV with joint bands, augmented synthetic control, and sensitivity-analysis notebooks.

## Suggested CV line

> **Creator, Econometrics Notebook Library** — Built an open, tested computational library deriving and simulating modern causal-inference and inference methods, including heterogeneous-treatment DiD/event studies, wild-cluster bootstrap, Conley spatial HAC, shift-share IV, synthetic control, randomization inference, and local projections.

## Researcher

See [`AUTHOR.md`](AUTHOR.md) for the canonical researcher identity and the Oraidi / Aloreidi name bridge used across public research records.

## License

Code and original note text are released under the MIT License. Papers and external materials remain subject to their respective copyright and licenses.
