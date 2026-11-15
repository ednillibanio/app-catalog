# Stage 05: local development environment standard

Status: `done`

## Objective and scope

Write `docs/standards/dev-environment.md` and `dev-environment.pt-BR.md`, a shared standard for the local development environment of application repositories: supported environments (macOS, Linux, Windows), differences only in a local unversioned `.env` documented by `.env.example`, an idempotent setup script, a read-only doctor check, common commands, cross-environment compatibility, and how each environment guide declares its validation state. Index it in the standards README and the root README, in both languages, and record the source in `PROVENANCE.md`. Tracked in [#14](https://github.com/ednillibanio/app-catalog/issues/14). The plan, with the full source classification, is kept outside this repository; the Evidence section maps every row of it.

Decisions approved by the maintainer on 2026-11-14:

- G1: file `docs/standards/dev-environment.md` and its `.pt-BR.md`, title "Local development environment", in the style of stages 03–04, indexed in both standards READMEs and the root READMEs' topics line.
- G2: generic rules are derived and written anew, not copied. `PROVENANCE.md` records the source as the maintainer's private application repository (not public), revision `f9f3597`, its environment guides, task runner, setup and provisioning scripts, `.env.example`, Compose file and package manager settings, first-party content, without naming the application. The row also states that two general script practices came indirectly from internal script conventions that the source cites (not public), restated without copying.
- G3: each environment guide starts with its validation state: `Validated` (date, revision, who, commands run) or `Not validated` (reviewed against the repository only, with a tracking issue and who can validate it). A change to shared files leaves other environments not validated for that change until someone runs it there.
- G4: every supported environment has a setup script, a doctor check and the common command interface. A gap is an exception recorded as the standards index requires; the standard grants no standing exception.
- G5: no tool versions in the standard; tools are named only as examples.
- G6: a minimum command set (`help`, `setup`, `doctor`, `up`, `down`, `test`, `dev`, `check`) with the same names and effects in every supported environment, through any task runner or wrapper; `down` keeps data, destructive commands have their own names; `test`/`dev` may be split per component; `smoke` recommended.
- G7: tooling (scripts, task runner, Compose files, `.env.example`, CI workflows) is written in English, one language per file; product and domain identifiers in tooling keep the app's vocabulary.
- G8: `docs/standards/documentation.md` "Languages" requires each app to keep a language map in its agent instructions, with a neutral example.
- D4 of the iteration refined accordingly (iteration README).
- Code blocks are identical in both languages; only prose is translated.

## Out of scope

Application guides, scripts and `.env` contents; CI for this repository (#8); the template repository (#15); any change in the application repository.

## Acceptance criteria and validation

No application-specific name or data in the standard (case-insensitive search with a private terms list kept outside this repository, plus a manual read). Examples run in a scratch directory outside both repositories. Linux and Windows are not claimed as validated without evidence.

## Result, evidence and pending work

### Changes

- New `docs/standards/dev-environment.md` and `dev-environment.pt-BR.md`, sections 1–15.
- `docs/standards/documentation.md` and `.pt-BR.md`: tooling in English and the language map (G7, G8).
- `docs/standards/README.md` and `README.pt-BR.md`: new row; root `README.md` and `README.pt-BR.md` name the standard among the topics.
- `PROVENANCE.md`: new private first-party row with revision `f9f3597` and the indirect influence (G2).
- Iteration README: D4 refined; rows 04 `done` (PR #21) and 05 `doing`.
- Stage 04 closed (`done`, PR #21, merge `9117779`, pre-merge reviews recorded).

### Source mapping

"New" marks a rule stricter than, or absent from, the source.

| Source | Catalog | Stays local / adaptation |
| --- | --- | --- |
| Agent instructions, environment list | §1 | Exact OS versions, VM box and provider. New: the guide, setup, doctor and commands required per environment, with exceptions recorded (G4) |
| `.env.example`, Compose file, task runner `.env` loading | §2, §3 | Variable names, ports, fallback ranges, identity-provider and LAN preview settings. New: portable `.env` syntax and documented precedence |
| Runtime version files, `packageManager`, build tool wrapper, image tags | §4 | Versions, SDK manager and package manager specifics |
| macOS install script, VM provisioning script | §5 | Formulas, hardware restriction. Adapted: no privilege escalation applies to the contributor's machine; a disposable VM provisioner may use privileged steps (as the source VM script does). New: `--dry-run` for VM provisioning (the source VM script has none) |
| macOS doctor script | §6 | Check list. New: a doctor check per environment (the source has one for macOS only) |
| macOS bootstrap script | §7 | Runtime profile sizes, port-picking details |
| Task runner targets | §8 | Target list beyond the minimum set. New: the minimum set with the same names in every environment (the source has no aggregate `test` or `dev`, and its `setup`/`doctor` run on macOS only); `check` states which CI jobs it omits |
| Compose file, package manager settings, VM guide | §9 | `.npmrc` values shown as an illustration; Vagrant specifics. Adapted: the VM working tree location is the app's documented choice. New: `.gitattributes` for LF line endings (the source has none); WSL2 working tree in the Linux file system. Rule 7 (script modes in Git) states what the source's `check-exec-bit` hook, from the maintainer's public `ci-workflows`, enforces: run-directly scripts with a shebang `100755`, sourced libraries `100644`; the source repository complies |
| — (not in source) | §10 | New (G7) |
| macOS guide and VM guide | §11 | Guide content. New: validation state at the top of each guide (G3) |
| Agent instructions "test in the current environment" | §12 | — |
| LAN preview section, `.env.example` | §13 | Identity-provider and certificate tool procedure |
| — | §14 anti-patterns, §15 checklist | — |

### Validation

| Check | Result |
| --- | --- |
| `python3 scripts/check_docs.py` | `OK: 12 language pairs, 36 Markdown files` |
| Pair comparison (scripted) | `dev-environment`: 10 fenced blocks in each file, identical; 32 headings in each; `§` references identical. `documentation`: same headings |
| Shell examples (§5, §6, §7), extracted by a script into a scratch directory | `bash -n` and `shellcheck -s bash`: pass. §5 run: an installed command prints `[ OK ]`, a missing one prints `[PLAN]` under `DRY_RUN=1` and runs the command otherwise. §7 run twice: first run creates `.env` (mode 600), second keeps it; with a dangling `.env` symlink it keeps the link and does not create its target. §6 run with the container runtime stopped: 1 failure, exit 1. With stub `docker` commands on `PATH` and Node v26.13.0: `.nvmrc` pins `26`, `v26.13` and `26.13.0` pass (exit 0, `All checks passed.`); `22.14` and `26.1` fail (exit 1), so a pin is compared in full, not by major only. The `.env` line-ending check passes with an LF `.env` or no `.env`, and fails (exit 1) with a CRLF `.env`, an unreadable `.env` (mode 000), a directory named `.env` or a dangling `.env` symlink. The `install_if_missing colima …` line and the Makefile are illustrative |
| Compose example (§9) with `docker compose config --format json` (Docker Compose 5.6.1) | Without `.env`: image `docker.io/library/postgres:<tag>` (placeholder) and port published on `127.0.0.1:5432`. With `.env` `POSTGRES_PORT="5544"` (double quotes): `5544`; with `POSTGRES_PORT='5545'` (single quotes): `5545`. With `POSTGRES_PORT=6000` set in the shell, a direct call: `6000` (shell wins). Through the §8 Makefile's `LOAD_ENV` with the same shell value: the `.env` value (`.env` wins), as §3 rule 7 states. `docker compose config` checks parsing and interpolation only; it does not establish Podman compatibility or service readiness |
| Makefile (§8) | `make` with no target and `make help` list the five targets with their descriptions. With `COMPOSE` pointing to an argument printer and `COMPOSE_UP_FLAGS="-d --wait"` (and again with single quotes) in `.env`, `make up` passes `up`, `-d`, `--wait` as three arguments and prints nothing else. With `COMPOSE_UP_FLAGS=-d` (the Podman setting), it passes `up`, `-d` and prints the instruction to run `make ps` until every service is healthy. Without `.env`, `make -n up` shows the `docker compose` and `-d --wait` defaults |
| `.env` subset (§3 rule 5) through both paths | A `.env` with a comment line, unquoted values using the whole allowed character set (`plain-value_1.2:3`, `user@host:/p,a+b=c`), a double-quoted and a single-quoted value with a space and `;`, and a single-quoted value starting with `~`: `docker compose config` and `bash` sourcing with `set -a` give the same values. Unquoted `;` and a leading `~`, outside the allowed set, give different results (the shell splits the command or expands the home directory), which is why §3 excludes them. A name with `-` (`MY-VAR=value`): Compose reads it as an `env_file` (`MY-VAR: value`), the shell fails with "command not found" |
| Script mode (§9 rule 7) in a scratch Git repository with `core.fileMode=false` | A new `run.sh` with mode 644 is staged as `100644`; after `git update-index --chmod=+x run.sh` the index and the commit show `100755` |
| `.gitattributes` (§9) in a scratch Git repository, `git check-attr eol` | `run.sh`, `.env.example`, `Makefile`, `mvnw`: `lf`; `mvnw.cmd`: `crlf`; `README.md`: unspecified |
| Private-terms search: `grep -n -i -F -f <terms file>` over both new files, both `documentation` files, `PROVENANCE.md` and the four indexes, with the stage 04 list extended with the source's environment names (VM box, project and realm names, ports, organization names) and kept outside this repository | `Vagrant` in §1 of both files: a generic tool named as an example, kept. Portuguese files: only ordinary Portuguese words that equal some private terms, kept. `PROVENANCE.md` and the root READMEs: only existing rows and the maintainer's public account name, kept |
| Manual read of every example and table | No application name, port other than the PostgreSQL default, realm or data |
| Source history | `f9f3597` is the source repository head; every commit to the source files is first-party |
| `pre-commit run --all-files` | Passed |
| Hosted checks | None until [#8](https://github.com/ednillibanio/app-catalog/issues/8) |

### Reviews

| Review | Result |
| --- | --- |
| `codex-review` plan, round `plano-14-devenv-001` | CHANGES REQUESTED, 4 medium and 1 low findings, applied: no standing exception for an environment without a setup script (G4); a common command interface instead of direct-command equivalents (G6); provenance records the indirect influence; validation with `docker compose config`, runnable shell examples and labelled fragments; VM working tree as the app's choice |
| `codex-review` plan, round `plano-14-devenv-002` | APPROVE; 2 low findings applied: each minimum command's effect defined, with `down` keeping data; validation limits and a two-path `.env` check |
| `technical-documentation` audit (plan) | 3 findings, applied: the minimum command set labelled stricter than the source; guides cover prerequisites, preparation, `.env`, verification and troubleshooting; optional `smoke` |
| `codex-review` plan, round `plano-14-devenv-003` | APPROVE; 1 low finding applied: portable `.env` syntax and precedence, validated with a quoted value and a shell override |
| `codex-review` plan, round `plano-14-devenv-004` (after G7, G8 and D4 were added) | APPROVE; 3 low findings applied: domain identifiers in tooling keep the app's vocabulary; macOS-derived practices separated from the VM provisioner; provenance names every source file kind |
| `technical-documentation` audit (stage end) | 1 low finding, fixed in both languages: the `.env.example` comment no longer states that podman-compose lacks `--wait` in general; it says some versions do. Other claims checked against the source files, the runs above, and Microsoft's WSL guidance on keeping files in the Linux file system |
| `codex-review --base origin/main`, round `14-devenv-005` (the counter is shared with the plan topic) | CHANGES REQUESTED, 2 medium and 2 low findings, fixed in both languages: the Makefile no longer `include`s `.env` as Make syntax (quoted multi-argument values reached Compose as one argument); the shell reads `.env` and the defaults live in the shell expansion. The doctor compares the full `.nvmrc` pin, not the major only. §3 rule 5 names single or double quotes. The Compose example uses a `<tag>` placeholder instead of a real version (G5). All rerun as recorded above |
| `codex-review`, round `14-devenv-006` | CHANGES REQUESTED, 2 medium and 1 low findings, fixed: §3 rule 5 narrows the `.env` subset (unquoted values without spaces or special characters, or whole-quoted values without `$`, backslash, backtick, the quote character or line breaks; no escapes or multi-line values), tested through both paths; §1 adds G4's conditions (manual steps in the guide, `Not validated`), both languages; `PROVENANCE.md` says "no application-specific ports" |
| `codex-review`, round `14-devenv-007` | CHANGES REQUESTED, 1 medium finding, fixed in both languages: unquoted values are limited to letters, digits and `_ . - / : , @ + =`; shell metacharacters and a leading `~` tested through both paths |
| `codex-review`, round `14-devenv-008` | CHANGES REQUESTED, 2 medium findings, fixed in both languages: §3 rule 5 requires LF for `.env.example` and `.env`, the `.gitattributes` example enforces it for `.env.example` and the doctor example reports a CRLF `.env`; the Makefile `up` prints how to check readiness when the flags do not include `--wait`, with a new `ps` target |
| `codex-review`, round `14-devenv-009` | APPROVE; 1 low finding fixed in both languages: the doctor example is labelled partial and its success message says `All checks passed.` instead of claiming the environment is ready |
| Commit `864c611` | The stage content above, with the maintainer's approval |
| Maintainer request after the commit | §9 rule 7 added (script modes in Git and `git update-index --chmod=+x` on Windows), with an anti-pattern row and a checklist item, both languages; reviewed again below |
| `technical-documentation` audit of the addition | No findings: the rule matches the `check-exec-bit` hook and the source repository modes; the Windows claim was checked in a scratch repository with `core.fileMode=false` |
| `codex-review` pre-push, round `14-prepush-001` on `864c611` plus the addition | CHANGES REQUESTED, 1 medium and 1 low findings, fixed in both languages: rule 7, the anti-pattern row and the checklist now cover POSIX shell scripts and shell libraries only (PowerShell and batch scripts use neither a shebang nor the mode); the doctor's `.env` line-ending check fails for an unreadable `.env` instead of passing on a `grep` error |
| `codex-review` pre-push, round `14-prepush-002` | CHANGES REQUESTED, 1 medium and 1 low findings, fixed in both languages: §3 rule 5 limits names to letters, digits and underscores, not starting with a digit (a name with `-` is accepted by Compose but breaks the shell, tested); the doctor's line-ending check requires a readable regular file and passes only on `grep` exit status 1 |
| `codex-review` pre-push, round `14-prepush-003` | APPROVE; 1 low finding fixed in both languages: a dangling `.env` symlink no longer counts as an absent `.env`; tested |
| `codex-review` pre-merge, round `14-premerge-001` on head `b3c2889` | APPROVE; 1 low finding fixed in both languages: the bootstrap example treats a dangling `.env` symlink as existing, so `cp` cannot create its target; tested. `gh pr checks 22`: no checks reported (#8) |
| `codex-review` pre-merge, round `14-premerge-002` on head `8ee5e7f` | APPROVE; 1 low finding: this record and the iteration README still listed the pull request as pending. Fixed after the merge in this closure record. `gh pr checks 22`: no checks reported (#8) |
| `codex-review` of the stage and iteration closure records, round `14-close-001` | APPROVE, no findings: the iteration closure criteria are met and the records match the stage 04 format |

### Out-of-scope findings for the source repository's maintainer

- Its macOS scripts' comments and the doctor hint point to an organization repository's controller setup.
- Its macOS scripts mix languages (two in Portuguese, one in English); under §10 they use one language, English.
- It needs a language map in its agent instructions (documentation standard).
- Its VM has no doctor and no setup command; its `setup`, `doctor` and `bootstrap` run on macOS only.
- Its decision to leave Windows without a script becomes a recorded exception there (§1, G4).
- Its guides declare no validation state; Windows has no guide.
- Its VM provisioning installs a system Maven that the documented path does not use.

For the maintainer's public `ci-workflows` repository: the hook names and descriptions in `.pre-commit-hooks.yaml` are in Portuguese, while §10 asks for English tooling.

### Pull request

[#22](https://github.com/ednillibanio/app-catalog/pull/22), three commits (`864c611`, `b3c2889`, `8ee5e7f`). No hosted checks exist yet (#8); `gh pr checks 22` reported none.

### Merge and pending

Merged with the maintainer's approval on 2026-11-14 as squash commit `ea93180` on `main`. Closing #14 with a comment and ticking stage 05 in the #16 checklist each need a separate approval. The out-of-scope findings above belong to other repositories and are reported there.
