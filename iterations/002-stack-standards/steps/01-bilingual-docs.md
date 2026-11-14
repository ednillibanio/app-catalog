# Stage 01: bilingual docs

Status: `done`

## Objective and scope

Apply decisions D1–D4 of the [iteration](../README.md) and keep the catalog's reader-facing documents in English and Brazilian Portuguese. Tracked in [#11](https://github.com/ednillibanio/app-catalog/issues/11).

- Create this iteration's records and link them in `iterations/README.md`.
- Rewrite the language rule in `docs/standards/documentation.md` (new "Languages" section), `AGENTS.md` and `CONTRIBUTING.md`.
- Add the language switch to the 10 reader-facing documents (`README.md`, `CONTRIBUTING.md`, `docs/standards/{README,contribution,iterations,review,documentation,ci-devsecops}.md`, `docs/operations/operator-guide.md`, `catalog/README.md`) and create their `.pt-BR.md` translations.
- Add "Maintain both languages" to the operator guide, with a check for language pairs, links and anchors, and point the guide's link-validation sentence to it.

## Out of scope

- Content changes to the standards beyond the language rule.
- Running the check in CI ([#8](https://github.com/ednillibanio/app-catalog/issues/8)).
- `iterations/001-*` (closed history).

## Acceptance criteria and validation

- Every reader-facing document has its pair and reciprocal language switch.
- The operator guide check reports 0 unpaired files, 0 broken relative links and anchors in both languages, and the same heading count per pair.
- Each pair is reviewed side by side against its English source (requirements, commands, links, exceptions and limitations), with findings resolved.
- `pre-commit run --all-files` and the catalog schema check pass.
- `technical-documentation` audit and `codex-review --base origin/main` recorded.

## Result, evidence and pending work

### Changes

- Language rule: new "Languages" section in `docs/standards/documentation.md`; `AGENTS.md` and `CONTRIBUTING.md` point to it.
- Language switch on the first line of the 10 reader-facing documents and 10 new `.pt-BR.md` translations.
- `scripts/check_docs.py`: checks language pairs, the reciprocal switch, heading counts per pair, relative links and GitHub-style anchors (including duplicate-heading suffixes and percent-encoding), and Portuguese pages that link to the English version of a translated document. Documented restrictions: fenced code blocks and `#` headings only.
- Operator guide: "Maintain both languages" section, link-validation sentence, troubleshooting entry and limitations updated in both languages; the README validation paragraph points to the check.
- Deviation from the plan: the plan placed the check inline in the operator guide. After review round 001 it grew too large to keep two inline copies in sync, so it moved to `scripts/check_docs.py`, which both guides and both READMEs call.

### Validation

| Check | Result |
| --- | --- |
| `python3 scripts/check_docs.py` | `OK: 10 language pairs, 37 Markdown files`, exit 0 |
| Negative tests on a copy of the repository | Reported a missing pair, an empty pair file, missing switch, heading-count mismatch, broken links (titled, reference, balanced parentheses, percent-encoded, after a fence), broken and duplicate-suffix anchors, a tracked file deleted from the working tree, and English links from a Portuguese file; ignored links in backtick, tilde and longer fences and in single- and multi-line inline code; handled a filename with a space; exit 1 |
| Code blocks of `operator-guide.md`/`.pt-BR.md` and `catalog/README.md`/`.pt-BR.md` (the latter removed in stage 02) | Identical |
| Catalog schema check from the operator guide (`uv run --no-project --with jsonschema`) | `Valid: catalog/apps/<app>.json` (one entry; the app name was redacted in stage 02, which also retired the schema check) |
| `pre-commit run --files` on every changed and new file, before commit | Passed (`sem-env` and `check-shdoc`: no files to check) |
| `pre-commit run --all-files` after commit `c13fce1`, with the new files tracked | Passed (`sem-env` and `check-shdoc`: no files to check) |
| Hosted checks | None: this repository has no workflow until [#8](https://github.com/ednillibanio/app-catalog/issues/8) |

Platform: macOS only. The check uses only the Python 3 standard library and Git; Linux and Windows were not tested.

### Reviews

| Review | Result |
| --- | --- |
| `technical-documentation` audit (plan) | 2 findings (Portuguese links to English-only files; provenance check for stages 02–04), both applied to the plan |
| `technical-documentation` audit (change) | README validation paragraph did not mention the check; fixed in both languages |
| `codex-review` plan, rounds `plano-cat-002-001`..`002` | CHANGES REQUESTED (5 findings, fixed), then APPROVE (1 low, fixed) |
| `codex-review` pre-push of `c13fce1`, round `11-bilingual-prepush-001` | APPROVE; 2 low findings on this evidence (the all-files pre-commit run and the pending list), fixed in the follow-up commit |
| `codex-review` change, rounds `11-bilingual-001`..`006` | Rounds 001–005 CHANGES REQUESTED, all on the check's Markdown parsing (file listing, fences, link forms, slugs, URL decoding, empty files, code spans), each fixed and retested; indented code and Setext headings documented as unsupported. Round 006 APPROVE, no findings; it compared all 10 pairs and found no omission or change of meaning |

Codex records are in `.agent-runs/codex-reviews/` (ignored by Git).

### Out-of-scope findings for triage

- `iterations/001-personal-app-foundation/README.md:3` is still `doing`, although master issue #1 is closed and all its stages are done or skipped. Resolved in stage 02: the iteration 001 records were removed.
- `iterations/README.md:3` still says the consuming app's provisional tracker "remains the provisional tracker until reconciliation"; stage 04 of iteration 001 completed the reconciliation. Resolved in stage 02.
- `iterations/BACKLOG.md` keeps the consuming app's reconciliation row, resolved in iteration 001 stage 04. Resolved in stage 02: the row was removed.
- `docs/operations/operator-guide.md` "Current limitations" says a real consumer PR "remains to be validated in stage 03"; iteration 001 stage 03 validated it. The Portuguese file mirrors the same sentence. Resolved in stage 02: the sentence was removed.

### Result

Merged in [PR #17](https://github.com/ednillibanio/app-catalog/pull/17) as `aacc0fb` on 2026-11-14 (squash of `c13fce1` and `c500442`); pre-merge `codex-review` round `11-bilingual-premerge-001` APPROVE, with one low finding (this record still listed the push and PR as pending), resolved by this closeout in stage 02. [#11](https://github.com/ednillibanio/app-catalog/issues/11) closed.
