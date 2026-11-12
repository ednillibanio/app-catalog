# Stage 04: reconciliation and protection

Status: `doing`

## Objective and scope

Reconcile sapl-next #80–#84 and its accepted backlog without duplicating work. Assign every pending item to an issue and owner. Apply pull-request and required-check protections only after separate approval; the approved changes were applied on 2026-11-12 and are recorded below. Do not implement image publication, deployment, Sonar or new environment installers.

## Tracker reconciliation

On 2026-11-12, master issue [app-catalog #1](https://github.com/ednillibanio/app-catalog/issues/1) was updated: stages 01–03 are checked, Stage 04 is in progress, and `@ednillibanio` is assigned. The provisional [sapl-next #103](https://github.com/ednillibanio/sapl-next/issues/103) has the same stage state and owner. The user-reported installation restriction was removed, allowing the app-catalog tracker update.

The current sapl-next reconciliation is:

| Issue | Disposition |
| --- | --- |
| [#79](https://github.com/ednillibanio/sapl-next/issues/79) | Iteration 002 remains separate. Steps 01–06 are complete; bootstrap/smoke and fresh VM validation remain assigned. |
| [#80](https://github.com/ednillibanio/sapl-next/issues/80) | Stage 03 delivered basic pre-commit hooks, repository hygiene, secret scanning and PR title validation. Remaining formatting, pinning and CI hygiene work stays here. |
| [#81](https://github.com/ednillibanio/sapl-next/issues/81) | CI integration tests were enabled informally. Three `TramitacaoAdminResourceIT` failures remain separate iteration 004 work; do not include their fixes here. Coverage, Maven enforcer and other test gaps remain assigned here. |
| [#82](https://github.com/ednillibanio/sapl-next/issues/82) | Semgrep, CycloneDX SBOMs and scheduled dependency scans were recorded complete. SonarQube and `SECURITY.md` remain. The 41 Dependabot alerts recorded on November 6 are a stale snapshot and need a fresh count before triage. |
| [#83](https://github.com/ednillibanio/sapl-next/issues/83) | Retains backend, SPA and SSR image builds, scanning and GHCR publication; out of scope for this adoption. |
| [#84](https://github.com/ednillibanio/sapl-next/issues/84) | Retains documentation index, README, ADR, domain and endpoint documentation, roadmap and historical link audit. |
| [#95](https://github.com/ednillibanio/sapl-next/issues/95) | Retains the separate development-seed default-versus-opt-in decision. |
| [#97](https://github.com/ednillibanio/sapl-next/issues/97) | Retains environment standards and per-environment guides, including Windows. |
| [#99](https://github.com/ednillibanio/sapl-next/issues/99) | Retains the broken V105 development seed and compliant repair decision; do not modify an existing Flyway migration. |

The remaining accepted backlog has distinct assigned sapl-next issues: #109–#113 for five medium-priority data-model findings, #114 for triage of 17 low-priority findings, #115 for the session/voting/committee audit, and #116 for file storage and attachment management. Issues #79–#84, #95, #97, #99 and #109–#116 are open and assigned to `@ednillibanio`.

## Protection evidence

After explicit approval on 2026-11-12, active repository rulesets were applied and verified. All require pull requests, block deletion and non-fast-forward updates, have no bypass actors, and require zero approving reviews for the single-maintainer workflow.

| Repository and branch | Ruleset | Required checks |
| --- | --- | --- |
| [app-catalog `main`](https://github.com/ednillibanio/app-catalog/rules/27132939) | `27132939`, active | None are available: the repository has no GitHub Actions workflows and its default-branch commit has zero check runs. |
| [ci-workflows `main`](https://github.com/ednillibanio/ci-workflows/rules/27132950) | `27132950`, active | Twelve contexts verified successful on PR #4: `backend / tests`, `frontend / validate`, `hygiene / hygiene`, `hygiene`, `secrets / gitleaks`, `title / title`, `sast / semgrep`, `sast-execution-error`, `security / trivy`, `dependencies / trivy`, `sbom-backend / sbom`, and `sbom-frontend / sbom`. Main run #12 also passed `hygiene`. |
| [sapl-next `dev`](https://github.com/ednillibanio/sapl-next/rules/25796977) | `25796977`, active | Five required contexts verified successful on PR #108 run #48: backend, frontend, repository hygiene, secret scan and PR title. The informational integration job and scanner findings are not required. |

Fresh API reads confirm active rulesets and `protected: true` for all target branches. Sapl-next retained the existing default-branch rules and Copilot review rule while gaining the five required checks. App-catalog has no CI checks to require until workflows are added.

## Validation and review

- PR #108 proved Markdown-only triggering in run #47; run #48 passed the required checks. It merged to sapl-next `dev` as `54d37610857b8347c5ba38e2394727f977fee2c0`.
- The sapl-next Stage 04 record was checked against current GitHub issue, PR, ruleset, workflow and check-run data. Its relative Markdown links and `git diff --check` passed; the documentation audit and Codex review round 006 approved with no findings.
- This app-catalog plan change is documentation-only. `PRE_COMMIT_HOME=/private/tmp/sapl-stage04-precommit rtk pre-commit run --all-files` passed; six relative Markdown targets resolve, and `git diff --check` passed. App-catalog currently has no hosted CI workflows; record the Codex review disposition in the PR.
- The current sapl-next plan remains in its original checkout with unrelated user-owned `AGENTS.md` changes preserved. No tests were run for this documentation reconciliation.
- Mac/Colima support was preserved. Linux and Windows were not tested.

## Remaining work

- Keep Stage 04 in progress until the repository-specific plan updates are reviewed and merged and the trackers are reconciled with those results.
- Keep app-catalog's master issue #1 and sapl-next #103 linked; close neither until the cross-repository records are consistent and the maintainer authorizes closure.
- Follow separate approvals for commit, push, pull-request creation and merge. Do not update app-catalog directly on `main`.
