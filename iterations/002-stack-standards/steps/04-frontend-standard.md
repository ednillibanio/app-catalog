# Stage 04: frontend standard

Status: `done`

## Objective and scope

Write `docs/standards/react-vite-frontend.md` and `react-vite-frontend.pt-BR.md`, a shared standard for React/Vite/TypeScript applications in a pnpm and Turborepo monorepo, rewritten from the generic parts of the maintainer's existing frontend standard in a private application repository. Index it in the standards README and the root README, in both languages, and record the source in `PROVENANCE.md` as in stage 03. Tracked in [#13](https://github.com/ednillibanio/app-catalog/issues/13). The plan, with the full source classification, is kept outside this repository; the Evidence section maps every source subsection.

Decisions approved by the maintainer on 2026-11-14:

- F1: file `docs/standards/react-vite-frontend.md` and its `.pt-BR.md`, title "React/Vite frontend", in the style of the backend standard: a reciprocal language switch first, and an opening paragraph that points to "Using these standards" in the standards README.
- F2: the generic rules are rewritten, not copied. `PROVENANCE.md` records the source as the maintainer's private application repository (not public), revision `f9f3597`, its frontend standard, first-party content, without naming the application.
- F3: examples use the backend standard's neutral `inventory` module and `Item` entity, English identifiers and the placeholder package scope `@<scope>/`. Each application chooses its identifier language and keeps one vocabulary.
- F4: the standard pins no version. Where a rule depends on a major line (Tailwind CSS v4 CSS-first configuration, React Router v7 framework mode), it says so, and an application on another line records a deviation. Each application pins exact versions in its own files.
- F5: the design system section keeps semantic token names and rules only. Palette, typography, spacing, breakpoint, layout and component style values are brand decisions that stay in the application.
- F6: tests have a required minimum (Zod schemas, pure utilities, SSR loaders and helpers, and real-time handlers and client stores when the application has them); component and hook tests are the application's choice.
- Code blocks are identical in both languages; only prose is translated (as stage 03, E5).

## Out of scope

Application-specific rules (application names, ports, package scope, palette values, identity-provider realms), the local development environment rules (stage 05, including the `.npmrc` symlink settings) and any change in the application repository.

## Acceptance criteria and validation

No application-specific name or data in the standard (case-insensitive search with a private terms list kept outside this repository, plus a manual read). The TypeScript examples are type-checked in a scratch directory outside both repositories. At stage start, the git history of the source file was checked on 2026-11-14: every commit is first-party. Linux and Windows are not claimed as validated.

## Result, evidence and pending work

### Changes

- New `docs/standards/react-vite-frontend.md` and `react-vite-frontend.pt-BR.md`, sections 1–13.
- `docs/standards/README.md` and `README.pt-BR.md`: new row; root `README.md` and `README.pt-BR.md` name the frontend standard among the topics.
- `PROVENANCE.md`: new private first-party row with revision `f9f3597`.
- Stage 03 closed (`done`, PR #20, merge `87afa36`); iteration table rows 03 `done` and 04 `doing`.

### Source mapping

Every numbered subsection of the source is either in the catalog or stays local. "Adapted" marks a deliberate change from the source.

| Source | Catalog | Stays local / adaptation |
| --- | --- | --- |
| 1 Canonical stack | §1.1 | Exact versions, package scope, identity-provider adapter and realms (F4). Adapted: Playwright as the application's choice instead of "future" |
| 1 Prohibited | §1.2 | — |
| 2 Monorepo structure | §2 | App names and ports; `.npmrc` `node-linker=hoisted`, `symlink=false` and the "no symlinks" rule, which exist for one development environment (stage 05) |
| 3.1 SPA layout | §3.1 | Sub-resource example |
| 3.2 Feature convention | §3.2 rules 1–8 | Hook names. Adapted: query keys carry a kind (`"list"`, `"detail"`); URLs built with `URLSearchParams` and `encodeURIComponent` |
| 3.3 Forms | §3.3 | Adapted: the labelled field component is named generically, because the source names a component its UI package lacks |
| 3.4 Zod schemas | §3.4 | Adapted: messages in the app's interface language instead of a fixed language; limits match the backend validation; rule 4 adds the `useForm` input and output types for `z.coerce` |
| 3.5 Tables | §3.5 | — |
| 3.6 Routing | §3.6 | Guard file path. Adapted: the client guard is stated as a convenience, not access control |
| 3.7 State | §3.7 | — |
| 4.1 SSR layout | §4.1 | Domain route names |
| 4.2 Loaders | §4.2 rules 1–6 | Public endpoint, helper map names. Adapted: the loader validates the page parameter and encodes query values |
| — (not in source) | §4.3 authenticated SSR | Added: server-side authentication and authorization, request-scoped data, `Cache-Control`, CSRF, tests |
| 4.3 Vite and Vitest | §4.4 | Adapted: the config adds `/// <reference types="vitest/config" />` so the `test` key type-checks |
| 5.1 Types | §5.1 | Adapted: same pull request when backend and frontend share a repository, otherwise a linked follow-up |
| 5.2 API client | §5.2 | 10 s timeout value, error body field name, `isNotFound` treating 403 as not found. Adapted: download and server-sent event helpers named as part of the package |
| 5.3 UI package | §5.3 rules 1–7 (source rules 1–7) and 9 (source rule 8) | Component inventory and app-local components. Adapted: `forwardRef` only where the React version requires it; source rule 8 ("no Storybook yet") becomes rule 9, a visual catalog only by the application's recorded decision; rule 8, injected link components, is added from the source inventory |
| 5.4 Auth | §5.4 | Keycloak adapter, realms. Adapted: provider-neutral OpenID Connect; provider, `useAuth`, factory and token getter; SSR-safe context separate from the browser adapter (from the source implementation) |
| 5.5 Config | §5.5, §8 rule 1 | Adapted: client configuration stated as public |
| 6.1 Principles | §6.1 | Product characterization ("data-heavy administrative system") |
| 6.2 Palette | §6.2 semantic token names | All hex values and dark-mode values (F5) |
| 6.3 Typography | §6.3 rule | Font and sizes (F5) |
| 6.4 Spacing | §6.3 rule (4 px grid) | Spacing values (F5) |
| 6.5 Grid and breakpoints | §6.3 rule | Columns, container width, breakpoints (F5) |
| 6.6 Layouts | §6.3 rule | Layout dimensions (F5) |
| 6.7 Component styles | §6.1 (tokens only) | Radii, padding, heights, weights (F5) |
| 6.8 `@theme` | §6.4 with placeholder values | The full token block (F5) |
| 6.9 Utility classes | §6.5 | — |
| 7.1 Types | §7.1 | OpenAPI path (covered by the backend standard §10.2) |
| 7.2 Error handling | §7.2 | Message text. Adapted: 403 shows a forbidden state instead of a login redirect; the example is a mutation hook instead of a direct client call in a component |
| — (not in source) | §8 Security | Added: public client configuration, URL encoding, `dangerouslySetInnerHTML` only with trusted or sanitized content, JSON-LD escaping, no tokens in web storage |
| 8.1 SPA tests | §9.1 | Adapted: a required minimum; component and hook tests optional (F6) |
| 8.2 SSR tests | §9.1, §9.2 | Domain file names. Adapted: real-time handlers and client stores added to the minimum (present in the source implementation, not in its standard) |
| 8.3 Commands | §9.3 | Package names |
| 9.1 Biome | §10.1 | Line width (the application's `biome.json` decides) |
| 9.2 Build | §10.2 | Package names |
| 9.3 Dev | §10.2 | Ports |
| 10.1 Accessibility | §11.1 | `<FormField>` name |
| 10.2 i18n | §11.2 | Adapted: the application states its interface language |
| 11 Anti-patterns | §12 | `.npmrc` row, `<FormField>` name. Added rows for secrets, URL encoding, JSON-LD and 403 |
| 12.1 Iteration pre-reading | — | Local process |
| 12.2 PR checklist | §13 | Package names. Added: deviation rule as in the backend standard, security and SSR items |

### Validation

| Check | Result |
| --- | --- |
| `python3 scripts/check_docs.py` | `OK: 11 language pairs, 34 Markdown files` |
| Pair comparison (scripted) | 18 fenced blocks in each file, identical; 46 headings in each; `§` references identical |
| TypeScript examples | The 10 `ts`/`tsx` blocks extracted by a script into a scratch directory outside both repositories, with stubs for the `@<scope>/*` packages and `@/`, `~/` aliases, and the libraries installed in the source repository's frontend; `tsc --noEmit --strict` exit 0. A deliberately broken file in the same setup failed with the expected errors, so the check is not vacuous. The JSON-LD test example ran with Vitest: 1 passed. Not built or run inside an application |
| Private-terms search: `grep -n -i -E -f <terms file>` over both new files, `PROVENANCE.md` and the four indexes, with the stage 03 list extended with the source's frontend names (apps, ports, components, helpers, palette hex values) and kept outside this repository | Both files: `ItemStatusBadge`, the neutral example of a domain component name, kept. Portuguese file, otherwise: only ordinary Portuguese words that equal some private terms (the words for "identity", "operators", "lookup" and "message"), kept. `PROVENANCE.md`: only the existing organization row, kept per stage 02 |
| Manual read of every example and table | No application name, port, palette value, realm or data |
| Source history | `f9f3597` is the source repository head; the file last changed in `bdbfe85`; every commit to it is first-party |
| Spot-check against the source implementation | API client (`createApiClient`, `getToken`, `ApiError`, 204, timeout), config package, auth package exports, SSR `vite.config.ts` and `biome.json` consistent with §5.2, §5.4, §5.5, §4.4 and §10.1 |
| `pre-commit run --all-files` | Passed |
| Hosted checks | None until [#8](https://github.com/ednillibanio/app-catalog/issues/8) |

### Reviews

| Review | Result |
| --- | --- |
| `technical-documentation` audit (plan) | 5 findings, all applied to the plan: JSON-LD escaping; type-checking the examples instead of review only; auth package shape; transport helpers in the API client; language switch and opening paragraph |
| `codex-review` plan, round `plano-13-frontend-001` | CHANGES REQUESTED, 3 findings, applied: 403 shows a forbidden state; authenticated SSR boundaries (request-scoped data, cache control, CSRF); SSE handlers and stores tested for logic and side effects |
| `codex-review` plan, round `plano-13-frontend-002` | CHANGES REQUESTED, 2 findings, applied: the JSON-LD escape sequence written correctly; server-side authentication and authorization for protected SSR loaders and actions, with tests |
| `codex-review` plan, round `plano-13-frontend-003` | APPROVE; 1 low finding applied: serialized output distinguished from the JavaScript literal, with a round-trip check |
| `technical-documentation` audit (stage end) | 1 low finding, fixed in both languages: §3.4 rule 4 states that a `z.coerce` schema passes its input and output types to `useForm` (pattern type-checked with `tsc --noEmit --strict`, exit 0). Other claims checked against the source implementation and the type-check; no other index lists the standards |
| `codex-review --base origin/main`, round `13-frontend-004` (the counter is shared with the plan topic) | CHANGES REQUESTED, 2 medium findings, fixed: the §8 prose showed the escape as `<` because an editing tool collapsed it; both languages now state the literal six-character escape, and the code was already correct. Source UI rule 8 (Storybook) was dropped; restored as §5.3 rule 9 and the mapping corrected |
| `codex-review`, round `13-frontend-005` | CHANGES REQUESTED, 2 medium and 1 low findings, all fixed in both languages: §8 rule 1 states Vite's default exposure (the `VITE_` prefix and built-in values) and warns that `define` or a changed prefix can inject more; the opening paragraph states F3 (each application chooses its identifier language and keeps one vocabulary); the 403 explanation says a login redirect can loop, not that it always does |
| `codex-review`, round `13-frontend-006` | CHANGES REQUESTED, 1 medium finding, fixed in both languages: `encodeURIComponent` leaves `.` and `..` unchanged, so §8 rule 2 now requires validating a path value against its expected format (rejecting dot segments) before encoding it; §3.2 rule 7, the anti-pattern row and the checklist point to it |
| `codex-review`, round `13-frontend-007` | APPROVE, no findings |
| `codex-review` pre-push, round `13-prepush-001` on `7e83055` | CHANGES REQUESTED, 1 medium finding, fixed in both languages: the detail and delete examples encoded a `number` ID without runtime validation; a new `itemPath` helper in §3.2 rejects non-integer and non-positive IDs before encoding, and both hooks use it. Type-check, pair comparison, `check_docs` and pre-commit rerun: pass |
| `codex-review` pre-push, round `13-prepush-002` on the fix | APPROVE; 2 low findings fixed: §3.2 allows the small helpers the hooks share (both languages); a missing sentence break in the English note after the §7.2 example |
| `technical-documentation` audit (pre-merge) | No findings: the `8bc4a7e` diff checked against the type-checked examples and the §3.2 reference |
| `codex-review --base origin/main` pre-merge, round `13-premerge-001` on head `8bc4a7e` | APPROVE, no findings; `check_docs` rerun: pass |

### Out-of-scope findings for the source repository's maintainer

- Its frontend standard §10.1 and §11 name a `<FormField>` component that its UI package does not export.
- One app reads `import.meta.env` directly, against its own rule.
- Its JSON-LD component writes `JSON.stringify` output into a `<script>` without escaping `<`.
- Its standard redirects 403 to login.
- Its standard does not cover the real-time handlers and client stores its apps have.

With the maintainer's approval, these were recorded in that repository's own issue tracker: one issue for the JSON-LD escaping (security) and one for the triage of the others, together with stale records found there.

### Pull request

[#21](https://github.com/ednillibanio/app-catalog/pull/21), two commits (`7e83055`, `8bc4a7e`). No hosted checks exist yet (#8); `gh pr checks 21` reported none.

### Merge and pending

Merged with the maintainer's approval on 2026-11-14 as squash commit `9117779` on `main`. With separate approvals, #13 was closed with a comment and stage 04 was ticked in the #16 checklist. Nothing pending.
