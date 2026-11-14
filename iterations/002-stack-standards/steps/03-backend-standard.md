# Stage 03: backend standard

Status: `todo`

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

Pending.
