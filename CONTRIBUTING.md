# Contributing to the Bike Share Optimizer project

This outlines how to propose a change to the Bike Share Optimizer project. 

### Fixing typos

Small typos or grammatical errors in documentation may be edited directly using
the GitHub web interface, so long as the changes are made in the _source_ file.

### Prerequisites

Before you make a substantial pull request, you should always file an issue and
make sure someone from the team agrees that it's a problem. If you've found a
bug, create an associated issue and illustrate the bug with a minimal 
[reprex](https://www.tidyverse.org/help/#reprex).

### Pull request process

*  We recommend that you create a Git branch for each pull request (PR).  
*  New code should follow PEP8 [style guide](https://www.python.org/dev/peps/pep-0008/) or the Black Code [style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) which is a subset of PEP8.

### Code of Conduct

Please note that this project is released with a [Contributor Code of
Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to
abide by its terms.

### Attribution
These contributing guidelines were adapted from the [dplyr contributing guidelines](https://github.com/tidyverse/dplyr/blob/master/.github/CONTRIBUTING.md).

---

## Milestone 3 Retrospective & Milestone 4 Collaboration Norms

As part of our continuous improvement for Milestone 4, the team has reflected on our workflow during M3 and established the following norms for M4.

### M3 Retrospective
* **What worked well:** We successfully integrated complex features (like the QueryChat AI tab) by effectively using branches. Communication regarding the overall layout and design of the dashboard was strong.
* **What needs improvement:** We experienced some bottlenecks with pull request reviews, where the workload was not perfectly balanced. Additionally, some major changes were merged close to the deadline, and documentation sometimes lagged behind the actual code implementation.

### M4 Collaboration Norms
To ensure a smooth, production-ready release for `v0.4.0`, we commit to the following workflow rules:
1. **Distributed Workload:** No single person should carry the codebase or dominate the review queue. Every team member must resolve at least one feedback item from the `M4 Feedback Prioritization` issue.
2. **Design Before Code:** For larger features (like the DuckDB integration or advanced UI interactions), we will explain the intent in a GitHub Issue and update the specification documents *before* writing the implementation.
3. **Scoped & Atomic PRs:** Each Pull Request should address exactly one feature or fix. PR descriptions must be meaningful and avoid massive "code dumps."

---