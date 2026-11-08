# Stage 02: reusable CI

Status: `todo`

Create public `ednillibanio/ci-workflows` with new history, `main`, Apache 2.0, English docs and provenance. Adapt three hooks and tests: allow `.env.example` and `.env.prod.example`, block real environment files, and check executable bits and shell headers. Publish versioned hooks and reusable workflows for hygiene, full-history secrets, PR titles, Quarkus/Maven tests, pnpm build/lint/test, SAST, dependency checks and separate CycloneDX SBOMs. Document stable names, inputs, outputs, tools and failure behavior.

Use hosted runners, read-only tokens, pinned actions and Trivy, no inherited secrets for PR code; caller supplies paths and versions and pins full SHAs. Called workflow checkout must retrieve the caller repository. Test `pom.xml` and `pnpm-lock.yaml` detection, YAML and `actionlint`; exercise each workflow with test callers, distinguish scanner failures from findings, check coverage and artifacts. Publish a version and record evidence. Real sapl-next PR validation belongs to stage 03 and iteration closure. No images, deploy, Sonar or environment installers.

## Result, evidence and pending work

Pending.
