# Stage 01: personal catalog

Status: `done`

## Objective and scope

Create public `ednillibanio/app-catalog` with a new history, `main`, Apache 2.0, English README and agent instructions, iteration templates, minimal catalog/schema and sapl-next entry. Formalize this full cross-repository iteration and its master issue. Selectively adapt reusable contribution, iteration, review, documentation, DevSecOps and CI outcomes, recording provenance, owners, exceptions and evidence without organizational authority or internal data.

## Out of scope

Executable CI jobs, a Java guide and changes to source organization repositories. The catalog defines outcomes and the relationship to personal CI and stricter local rules.

## Acceptance criteria and validation

Validate license, links and schema; ensure plan and master issue agree, provenance is clear and documents are reviewed. Preserve all stages and pending work on transfer. Use separate issues and PRs per repository, subject to applicable approvals.

## Result, evidence and pending work

Completed 2026-11-08. Created public repository and issue #1. Merged catalog foundation in [PR #2](https://github.com/ednillibanio/app-catalog/pull/2) and operator guide in [PR #3](https://github.com/ednillibanio/app-catalog/pull/3). Fixed stale sapl-next parent-issue reference in commit `f03921c`.

Validation: Draft 2020-12 schema and app entry validated with jsonschema FormatChecker; local Markdown links checked; `git diff --check` passed. `technical-documentation` audit completed for the operator guide. Codex review round 1 requested tracking an out-of-scope plan mismatch; it was recorded and resolved in sapl-next. Final review approved. PR #3 had no CI checks configured. Linux and Windows were not tested.

Pending work remains in `iterations/BACKLOG.md`: reconcile remaining records in stage 04.
