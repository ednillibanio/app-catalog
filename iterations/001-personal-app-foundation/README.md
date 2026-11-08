# Iteration 001: personal app foundation

Status: `doing`. Master issue: [#1](https://github.com/ednillibanio/app-catalog/issues/1). Provisional tracker: [sapl-next #103](https://github.com/ednillibanio/sapl-next/issues/103), pending reconciliation.

## Objective and origin

Adopt personal application standards and reusable CI, using sapl-next as the first adopter. The catalog and CI repositories are independent, public, use new histories, `main` and Apache 2.0. The catalog defines outcomes; CI workflows implement hooks and PR validation, including Java and pnpm. Do not alter organization repositories or include their internal data.

## Decisions and dependencies

- On 2026-11-08 the maintainer removed completion of sapl-next iteration 002 from the critical path. Its VM, seed [#99](https://github.com/ednillibanio/sapl-next/issues/99), test [#81](https://github.com/ednillibanio/sapl-next/issues/81) and other pending work remain separate.
- After the language PR, new standards, documentation, issues, PRs, commits, automation text and comments in touched files use English; product text and domain identifiers remain Portuguese. Completing iteration 002 follows its current Portuguese policy.
- Keep existing review-tool installations and origins. Sapl-next retains its stricter local `technical-documentation` and `codex-review` requirements.
- Preserve Mac/Colima. Do not claim Linux or Windows validation without evidence. Each repository has its own linked issue, branch and PR. Reconcile sapl-next #80–#84 without duplication.
- No image publication, deployment, Sonar, new environment installers or Java guide in this iteration. Evaluate environment automation after platform-modules work. Protect repositories only after separate approval.

## Stages

| Stage | Status | Plan | Milestone |
| --- | --- | --- | --- |
| Preparation | `skipped` | [002 completion](steps/00-iteration-002.md) | Removed from critical path |
| 01 | `done` | [Personal catalog](steps/01-personal-catalog.md) | [PR #2](https://github.com/ednillibanio/app-catalog/pull/2), [PR #3](https://github.com/ednillibanio/app-catalog/pull/3) |
| 02 | `done` | [Reusable CI](steps/02-reusable-ci.md) | [PR #2](https://github.com/ednillibanio/ci-workflows/pull/2), [PR #3](https://github.com/ednillibanio/ci-workflows/pull/3), hook tag `v0.1.0` |
| 03 | `todo` | [Sapl-next adoption](steps/03-sapl-next-adoption.md) | Language PR and CI adoption |
| 04 | `todo` | [Reconciliation and protection](steps/04-reconciliation.md) | Assigned pending work and approved protections |

Each stage requires its own authorization, validation, review, PR and recorded evidence; later stages are not authorized by this plan. Maintain separate PRs and issues per repository. Record platform limitations and risks.

## Tracked alignment work

- Update the provisional sapl-next plan so its issue-mother reference points to app-catalog issue [#1](https://github.com/ednillibanio/app-catalog/issues/1) while retaining sapl-next [#103](https://github.com/ednillibanio/sapl-next/issues/103) as the provisional tracker until records are reconciled. Owner: maintainer. Tracked by issues #1 and #103; resolve during reconciliation. The source plan is outside this catalog PR.

## Closure criteria

Both public repositories are reviewed and versioned with provenance; hooks and workflows pass their tests and are exercised by test callers and a real sapl-next PR. Verify a documentation-only PR, resolved full SHAs, scanner failure behavior, `make check` parity and known IT reports. Required checks are protected only after approval. All pending work has an owner and issue. Audit docs, links and operational claims; apply the reviews required by each repository.

## Result

Stage 01 completed 2026-11-08: catalog and operator guide merged in PRs #2 and #3; schema, links and documentation were reviewed. Stage 02 completed 2026-11-08: reusable CI merged in PRs #2 and #3, hook tag `v0.1.0` published, and all test callers passed in GitHub Actions. Stage 03 remains `todo`. The full provisional plan remains at [sapl-next](https://github.com/ednillibanio/sapl-next/tree/dev/iterations/plano-adocao-pessoal) until the master issue and records are linked and reconciled.
