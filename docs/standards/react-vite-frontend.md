English | [Português](react-vite-frontend.pt-BR.md)

# React/Vite frontend

This standard applies to web frontends built with React, Vite and TypeScript in a pnpm and Turborepo monorepo. It sets the structure, data access, forms, state, shared packages, design tokens, security, test and tooling rules that application repositories on this stack share. An application records its own apps, ports, package scope, design values, exact versions and stricter rules in its own repository, as described in [Using these standards](README.md#using-these-standards).

The examples use the neutral `inventory` module and `Item` entity of the [Java/Quarkus backend](java-quarkus-backend.md) standard, the placeholder package scope `@<scope>/` and English identifiers. Each application chooses the language of its identifiers and keeps one vocabulary for hooks, schemas, types and components. The examples illustrate the rules; they are type-checked when this standard changes, but they are not built or run as part of this catalog.

## 1. Stack

### 1.1 Components

| Layer | Technology |
| --- | --- |
| Language | TypeScript in strict mode |
| UI library | React |
| Build and dev server | Vite |
| Routing | React Router: library mode for single-page apps, framework mode for server-rendered (SSR) apps |
| Packages | pnpm workspaces and Turborepo |
| Lint and format | Biome, the only lint and format tool |
| Styling | Tailwind CSS with CSS-first configuration (`@theme`) |
| UI components | A shared UI package built with Tailwind and CVA (`class-variance-authority`) |
| Server state | TanStack Query |
| Client state | Zustand, only when justified (§3.7) |
| Forms | React Hook Form with Zod |
| Tables | TanStack Table |
| Tests | Vitest; Playwright when the application adds end-to-end tests |

This standard pins no version. Each application pins exact versions in its own files: Node.js (for example in `.nvmrc`), pnpm through the `packageManager` field, and every dependency in `package.json` and the lockfile. Some rules depend on a major line: CSS-first configuration needs Tailwind CSS v4 or later, and the SSR rules use React Router v7 framework mode. An application on another major line records a deviation (§13).

### 1.2 Prohibited

- ESLint or Prettier: Biome covers both.
- A `tailwind.config.js` or `tailwind.config.ts` file: design tokens go in `@theme` in CSS (§6.4).
- Redux, MobX or Recoil: Zustand is the only client-state library.
- shadcn/ui components copied into an app: wrap them in the shared UI package (§5.3).
- Form libraries other than React Hook Form, such as Formik.
- Validation libraries other than Zod.
- Single quotes and indentation other than two spaces: Biome enforces double quotes and two spaces.

## 2. Monorepo structure

```text
frontend/
├── apps/
│   ├── <spa-app>/          ← single-page app (Vite, React Router library mode)
│   └── <ssr-app>/          ← server-rendered app (React Router framework mode)
├── packages/
│   ├── api-client/         ← HTTP client, ApiError, transport helpers
│   ├── auth/               ← OpenID Connect client wrapper
│   ├── config/             ← typed runtime configuration
│   ├── types/              ← DTOs mirrored from the backend
│   └── ui/                 ← shared Tailwind and CVA components and tokens
├── biome.json
├── package.json
├── pnpm-workspace.yaml
└── turbo.json
```

Every package is named `@<scope>/<name>`. Apps import packages through the workspace and resolve their sources through Vite aliases and TypeScript `paths`. The root `biome.json` and `turbo.json` apply to the whole monorepo.

## 3. Single-page apps

### 3.1 Source layout

```text
apps/<spa-app>/src/
├── main.tsx              ← entry point
├── App.tsx               ← routes
├── components/           ← components shared inside the app (auth guard, icons)
├── features/             ← one directory per feature (§3.2)
│   └── <feature>/
│       ├── api.ts                ← TanStack Query hooks
│       ├── <Feature>Form.tsx     ← form (React Hook Form and Zod)
│       └── <sub-resource>-api.ts ← hooks for a sub-resource, when needed
├── pages/                ← one directory per feature, screens that use features/
│   └── <feature>/
│       ├── <Feature>ListPage.tsx
│       ├── <Feature>FormPage.tsx
│       └── <Feature>DetailPage.tsx
├── schemas/              ← one Zod schema per entity, with its test beside it
├── layouts/
├── lib/
│   └── api.ts            ← the app's API client instance
└── styles/               ← global CSS with the app's @theme overrides
```

### 3.2 Features and data hooks

Each backend resource that the app manages has a `features/<feature>/` and `pages/<feature>/` pair. `features/<feature>/api.ts` holds TanStack Query hooks and nothing else:

```ts
import { apiClient } from "@/lib/api";
import type { ItemCreateRequest, ItemDto, PagedResponse } from "@<scope>/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

const ITEMS_KEY = "items";

export function useItems(page = 0, size = 20) {
  return useQuery({
    queryKey: [ITEMS_KEY, "list", page, size],
    queryFn: () => {
      const params = new URLSearchParams({ page: String(page), size: String(size) });
      return apiClient.get<PagedResponse<ItemDto>>(`/api/admin/items?${params}`);
    },
  });
}

export function useItem(id: number) {
  return useQuery({
    queryKey: [ITEMS_KEY, "detail", id],
    queryFn: () => apiClient.get<ItemDto>(`/api/admin/items/${encodeURIComponent(id)}`),
  });
}

export function useCreateItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ItemCreateRequest) => apiClient.post<ItemDto>("/api/admin/items", data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: [ITEMS_KEY] }),
  });
}
```

Rules:

1. Hooks are named `use<Verb><Resource>`: `useItems`, `useItem`, `useCreateItem`, `useUpdateItem`, `useDeactivateItem`.
2. Paginated list hooks take `page` and `size` with defaults.
3. Query keys are constants at the top of the file.
4. Query key variants are tuples that start with the constant and a kind: `[ITEMS_KEY, "list", page, size]`, `[ITEMS_KEY, "detail", id]`. Invalidating `[ITEMS_KEY]` then covers every variant.
5. Every mutation invalidates the query keys it affects in `onSuccess`; do not rely on a manual `refetch`.
6. Backend types come from `@<scope>/types` (§5.1); do not declare them in the app.
7. A hook writes its URL directly, which keeps it self-contained; there is no separate "endpoints" layer. Query strings are built with `URLSearchParams` and path values are validated and encoded as stated in §8.
8. Components never call the API client directly; they use a hook.

### 3.3 Forms

A form lives in `features/<feature>/<Feature>Form.tsx`:

```tsx
import { type ItemFormData, itemSchema } from "@/schemas/item.schema";
import { zodResolver } from "@hookform/resolvers/zod";
import { AppButton, Input } from "@<scope>/ui";
import { useForm } from "react-hook-form";

export type ItemFormProps = {
  defaultValues?: Partial<ItemFormData>;
  onSubmit: (data: ItemFormData) => void;
};

export function ItemForm({ defaultValues, onSubmit }: ItemFormProps) {
  const form = useForm<ItemFormData>({
    resolver: zodResolver(itemSchema),
    defaultValues,
  });
  const { errors } = form.formState;

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} noValidate>
      <Input label="Code" error={errors.code?.message} {...form.register("code")} />
      <Input label="Name" error={errors.name?.message} {...form.register("name")} />
      <AppButton type="submit">Save</AppButton>
    </form>
  );
}
```

Rules:

1. The Zod schema lives in `src/schemas/<entity>.schema.ts` (§3.4).
2. The form data type is `z.infer` of the schema, exported next to it.
3. Every form uses `zodResolver`.
4. Validation lives in the schema; `onSubmit` adds no ad hoc checks.
5. Fields use the shared UI package's input components, which associate a visible label and the error message with the control (§11.1). When a component is missing, add it to the UI package instead of writing a raw `<input>`.

### 3.4 Zod schemas

```ts
// src/schemas/item.schema.ts
import { z } from "zod";

export const itemSchema = z.object({
  code: z.string().trim().min(1, "Code is required").max(50),
  name: z.string().trim().min(1, "Name is required").max(200),
});

export type ItemFormData = z.infer<typeof itemSchema>;
```

Rules:

1. Each schema has `<entity>.schema.test.ts` beside it, with valid and invalid cases.
2. Messages are written in the app's user interface language, because users read them.
3. Optional and nullable fields match the backend request exactly (`.optional()`, `.nullable()`); the schema does not invent rules the backend lacks, and its limits match the backend's validation.
4. A numeric field that arrives as a string from `<input type="number">` is parsed with `z.coerce.number()` or registered with `valueAsNumber: true`. When a schema's input and output types differ, as with `z.coerce`, the form passes both to `useForm`: `useForm<z.input<typeof itemSchema>, unknown, z.output<typeof itemSchema>>`.

### 3.5 Tables

- Use the shared `DataTable` component (TanStack Table) from the UI package; extend it there when a table needs new behavior.
- Define the `ColumnDef<T>[]` columns in the page component.
- Paginate on the server through the list hook's `page` and `size`. Do not load every row and paginate in the browser.

### 3.6 Routing

- Declare routes in one place (`App.tsx`) with `createBrowserRouter` or `<Routes>`.
- Wrap protected routes in the app's auth guard component. The guard sends a signed-out user to sign in; it is a user-experience convenience, and the backend enforces access on every request.
- Load large pages lazily with `import()`.

### 3.7 State

| State | Where it lives |
| --- | --- |
| Server data (cache) | TanStack Query |
| Form fields | React Hook Form |
| Local UI state, such as an open dialog | `useState` |
| State shared across pages | Zustand, only when justified |
| Filters, sorting and pagination that a link should keep | URL search parameters (`useSearchParams`) |

Do not copy server data into Zustand or `useState`: TanStack Query is the source of truth for server state.

## 4. Server-rendered apps

### 4.1 Source layout

```text
apps/<ssr-app>/app/
├── root.tsx
├── routes.ts                ← route declarations
├── routes/
│   ├── home.tsx
│   ├── items.tsx            ← list
│   ├── item-detail.tsx      ← detail
│   └── items.test.ts        ← loader tests (§9.1)
├── components/              ← components specific to this app
├── layouts/
├── lib/
│   ├── api.client.ts        ← requests made in the browser
│   ├── api.server.ts        ← requests made by loaders and actions on the server
│   └── seo.ts               ← meta and structured-data helpers
└── styles/
```

### 4.2 Loaders in a public app

A public SSR app renders anonymous content:

```ts
// app/routes/items.tsx
import { apiFetch } from "~/lib/api.server";
import type { ItemDto, PagedResponse } from "@<scope>/types";
import type { LoaderFunctionArgs } from "react-router";

export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const requestedPage = Number(url.searchParams.get("page") ?? "0");
  const page = Number.isInteger(requestedPage) && requestedPage >= 0 ? requestedPage : 0;
  const params = new URLSearchParams({ page: String(page), size: "20" });
  const category = url.searchParams.get("category");
  if (category) {
    params.set("category", category);
  }
  const items = await apiFetch<PagedResponse<ItemDto>>(`/api/public/items?${params}`);
  return { items };
}
```

Rules:

1. Loaders call the API through `apiFetch` from `lib/api.server.ts`, never `fetch` directly.
2. A public app's loaders call only the backend's public namespace and send no credentials.
3. The loader reads and validates query parameters and builds the request with `URLSearchParams`.
4. Lookup maps that a page needs (for example, names by ID) are built in the loader, not in the component.
5. The `meta` export builds its tags with the helpers in `lib/seo.ts`.
6. Filtered lists keep their filters in URL search parameters, so back and forward navigation and shared links work.

### 4.3 Authenticated SSR apps

An SSR app that renders content for signed-in users chooses its own authentication mechanism and records it. It also meets these minimum rules:

1. Every protected loader and action authenticates and authorizes the request on the server. A client-side guard is not access control.
2. Credentials and user data are scoped to the request. They are never kept in module-level variables or in a cache shared between users.
3. Personalized responses are sent with `Cache-Control: private, no-store` or a stricter policy.
4. Mutations authenticated by a cookie are protected against cross-site request forgery (CSRF).
5. Tests cover an unauthenticated request and an unauthorized request for each protected loader and action.

### 4.4 Vite and Vitest

The React Router framework plugin does not run under Vitest, so `vite.config.ts` leaves it out in test mode:

```ts
/// <reference types="vitest/config" />
import { reactRouter } from "@react-router/dev/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

export default defineConfig(({ mode }) => ({
  plugins: [tailwindcss(), ...(mode !== "test" ? [reactRouter()] : [])],
  test: { environment: "node", include: ["app/**/*.test.ts"] },
}));
```

## 5. Shared packages

### 5.1 Types

`@<scope>/types` mirrors the backend DTOs one to one.

- Change it in the same pull request as the backend DTO it mirrors whenever both live in one repository; otherwise, in the next frontend change, with a link to the backend change.
- Keep the backend names (`ItemDto`, `ItemCreateRequest`, `PagedResponse`).
- Do not put frontend-only types here: a form data type lives with its schema in the app.

### 5.2 API client

`@<scope>/api-client` exports `createApiClient({ baseUrl, getToken })`, which returns `get`, `post`, `put`, `patch` and `delete`. The client:

- adds the bearer token from `getToken`, so callers never pass tokens themselves;
- throws `ApiError` with the HTTP status and a message taken from the backend's error body, when there is one;
- returns no body for 204 responses;
- aborts a request after a timeout and reports it as an `ApiError`.

Each app creates one instance in `lib/api.ts`:

```ts
import { createApiClient } from "@<scope>/api-client";
import { getAccessToken } from "@<scope>/auth";
import { getConfig } from "@<scope>/config";

export const apiClient = createApiClient({
  baseUrl: getConfig().apiBaseUrl,
  getToken: getAccessToken,
});
```

Shared transport helpers, such as file downloads and server-sent event streams, belong in this package too. Do not change the API client for a single feature; add shared behavior, such as a retry policy, in a generic form.

### 5.3 UI package

`@<scope>/ui` holds Tailwind and CVA components grouped by category. shadcn/ui may serve as the underlying primitive, but apps never use raw shadcn/ui components: they are wrapped in the UI package.

```text
packages/ui/src/components/
├── base/          ← buttons, cards, badges, inputs
├── forms/         ← form-level helpers
├── data-display/  ← DataTable, metric cards
├── feedback/      ← spinners, empty states, skeletons
├── navigation/    ← navigation items, breadcrumbs, pagination
├── layout/        ← page containers, page headers, sections
└── domain/        ← domain-aware components reused across apps
```

Rules:

1. Variants are defined with CVA: `<AppButton variant="primary" size="lg">`, not boolean props such as `<AppButton isPrimary isLarge>`.
2. Every component exports a named props type.
3. Components are stateless when possible; the caller owns the state.
4. Use `forwardRef` only where the React version in use requires it to pass a ref.
5. Generic components carry the `App` prefix (`AppButton`, `AppTable`); domain-aware components carry a domain name (`ItemStatusBadge`). Avoid names such as `CustomBox` or `BlueButton`.
6. Components keep keyboard navigation, visible focus, labels or ARIA attributes, and WCAG AA contrast.
7. A component moves to the UI package when a second app or feature reuses it; until then it stays local.
8. Framework-specific links are injected (for example a `linkComponent` prop), so the package does not depend on one router setup.
9. A visual component catalog, such as Storybook, is added only when the application decides so and records it.

The application records its component inventory and its app-local domain components in its own repository.

### 5.4 Auth

`@<scope>/auth` wraps the OpenID Connect client that the application chose. It exposes a provider, a `useAuth` hook, a typed client factory and an access-token getter for the API client. The context and the hook are safe to import in SSR code; the browser-only adapter is exported separately. Apps do not call the OpenID Connect library directly. The application records its identity provider, realms or tenants, and client IDs.

### 5.5 Config

`@<scope>/config` exports `getConfig()`, which returns typed configuration read from `import.meta.env`. Apps do not read `import.meta.env` directly. Every value read this way is embedded in the client bundle at build time and is public (§8).

## 6. Design system

### 6.1 Principles

- Design tokens are the single source of colors, type, spacing, radii and breakpoints; components do not use one-off values.
- Neutral surfaces dominate and the accent color is used sparingly.
- The primary color is consistent across navigation and primary actions.
- Status indicators are clear and do not rely on color alone.
- Text and interactive elements meet at least WCAG AA contrast.
- Every interaction works with the keyboard and exposes correct ARIA semantics.

### 6.2 Semantic tokens

Tokens are named by role, not by color:

| Group | Tokens |
| --- | --- |
| Brand | `primary`, `primary-light`, `primary-dark`, `secondary`, `secondary-light`, `accent`, `accent-light`, `accent-dark` |
| Neutrals | `background`, `surface`, `border`, `text-primary`, `text-secondary`, `text-muted` |
| Status | `success`, `warning`, `destructive`, `info` |

A dark theme, when the application has one, is another set of values for the same tokens.

### 6.3 Scales and layouts

The application records, as tokens, its font family and type scale, a spacing scale on a 4 px grid, radii, breakpoints and container width, and the layout shells it uses (for example a sidebar layout for operators and a top navigation layout for the public). It also records how tables adapt on small screens: as cards or with horizontal scrolling. The values are brand decisions and stay in the application.

### 6.4 Tailwind `@theme`

```css
/* packages/ui/src/styles/theme.css */
@import "tailwindcss";

@theme {
  --color-primary: <brand value>;
  --color-surface: <brand value>;
  --color-destructive: <brand value>;
  --spacing-md: <scale value>;
  --radius-md: <scale value>;
  --font-sans: <font stack>;
}
```

- Tokens are declared in `@theme`; there is no `tailwind.config.*` file.
- Shared tokens live in the UI package's styles. An app overrides only values that are specific to it.

### 6.5 Utility classes

- Order classes by category: layout, spacing, color, typography, state.
- Use Biome's class sorting where it applies; order by hand where it does not.
- Avoid `@apply`; extract a component instead.

## 7. Backend communication

### 7.1 Types

- Every API call is typed with a type from `@<scope>/types`.
- A backend DTO change updates the types package as stated in §5.1.
- Generating the types from the backend's OpenAPI description is preferred when the application sets it up; the [backend standard](java-quarkus-backend.md#102-openapi) coordinates breaking DTO changes in that case.

### 7.2 Errors

`ApiError` carries the HTTP status and a message.

- 401: the session is missing or expired; the app sends the user to sign in.
- 403: the request is not allowed; the app shows a forbidden state. A redirect to sign in does not grant access and can loop when the user already has a session. An application that reauthenticates on 403 records the reason.
- A generic notification for failed requests may be set once, for example in the query client's `onError`. A component handles an error itself only when it needs a contextual action:

```ts
export function useDeleteItem(onConflict: () => void) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) =>
      apiClient.delete<void>(`/api/admin/items/${encodeURIComponent(id)}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: [ITEMS_KEY] }),
    onError: (error) => {
      if (error instanceof ApiError && error.status === 409) {
        onConflict();
      }
    },
  });
}
```

This hook belongs in `features/items/api.ts` next to the others and also imports `ApiError` from `@<scope>/api-client`.

## 8. Security

1. Everything that reaches the client bundle is public. By default Vite exposes in `import.meta.env` only the variables with its client prefix (`VITE_`) and its built-in values, but other build configuration, such as `define` or a changed prefix, can inject more. No secret goes into an exposed variable or into such configuration; secrets stay on servers.
2. User values go into a query string only through `URLSearchParams`. A user value goes into a path segment only after it is validated against its expected format (for example, a positive integer ID or an allowlisted pattern), which rejects `.` and `..`, and then encoded with `encodeURIComponent`. Encoding alone is not enough: it leaves `.` and `..` unchanged, and URL resolution can turn them into a different path.
3. React escapes text by default. `dangerouslySetInnerHTML` is used only with trusted content or with HTML cleaned by an allowlist-based sanitizer.
4. Structured data (JSON-LD) written into a `<script>` element escapes every `<` in the serialized JSON as the six-character sequence `\u003c`, so the data cannot close the element. The result still parses to the same value:

```tsx
export function serializeJsonLd(data: Record<string, unknown>): string {
  return JSON.stringify(data).replace(/</g, "\\u003c");
}

export function JsonLd({ data }: { data: Record<string, unknown> }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: serializeJsonLd(data) }}
    />
  );
}
```

5. Tokens are obtained through the auth package (§5.4); app code does not store them in `localStorage` or `sessionStorage`.
6. An authenticated SSR app follows §4.3.

## 9. Tests

### 9.1 Required minimum

| Code | What the tests check |
| --- | --- |
| Zod schemas | Valid and invalid cases, beside the schema (`item.schema.test.ts`) |
| Pure utilities in `lib/` | Their results for typical and edge inputs |
| SSR helpers (`lib/seo.ts`, `lib/api.server.ts`) | Meta and structured-data output; fallbacks and error handling with a mocked `fetch` |
| SSR loaders and actions | URLs built from filters and query parameters, lookup maps, and §4.3 cases for protected ones |
| Real-time handlers and client stores, when the app has them | Their pure logic extracted and unit-tested; their subscriptions, reconnection and store updates tested with mocks or an integration test |
| Security helpers | For example, that `serializeJsonLd` output contains no `<` and parses back to the input |

Vitest runs in the `node` environment, with v8 coverage. Test files are named `<module>.test.ts` and sit beside the code they test. Component and hook tests are optional; an application that wants them adds a DOM environment for those files and records it.

### 9.2 Mocking `fetch`

```ts
import { afterEach, beforeEach, vi } from "vitest";

beforeEach(() => {
  vi.stubGlobal("fetch", vi.fn());
});

afterEach(() => {
  vi.unstubAllGlobals();
});
```

A JSON-LD check:

```ts
import { expect, test } from "vitest";
import { serializeJsonLd } from "./json-ld";

test("structured data cannot close its script element", () => {
  const data = { name: "</script><script>alert(1)</script>" };
  const json = serializeJsonLd(data);
  expect(json).not.toContain("<");
  expect(JSON.parse(json)).toEqual(data);
});
```

### 9.3 Commands

```bash
pnpm test                                       # all packages through Turborepo
pnpm --filter @<scope>/<app> test               # one app
pnpm --filter @<scope>/<app> test:coverage      # one app with coverage
pnpm --filter @<scope>/<app> exec vitest run <file>
```

## 10. Lint, format and build

### 10.1 Biome

The root `biome.json` is the source of truth: two-space indentation, double quotes, semicolons always, import organizing enabled and the recommended rules, including the accessibility rules.

```bash
pnpm lint                                                # whole monorepo
pnpm lint:fix                                            # apply safe fixes
pnpm --filter <package> exec biome format --write <file> # format one file
```

Format only the files the change touches. Do not run `biome format --write` over a whole directory as part of unrelated work.

### 10.2 Build and dev server

```bash
pnpm build                          # every package through Turborepo
pnpm --filter @<scope>/<app> build  # one app or package
pnpm dev                            # every app
pnpm --filter @<scope>/<app> dev    # one app
```

Every pull request passes `pnpm build` and `pnpm lint`. The application records its apps' ports.

## 11. Accessibility and languages

### 11.1 Accessibility

- Every input is associated with a visible label, through the UI package's field components.
- Icon-only buttons have an `aria-label`.
- Every interactive element shows a visible focus (Tailwind `focus-visible:`).
- Color tokens meet WCAG AA contrast (§6.1).

### 11.2 Languages

The application states its user interface language. Product text and validation messages use it. Do not add an internationalization framework or translation keys until the application needs more than one interface language.

## 12. Anti-patterns

| Do not use | Use |
| --- | --- |
| `tailwind.config.js` or `tailwind.config.ts` | `@theme` in CSS |
| ESLint or Prettier | Biome |
| Single quotes | Double quotes |
| Class components | Function components |
| A component that calls the API client | A hook in `features/<feature>/api.ts` |
| Validation in `onSubmit` | A Zod schema and `zodResolver` |
| Server data in `useState` or Zustand | `useQuery` |
| Backend types declared in an app | `@<scope>/types` |
| A bearer token passed on each call | `createApiClient` with `getToken` |
| A shadcn/ui component copied into an app | A wrapper in the UI package |
| A raw `<input>` without a label | A UI package field component |
| `fetch` in a loader | `apiFetch` from `lib/api.server.ts` |
| `import.meta.env` read in an app | `getConfig()` from `@<scope>/config` |
| A secret in client configuration | A server-side value |
| A user value concatenated into a URL | `URLSearchParams` for queries; validated and encoded path segments (§8) |
| `JSON.stringify` output written into a `<script>` as is | `serializeJsonLd` (§8) |
| A login redirect on 403 | A forbidden state |
| `biome format --write` over a whole directory | Formatting the changed files only |
| Boolean props that multiply variants | CVA variants |

## 13. Pull request checklist

Every frontend pull request follows the sections that apply. A deviation is an exception and records the owner, reason, scope, expiry or review date and tracking issue required by the [standards index](README.md), whether it is written in the pull request or in the application's local rules.

- [ ] New features follow the `features/<feature>/api.ts` and `pages/<feature>/` layout (§3.1, §3.2).
- [ ] Hooks are named `use<Verb><Resource>`, and mutations invalidate their query keys (§3.2).
- [ ] Types come from `@<scope>/types` (§5.1).
- [ ] Each Zod schema is in `src/schemas/` with a test beside it, and forms use `zodResolver` (§3.3, §3.4).
- [ ] UI components come from the UI package (§5.3).
- [ ] URLs carry user values only as stated in §8, and no secret reaches the client bundle (§8).
- [ ] Protected SSR loaders and actions enforce access on the server (§4.3).
- [ ] Tests cover the required minimum for the changed code (§9.1).
- [ ] `pnpm build`, `pnpm lint` and `pnpm test` pass.
