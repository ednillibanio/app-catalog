# Stage 02: independent catalog

Status: `doing`

## Objective and scope

Apply decision D6 of the [iteration](../README.md): this repository is an independent, reusable source of truth, like `ci-workflows`. Application repositories link to it; it does not list, describe or track them. Tracked in [#18](https://github.com/ednillibanio/app-catalog/issues/18).

- Remove the app inventory: `catalog/` (README in both languages, schema and the single app entry) and the schema validation in both READMEs and both operator guides.
- Remove the records of iteration 001, which described one application's adoption; they remain in the Git history and the closed issues #1–#9.
- Remove application names from the reader-facing docs (both languages), `PROVENANCE.md`, `iterations/README.md`, `iterations/BACKLOG.md` and the iteration 002 records.
- Add "Using these standards" to the standards index (both languages): applications link to the standards, may pin a commit or tag, and keep their rules and exceptions in their own repositories.
- `PROVENANCE.md`: the organization source keeps only "CI/DevSecOps outcome categories"; the planning source becomes a private first-party row with the revision consulted, without naming the application.
- Close stage 01 (PR #17) and renumber the standards stages to 03–05.
- Edit the bodies of the open issues #10 and #12–#16 so they name no consuming application, and add this stage to the #16 checklist. Each edit needs its own approval and is verified with `gh issue view`; this stage is not `done` until they are made.

The application whose entry and records were removed recorded its own adoption and repointed its references to a permanent link at commit `aacc0fb` before this stage, in its own repository.

## Out of scope

Renaming this repository; the content of the standards.

## Acceptance criteria and validation

- A case-insensitive search of tracked file contents and names for consuming-application terms finds nothing.
- A search for inventory-specific expressions matches only this iteration's records, which describe the removal.
- `python3 scripts/check_docs.py` passes with 9 language pairs, after the deletions are staged; `pre-commit run --all-files` passes.
- The bodies of #10 and #12–#16 name no consuming application and #16 lists this stage (`gh issue view`).
- `technical-documentation` audit and `codex-review --base origin/main` recorded.

## Result, evidence and pending work

### Changes

- Deleted `catalog/` (4 files) and `iterations/001-personal-app-foundation/` (6 files).
- Both READMEs describe a reusable, independent repository and no longer validate a schema; both operator guides drop "Inspect app adoption", the schema check and its troubleshooting entries, and keep a "Validate links" section; both `review.md` files give a generic example instead of an application name; both `documentation` files drop `catalog/README.md` from the bilingual list; both standards indexes gain "Using these standards".
- `PROVENANCE.md`: the organization row keeps "CI/DevSecOps outcome categories"; the planning row is a private first-party source with its revision and no application name.
- `iterations/README.md` and `BACKLOG.md` (resolved row removed); iteration README with D6, the new stage and renumbered stages 03–05; stage 01 closed with its history kept and names neutralized; `scripts/check_docs.py` no longer lists `catalog/README.md`.

### Validation

| Check | Result |
| --- | --- |
| `python3 scripts/check_docs.py`, after staging the deletions | `OK: 9 language pairs, 30 Markdown files` |
| Consumer-term search over tracked contents and file names (case-insensitive) | No match |
| Inventory-expression search over tracked contents and file names | Matches only in this iteration's records (D6, the validation note, the stage 01 evidence row and this stage's scope) |
| `pre-commit run --all-files`; `git diff --cached --check` | Passed |
| Hosted checks | None until [#8](https://github.com/ednillibanio/app-catalog/issues/8) |

### Reviews

| Review | Result |
| --- | --- |
| `technical-documentation` audit (plan and change) | No findings beyond those Codex raised |
| `codex-review` plan, rounds `plano-18-independence-001`..`005` | Rounds 001–004 CHANGES REQUESTED (missing references, history kept as dated evidence, traceable provenance, link sequencing, executable searches), each fixed; round 005 APPROVE |
| `codex-review` change, rounds `18-independence-006`..`008` (the counter is shared with the plan rounds) | 006: the backend stub lacked E1–E5 and the source revision, and the issue edits were out of scope; 007: the stubs dropped the source-history check; both fixed. 008 APPROVE, no findings |

### Pending

- Edit the bodies of #10 and #12–#16 and the #16 checklist (each with its own approval).
- Commit, push, pull request and merge, each with its own approval; then this stage becomes `done`.
