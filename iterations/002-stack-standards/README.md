# Iteration 002: stack standards

Status: `doing`
Master issue: [#16](https://github.com/ednillibanio/app-catalog/issues/16)

## Objective and origin

Make this repository the independent source of truth for the standards shared by application repositories on one stack: a Java/Quarkus/Maven backend, a React/Vite frontend in a pnpm monorepo, and local development environments on macOS, Linux and Windows. More projects on this stack are planned, and a template repository ([#15](https://github.com/ednillibanio/app-catalog/issues/15)) follows once the standards exist. The maintainer decided this on 2026-11-14, after an application switched its documentation to Portuguese and exposed the mismatch between an English-only catalog and applications in another language.

## Scope, exclusions and dependencies

In scope: the bilingual convention and the Portuguese versions of the reader-facing docs (stage 01); the independence of this repository from the applications that use it (stage 02); then one shared standard per stage (03–05), each rewritten from the generic parts of the maintainer's existing application standards.

Out of scope: the template repository (#15), CI for this repository ([#8](https://github.com/ednillibanio/app-catalog/issues/8)), renaming this repository, and changes in application repositories, which are made in those repositories.

Dependencies: an application that follows a standard of stages 03–05 updates its own local standard after the stage merges, in its own repository. This repository does not track that work.

## Decisions

Approved by the maintainer on 2026-11-14.

- D1: English is canonical. The Portuguese file is a maintained translation, changed in the same PR; a divergence is a defect fixed to match English.
- D2: `name.md` (English) and `name.pt-BR.md` (Portuguese) sit side by side. Each starts with a reciprocal language switch. A Portuguese file links to translated documents in their Portuguese version and matching heading; links to English-only files, non-Markdown files and external URLs stay unchanged.
- D3: bilingual = the reader-facing docs (`README.md`, `CONTRIBUTING.md`, `docs/**`) and every new standard. English only = `AGENTS.md`, `PROVENANCE.md`, `iterations/**`, issues, pull requests and commits.
- D4: the catalog does not set an app's language. Each app states it in its own `AGENTS.md` and links to the catalog version in that language.
- D5: this iteration, with one stage per issue.
- D6: this repository is independent and reusable, like `ci-workflows`. Application repositories link to it; it does not list, describe or track them. The app inventory and the records of iteration 001, which described one application's adoption, were removed in stage 02 and remain in the Git history.

## Stages

| Stage | Status | Plan | Pull requests |
| --- | --- | --- | --- |
| 01 | `done` | [Bilingual docs](steps/01-bilingual-docs.md) ([#11](https://github.com/ednillibanio/app-catalog/issues/11)) | [#17](https://github.com/ednillibanio/app-catalog/pull/17) |
| 02 | `doing` | [Independent catalog](steps/02-independent-catalog.md) ([#18](https://github.com/ednillibanio/app-catalog/issues/18)) | pending |
| 03 | `todo` | [Backend standard](steps/03-backend-standard.md) ([#12](https://github.com/ednillibanio/app-catalog/issues/12)) | pending |
| 04 | `todo` | [Frontend standard](steps/04-frontend-standard.md) ([#13](https://github.com/ednillibanio/app-catalog/issues/13)) | pending |
| 05 | `todo` | [Dev environment standard](steps/05-dev-environment-standard.md) ([#14](https://github.com/ednillibanio/app-catalog/issues/14)) | pending |

Each stage requires its own approval, validation, review, pull request and recorded evidence.

## Validation and closure criteria

Per stage: `pre-commit run --all-files`; the link, anchor and language-pair check (`python3 scripts/check_docs.py`); a `technical-documentation` audit and a `codex-review` against `origin/main` at plan, stage end and pre-push. Before merge, record which hosted checks exist and their results; until #8 adds a workflow, record that there are none. The catalog schema check used in stage 01 was retired in stage 02 with the app inventory.

Close the iteration when every stage is `done` or `skipped` with a reason, all pending work has an owner and issue (including #8 and #15), and the maintainer authorizes closure.

## Result and pending work

Pending.
