# Iteration 002: stack standards

Status: `doing`
Master issue: [#16](https://github.com/ednillibanio/app-catalog/issues/16)

## Objective and origin

Make this catalog the source of truth for the standards shared by apps on the sapl-next stack: a Java/Quarkus/Maven backend, a React/Vite frontend in a pnpm monorepo, and local development environments on macOS, Linux and Windows. Another project on this stack is planned, and a template repository ([#15](https://github.com/ednillibanio/app-catalog/issues/15)) follows once the standards exist. The maintainer decided this on 2026-11-14, after [sapl-next #153](https://github.com/ednillibanio/sapl-next/issues/153) switched that app to Portuguese and exposed the mismatch between an English-only catalog and apps in another language.

## Scope, exclusions and dependencies

In scope: the bilingual convention and the Portuguese versions of the reader-facing docs (stage 01), then one shared standard per stage (02–04), each written from the generic parts of its sapl-next source.

Out of scope: the template repository (#15), CI for this repository ([#8](https://github.com/ednillibanio/app-catalog/issues/8)), and changes to sapl-next, which are made in [sapl-next #84](https://github.com/ednillibanio/sapl-next/issues/84) and [#97](https://github.com/ednillibanio/sapl-next/issues/97).

Dependencies: stages 02–04 pair with sapl-next iteration 007 stages 01–03. For each pair, the catalog PR merges first; the sapl-next PR then reduces its local standard to stricter rules plus a link.

## Decisions

Approved by the maintainer on 2026-11-14.

- D1: English is canonical. The Portuguese file is a maintained translation, changed in the same PR; a divergence is a defect fixed to match English.
- D2: `name.md` (English) and `name.pt-BR.md` (Portuguese) sit side by side. Each starts with a reciprocal language switch. A Portuguese file links to translated documents in their Portuguese version and matching heading; links to English-only files, non-Markdown files and external URLs stay unchanged.
- D3: bilingual = the reader-facing docs (`README.md`, `CONTRIBUTING.md`, `docs/**`, `catalog/README.md`) and every new standard. English only = `AGENTS.md`, `PROVENANCE.md`, `iterations/**`, issues, pull requests and commits.
- D4: the catalog does not set an app's language. Each app states it in its own `AGENTS.md` and links to the catalog version in that language.
- D5: this iteration, with one stage per issue.

## Stages

| Stage | Status | Plan | Pull requests |
| --- | --- | --- | --- |
| 01 | `doing` | [Bilingual docs](steps/01-bilingual-docs.md) ([#11](https://github.com/ednillibanio/app-catalog/issues/11)) | pending |
| 02 | `todo` | [Backend standard](steps/02-backend-standard.md) ([#12](https://github.com/ednillibanio/app-catalog/issues/12)) | pending |
| 03 | `todo` | [Frontend standard](steps/03-frontend-standard.md) ([#13](https://github.com/ednillibanio/app-catalog/issues/13)) | pending |
| 04 | `todo` | [Dev environment standard](steps/04-dev-environment-standard.md) ([#14](https://github.com/ednillibanio/app-catalog/issues/14)) | pending |

Each stage requires its own approval, validation, review, pull request and recorded evidence.

## Validation and closure criteria

Per stage: `pre-commit run --all-files`; the link, anchor and language-pair check; the catalog schema check from the [operator guide](../../docs/operations/operator-guide.md); a `technical-documentation` audit and a `codex-review` against `origin/main` at plan, stage end and pre-push. Before merge, record which hosted checks exist and their results; until #8 adds a workflow, record that there are none.

Close the iteration when every stage is `done` or `skipped` with a reason, all pending work has an owner and issue (including #8 and #15), and the maintainer authorizes closure.

## Result and pending work

Pending.
