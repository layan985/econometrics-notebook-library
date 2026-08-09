# External Validation Ledger

This page records **third-party evidence only**. Author-run CI, author-run notebook execution, and author-written documentation do not count as external validation.

## Validation targets

| Target | Definition of done | Status |
|---|---|---|
| Professor use | A faculty member uses, recommends, or assigns at least one notebook in research, teaching, or RA training, with attributable evidence and permission to name them | ☐ Open |
| Independent reproduction | A non-author clones a clean environment and successfully reproduces at least one notebook at a stated commit SHA | ☐ Open |
| External issue | A non-author opens a substantive methodological, numerical, software, or documentation issue | ☐ Open |
| External PR | A non-author submits a substantive pull request that passes CI and is merged | ☐ Open |
| Live Quarto site | GitHub Pages successfully deploys the Quarto documentation from `main` | ☐ Pending deployment verification |

## Validation ledger

| Date | Validator | Affiliation | Object | Commit SHA | Result | Evidence |
|---|---|---|---|---|---|---|
| — | — | — | — | — | Awaiting external validation | — |

## Evidence rules

A validation entry should include enough information for another researcher to inspect the claim:

1. validator name or stable public identity;
2. affiliation when the validator is willing to provide it;
3. exact notebook, function, or documentation object checked;
4. repository commit SHA;
5. operating system and Python version for computational reproductions;
6. commands executed;
7. whether numerical tests and notebook execution passed;
8. any deviations, errors, or ambiguities discovered;
9. a public issue, pull request, or other durable evidence link where possible.

Negative results belong here too. A failed reproduction that identifies a real portability, dependency, numerical, or methodological problem is useful validation evidence once the failure is documented and investigated.

## What does not count

- a repository star;
- a clone or page view without evidence of use;
- the author's own CI run;
- a contributor listed without a substantive contribution;
- a testimonial that cannot be tied to an inspected notebook or use case;
- a pull request created solely to manufacture activity.

The goal is not social proof. The goal is evidence that independent researchers can execute, inspect, criticize, and reuse the library.
