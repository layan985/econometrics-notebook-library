# Portfolio case study — Econometrics Notebook Library

> Modern causal methods learned through estimands, derivations, simulations and reproducible failure cases.

[Portfolio](https://layan-research-portfolio.r8ms5bfzb6.chatgpt.site) · [Repository overview](../README.md)

## The teaching and research problem

A notebook that only produces a clean coefficient does not demonstrate understanding. These notes begin with the estimand and identification logic, simulate known ground truth, expose the estimator mechanics and then construct a setting where misuse fails.

## Public method coverage

- Sun–Abraham interaction-weighted event studies;
- Callaway–Sant'Anna group-time effects;
- Borusyak–Jaravel–Spiess imputation;
- wild-cluster bootstrap and spatial Conley/HAC inference;
- shift-share designs and shock-level equivalence;
- synthetic control and randomization inference;
- local projections.

## What is distinctive

| Layer | Requirement |
| --- | --- |
| Estimand | State the target before code |
| Identification | Separate assumptions from implementation |
| Known truth | Simulate a data-generating process with a recoverable answer |
| Estimator | Keep the important algebra visible in the notebook |
| Failure case | Reproduce a setting where the method becomes misleading |
| Validation | Run in CI and invite clean-environment reproduction |

## Current status

Method expansion is deliberately paused. The library is in a **validation phase**: outside reports may be PASS, FAIL or PASS WITH NOTES, and corrections are treated as evidence rather than reputational damage.

No professor email, private praise, repository star or download is presented as endorsement.

## Next validation gate

One independent clean-environment rerun, one non-author issue based on substantive use and one outside contribution or correction.
