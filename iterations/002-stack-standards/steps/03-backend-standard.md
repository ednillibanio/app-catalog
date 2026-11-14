# Stage 03: backend standard

Status: `doing`

## Objective and scope

Write `docs/standards/java-quarkus-backend.md` and `java-quarkus-backend.pt-BR.md`, a shared standard for Java/Quarkus/Maven applications, rewritten from the generic parts of the maintainer's existing backend standard in a private application repository. Index it in the standards README and record the source in `PROVENANCE.md` as a private first-party source with the revision consulted, without naming the application. Tracked in [#12](https://github.com/ednillibanio/app-catalog/issues/12). The source classification is detailed in this file at stage start.

Decisions approved by the maintainer on 2026-11-14:

- E1: file `docs/standards/java-quarkus-backend.md` and its `.pt-BR.md`, so standards for other stacks can be added without renaming.
- E2: the generic rules are rewritten, not copied, from the maintainer's private backend standard. `PROVENANCE.md` records the source as the maintainer's private application repository (not public), revision `16d51b2`, first-party content, without naming the application. Code examples use a neutral entity and English identifiers.
- E3: each application chooses the language of its code identifiers; the standard requires one consistent vocabulary for repository methods, DTOs and exceptions and shows English names.
- E4: the standard names the stack and requires each application to pin exact versions in its own build files; it pins no version itself.
- E5: code blocks are identical in both languages; only prose is translated.

## Out of scope

Application-specific rules (packages, modules, table prefixes, namespaces, realms, roles, seeds, versions) and any change in the application repository.

## Acceptance criteria and validation

No application-specific name or data in the standard (case-insensitive search with a private terms list kept outside this repository, plus a manual read). At stage start, check the git history of the source file: material adapted from organization sources is not copied (`PROVENANCE.md`); it is rewritten from the implementation or left out. For this source, the history check on 2026-11-14 found only first-party commits. Linux and Windows are not claimed as validated.

## Result, evidence and pending work

### Changes

- New `docs/standards/java-quarkus-backend.md` and `java-quarkus-backend.pt-BR.md`, sections 1–12 in the source order.
- `docs/standards/README.md` and `README.pt-BR.md`: new row; root `README.md` and `README.pt-BR.md` name the backend standard among the topics.
- `PROVENANCE.md`: new private first-party row with revision `16d51b2`.
- Stage 02 closed (`done`, PR #19, merge `9525a88`); iteration table rows 02 `done` and 03 `doing`.

### Source mapping

Every numbered subsection of the source is either in the catalog or stays local. "Adapted" marks a deliberate change from the source.

| Source | Catalog | Stays local / adaptation |
| --- | --- | --- |
| 1.1 Versions | §1.1 components | Exact versions, cache backend, identity-provider admin client (E4) |
| 1.2 Annotations, prohibited packages | §1.2 | Adapted: cache annotations apply only when the app uses Quarkus Cache |
| 2.1 Package layout | §2.1 | Base package, namespace-specific resource names |
| 2.2 Dependency rule | §2.2 | — |
| 2.3 Cross-module references | §2.3 | Concrete entity examples |
| 2.4 Existing modules | §2.4 rule: one prefix per module that owns tables | Module and prefix list |
| 3.1 Entities | §3.1 rules 1–9 | Audit field names, the exception comment text, the one-line getter layout. Adapted: exceptions to the audit base are app decisions, not automatic |
| 3.2 Repository interface | §3.2 | Method names in the app's language (E3). Adapted: names must not collide with Panache methods |
| 3.3 Domain exceptions | §3.3 | Exception class names and error body field names. Adapted: error body shape decided per app |
| 4.1 Service | §4.1 | — |
| 4.2 DTOs | §4.2 | Naming examples |
| 4.3 Mapper | §4.3 | — |
| 5.1 Repository implementation | §5.1 | — |
| 5.2 Panache | §5.2 | — |
| 5.3 Native queries | §5.3 | The source's table and query example |
| 6.1 Namespaces | §6.1 rule: namespaces by prefix with explicit auth | Prefixes, realms, roles, special endpoints |
| 6.2 Resource naming | §6.2 prefix rule and "keep older names" | Namespace-specific names and listed exceptions |
| 6.3 Resource structure | §6.3 | — |
| 6.4 Resource rules | §6.4 | Names of resources still to convert |
| 6.5 Page wrapper | §6.5 | Class name and package |
| 6.6 User identity | §6.6 | Service name, application-specific claim |
| 7.1 Schema | §7.1 | Example tables, audit column names |
| 7.2 Flyway | §7.2 | The one-time seed repair exception and paths. Adapted: an app documents its own one-time exception |
| 7.3 Auditing | §7.3, §3.1 | Base class name |
| 8.1 Authentication | §8.1 | Provider version, realms, tenant resolver |
| 8.2 Roles | §8.2 rule: the app documents its roles | Role table and assignment steps |
| 8.3 Authorization | §8.3 | Ownership examples |
| 8.4 Security rules | §8.4 | Environment variable name |
| 8.5 Sensitive fields | §8.5 | Audit field names |
| 8.6 Audit trail | §8.6 | Service name |
| 8.7 CORS | §8.7 | Environment variable name |
| 9.1 Test types | §9.1 | Adapted: Testcontainers or a dedicated test database |
| 9.2–9.3 Test examples | §9.2, §9.3 | — |
| 9.4 Test rules | §9.4 | Test database name, application-specific claim example, module-specific order issue, reference to a local pre-reading file |
| 9.5 Commands | §9.5 | — |
| 10.1 Logging | §10.1 | Adapted: personal data masked at every level, including DEBUG (the source allowed DEBUG) |
| 10.2 OpenAPI | §10.2 | Adapted: coordination stated as conditional on a frontend generating types |
| 10.3 Health | §10.3 | — |
| 11 Anti-patterns | §11 | Frontend formatting row; audit field names |
| 12.1 Iteration pre-reading | — | Local process |
| 12.2 PR checklist | §12 | — |
| 12.3 Conformance refactoring | — | Local audit files |
| Appendices A–C | — | Migration list, table reference and endpoint catalog |
| Agent rule: one `application.properties` with profiles | §7.4 and anti-pattern row | — |

### Validation

| Check | Result |
| --- | --- |
| `python3 scripts/check_docs.py` | `OK: 10 language pairs, 32 Markdown files` |
| Code blocks identical across the pair (scripted comparison of all fenced blocks) | 16 blocks, identical |
| Private-terms search: `grep -n -i -E -f <terms file>` over both new files, `PROVENANCE.md` and both indexes, with the terms list kept outside this repository | English file: no match. Portuguese file: matches only ordinary Portuguese words in prose that equal some private terms (for example the words for "audit", "identity" and "query"); none is an identifier or a module name, kept. `PROVENANCE.md`: only the existing organization row, kept per stage 02 |
| Manual read of every example and table | No application name, table, role, realm, person or data |
| Source history | `16d51b2` unchanged at the source head; every commit to the source file is first-party |
| Spot-check against the source application's code (audit base class, page wrapper, global exception mapper) | Consistent with §3.1, §3.3 and §6.5 |
| Java snippets | Reviewed for the stated stack, not compiled. Repository method names changed from the plan's draft to avoid a compile error with Panache's `findById`, `count` and `delete` |
| `pre-commit run --all-files` | Passed |
| Hosted checks | None until [#8](https://github.com/ednillibanio/app-catalog/issues/8) |

### Reviews

| Review | Result |
| --- | --- |
| `codex-review` plan, rounds `plano-12-backend-001`..`007` (written before stages were renumbered, when this stage was 02) | Rounds 001–006 CHANGES REQUESTED, each fixed in the plan; round 007 APPROVE. The plan is kept outside this repository |
| `technical-documentation` audit (plan) | No record survives from the earlier session; not claimed. The stage-end audit below covers the result |
| `technical-documentation` audit (stage end) | 2 findings, fixed: the create example did not set the required `code` and carried a field the entity lacked; the root READMEs did not list the backend standard |
| `codex-review --base origin/main`, round `12-backend-008` (the counter is shared with earlier topics) | CHANGES REQUESTED, 7 findings, all fixed in both languages: create example (same as the audit); method-level `@RolesAllowed` replaces the class annotation instead of narrowing it; the `javax.*` ban now covers only Java EE packages replaced by Jakarta; the native-query method is declared in the interface; user search text goes to `websearch_to_tsquery`; the dependency diagram no longer points from `application` to `infrastructure`; the Swagger UI is stated as dev/test only by default |
| `codex-review`, round `12-backend-009` | CHANGES REQUESTED, 4 findings, all fixed in both languages: output encoding and an allowlist sanitizer for untrusted text (§8.4); validated `page` and bounded `size` (§6.3, §6.4); audit columns only on tables of audited entities (§7.1, §7.3); a deviation records the exception fields of the standards index (§12). The pagination bounds are stricter than the source |
| `codex-review`, round `12-backend-010` | CHANGES REQUESTED, 3 findings, all fixed in both languages: bound parameters required for Panache and JPQL too, with allowlisted dynamic identifiers (§8.4); a maximum `page` so the offset fits in an `int` (§6.3, §6.4); the service example records audit events through `AuditTrail` and its unit test mocks it (§4.1, §8.6, §9.2) |
| `codex-review`, round `12-backend-011` | CHANGES REQUESTED, 1 finding, fixed in both languages: the update request rejected a blank supplied name (`@Pattern`), with the rule stated in §4.2 |
| `codex-review`, round `12-backend-012` | CHANGES REQUESTED, 2 findings, fixed in both languages: the `@Pattern` did not match `@NotBlank`, so the PUT update request now uses `@NotBlank` and §4.2 states the PATCH case; disabling OIDC is limited to tests that use `@TestSecurity`, with real token validation in a separate profile (§9.4). Adapted: the source required `%test.quarkus.oidc.enabled=false` for the whole test profile |
| `codex-review`, round `12-backend-013` | CHANGES REQUESTED, 2 findings, fixed in both languages: request bodies carry `@NotNull @Valid` (§6.3, §6.4); the summary test command keeps Maven's exit status with `pipefail` (§9.5) |
| `codex-review`, round `12-backend-014` | CHANGES REQUESTED, 1 finding: the plan reviews were not recorded; added above |
| `codex-review`, round `12-backend-015` | APPROVE, no findings |
| `codex-review` pre-push, round `12-prepush-001` on `46465ce` | APPROVE, no findings |
| `technical-documentation` audit (pre-push) | Not rerun: the content is the stage-end audit's plus the fixes reviewed by Codex rounds 008–015 |

### Pull request

[#20](https://github.com/ednillibanio/app-catalog/pull/20), from commit `46465ce`. `gh pr checks 20`: no hosted checks until [#8](https://github.com/ednillibanio/app-catalog/issues/8).

### Pending

- Merge #20 (with approval); then this stage becomes `done`.
- Close #18 and tick stages 02 and 03 in the #16 checklist (each with its own approval).
