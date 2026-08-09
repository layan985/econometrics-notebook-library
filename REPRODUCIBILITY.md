# Independent Reproduction Protocol

This protocol is designed for a researcher who has not previously run the repository.

## Objective

Reproduce at least one notebook from a clean environment and report the result at an exact repository commit.

## Clean setup

```bash
git clone https://github.com/layan985/econometrics-notebook-library.git
cd econometrics-notebook-library
git rev-parse HEAD
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Record the output of:

```bash
python --version
python -m pip freeze
```

## Baseline checks

```bash
pytest
python scripts/smoke_run_notebooks.py
```

A reproduction is not considered successful merely because installation completes. Record the test result and whether notebook execution completes from repository root.

## Reproduce one method object

Choose one notebook from `notebooks/` and execute it from a clean environment. Preferred first targets are:

- `01_sun_abraham_event_studies.ipynb`
- `02_callaway_santanna_did.ipynb`
- `03_borusyak_jaravel_spiess.ipynb`
- `04_wild_cluster_bootstrap.ipynb`
- `05_conley_standard_errors.ipynb`

If a result differs from the notebook's stated ground truth, report the observed value, expected value, and tolerance rather than silently editing code until it passes.

## Report template

Open a GitHub issue with the title:

`Independent reproduction: <notebook name> — <PASS|FAIL|PASS WITH NOTES>`

Include:

```text
Validator:
Affiliation (optional):
Date:
Commit SHA:
Operating system:
Python version:
Notebook:

pytest result:
Notebook execution result:
Expected numerical result(s):
Observed numerical result(s):

Reproduction status: PASS / FAIL / PASS WITH NOTES

Problems or ambiguities discovered:
Commands executed:
Additional notes:
```

## Interpretation

- **PASS**: clean setup, tests pass, target notebook executes, and stated numerical behavior is reproduced within documented tolerances.
- **PASS WITH NOTES**: reproduction succeeds but the validator finds documentation, dependency, portability, or interpretation issues worth recording.
- **FAIL**: installation, tests, notebook execution, or a stated numerical invariant cannot be reproduced.

A FAIL is not an embarrassment. It is evidence that the validation process found something the author-run workflow did not.
