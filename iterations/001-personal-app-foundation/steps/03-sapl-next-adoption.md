# Stage 03: sapl-next adoption

Status: `todo`

First integrate a focused language and authority PR: translate active agent and contribution instructions, local review and Git rules, active standards, getting-started guides, active templates and canonical endpoint catalog. Explicitly change `AGENTS.md` language policy and matching iteration and Git rules; preserve Portuguese product text and domain identifiers. Track untranslated historical docs and untouched comments. Replace organizational normative references in active docs with the personal catalog, preserving stricter local sapl-next rules.

Then adopt published, SHA-pinned hooks and lean workflow calls. Configure `pull_request` for `dev` and `main`, `push` for `dev` and scheduled dependency checks; remove Markdown `paths-ignore`. Retain PostgreSQL/Redis services; Dev Services is decided in [#81](https://github.com/ednillibanio/sapl-next/issues/81).

After cleanup, unit tests, frontend build/lint/test, hygiene, secrets and PR title are required. ITs, Semgrep and dependency findings start as informational with reports and issues; scanner infrastructure or execution failures must fail. Promote checks after findings are resolved. Compare with `make check`, validate a docs-only PR and SHA resolution, audit translation, links, examples and policy, and exercise every workflow in a real sapl-next PR. `portal-gabinete` has no test script; do not claim five-app test coverage. No installers, image publication, deployment or immediate promotion of security findings to blocking.

## Result, evidence and pending work

Pending.
