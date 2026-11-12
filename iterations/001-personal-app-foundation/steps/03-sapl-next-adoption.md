# Stage 03: sapl-next adoption

Status: `done`

## Scope and result

Adopt the personal language, contribution and review policies and published CI interfaces in sapl-next while retaining stricter local requirements. Stage 03 completed through [PR #106](https://github.com/ednillibanio/sapl-next/pull/106) (language and authority), [PR #107](https://github.com/ednillibanio/sapl-next/pull/107) (published reusable CI adoption) and [PR #108](https://github.com/ednillibanio/sapl-next/pull/108) (documentation-only CI trigger validation). PR #108 merged to `dev` at `54d37610857b8347c5ba38e2394727f977fee2c0`.

## Evidence and limitations

- PR #108 run #47 was triggered by a Markdown-only change; all required checks passed.
- PR #108 run #48 passed backend unit tests, frontend validation, repository hygiene, secret scan, PR title, Semgrep, security and dependency scans, and both SBOM jobs. The informational integration job ran 202 tests: 199 passed and three failed in `TramitacaoAdminResourceIT`; the failures remain separately tracked in [sapl-next #81](https://github.com/ednillibanio/sapl-next/issues/81).
- The reusable backend workflow lacks PostgreSQL and Redis services, and the reusable secrets workflow does not pass `pull-requests: read`. Sapl-next therefore retains those local caller jobs with scoped permissions.
- The local `make check` was not run because the Colima Docker socket was unavailable. Linux and Windows were not tested.
- The PR recorded successful documentation audits and pre-push and pre-merge Codex reviews. Its hosted CI evidence and review record are in PR #108.

## Deferred work

Keep the three `TramitacaoAdminResourceIT` failures in iteration 004 #81. Other pending app CI work remains assigned to sapl-next issues #80–#84, #95, #97 and #99; Stage 04 reconciles these without expanding this adoption scope.
