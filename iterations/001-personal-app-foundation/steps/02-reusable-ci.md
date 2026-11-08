# Stage 02: reusable CI

Status: `done`

Create public `ednillibanio/ci-workflows` with new history, `main`, Apache 2.0, English docs and provenance. Adapt three hooks and tests: allow `.env.example` and `.env.prod.example`, block real environment files, and check executable bits and shell headers. Publish versioned hooks and reusable workflows for hygiene, full-history secrets, PR titles, Quarkus/Maven tests, pnpm build/lint/test, SAST, dependency checks and separate CycloneDX SBOMs. Document stable names, inputs, outputs, tools and failure behavior.

Use hosted runners, read-only tokens, pinned actions and Trivy, no inherited secrets for PR code; caller supplies paths and versions and pins full SHAs. Called workflow checkout must retrieve the caller repository. Test `pom.xml` and `pnpm-lock.yaml` detection, YAML and `actionlint`; exercise each workflow with test callers, distinguish scanner failures from findings, check coverage and artifacts. Publish a version and record evidence. Real sapl-next PR validation belongs to stage 03 and iteration closure. No images, deploy, Sonar or environment installers.

## Result, evidence and pending work

Completed 2026-11-08. `ednillibanio/ci-workflows` was merged in PRs [#2](https://github.com/ednillibanio/ci-workflows/pull/2) and [#3](https://github.com/ednillibanio/ci-workflows/pull/3). Hook release `v0.1.0` points to `d9e8db92a2a88f5a69460d9d635bc25adf37432e`. PR #3 added test callers for secrets and SAST and corrected the public setup and provenance docs.

Validation: all 11 GitHub checks passed on PR #3, covering all nine reusable workflows and the separate PR-title caller. The SBOM workflows uploaded their artifacts. Local `./tests/test_hooks.sh` passed all 18 cases, `pre-commit run --all-files` passed, all workflow YAML parsed, and the final documentation review and Codex review passed.

Pending for iteration closure: exercise the published workflows in a real sapl-next PR, including a documentation-only PR and the scanner failure/finding behavior; compare with `make check` and reconcile remaining issues. These are tracked in stage 03 and the iteration closure criteria.
