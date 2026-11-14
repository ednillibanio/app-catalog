[English](react-vite-frontend.md) | Português

# Frontend React/Vite

Este padrão vale para frontends web feitos com React, Vite e TypeScript num monorepo pnpm e Turborepo. Ele define as regras de estrutura, acesso a dados, formulários, estado, pacotes compartilhados, tokens de design, segurança, testes e ferramentas que os repositórios de aplicação dessa stack compartilham. Cada aplicação registra no próprio repositório os apps, as portas, o escopo dos pacotes, os valores de design, as versões exatas e as regras mais estritas, como descrito em [Como usar estes padrões](README.pt-BR.md#como-usar-estes-padrões).

Os exemplos usam o módulo neutro `inventory` e a entidade `Item` do padrão de [backend Java/Quarkus](java-quarkus-backend.pt-BR.md), o escopo genérico de pacotes `@<scope>/` e identificadores em inglês. Cada aplicação escolhe o idioma dos seus identificadores e mantém um único vocabulário para hooks, schemas, tipos e componentes. Os exemplos ilustram as regras; passam por checagem de tipos quando este padrão muda, mas não são construídos nem executados como parte deste catálogo.

## 1. Stack

### 1.1 Componentes

| Camada | Tecnologia |
| --- | --- |
| Linguagem | TypeScript em modo strict |
| Biblioteca de UI | React |
| Build e servidor de desenvolvimento | Vite |
| Rotas | React Router: modo biblioteca para apps de página única, modo framework para apps renderizados no servidor (SSR) |
| Pacotes | Workspaces do pnpm e Turborepo |
| Lint e formatação | Biome, a única ferramenta de lint e formatação |
| Estilos | Tailwind CSS com configuração em CSS (`@theme`) |
| Componentes de UI | Um pacote de UI compartilhado, feito com Tailwind e CVA (`class-variance-authority`) |
| Estado do servidor | TanStack Query |
| Estado do cliente | Zustand, só quando justificado (§3.7) |
| Formulários | React Hook Form com Zod |
| Tabelas | TanStack Table |
| Testes | Vitest; Playwright quando a aplicação adota testes de ponta a ponta |

Este padrão não fixa versões. Cada aplicação fixa versões exatas nos próprios arquivos: o Node.js (por exemplo, em `.nvmrc`), o pnpm pelo campo `packageManager` e cada dependência no `package.json` e no lockfile. Algumas regras dependem de uma versão maior: a configuração em CSS exige o Tailwind CSS v4 ou posterior, e as regras de SSR usam o modo framework do React Router v7. Uma aplicação em outra versão maior registra um desvio (§13).

### 1.2 Proibido

- ESLint ou Prettier: o Biome cobre os dois.
- Um arquivo `tailwind.config.js` ou `tailwind.config.ts`: os tokens de design ficam no `@theme` do CSS (§6.4).
- Redux, MobX ou Recoil: o Zustand é a única biblioteca de estado do cliente.
- Componentes do shadcn/ui copiados para um app: eles são encapsulados no pacote de UI compartilhado (§5.3).
- Bibliotecas de formulário que não sejam o React Hook Form, como o Formik.
- Bibliotecas de validação que não sejam o Zod.
- Aspas simples e indentação diferente de dois espaços: o Biome impõe aspas duplas e dois espaços.

## 2. Estrutura do monorepo

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

Todo pacote se chama `@<scope>/<nome>`. Os apps importam os pacotes pelo workspace e resolvem os fontes deles por aliases do Vite e `paths` do TypeScript. O `biome.json` e o `turbo.json` da raiz valem para o monorepo inteiro.

## 3. Apps de página única

### 3.1 Estrutura do código

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

### 3.2 Features e hooks de dados

Cada recurso do backend que o app gerencia tem um par `features/<feature>/` e `pages/<feature>/`. O `features/<feature>/api.ts` contém hooks do TanStack Query e os pequenos auxiliares que eles compartilham, como montadores de caminho, e nada mais:

```ts
import { apiClient } from "@/lib/api";
import type { ItemCreateRequest, ItemDto, PagedResponse } from "@<scope>/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

const ITEMS_KEY = "items";

export function itemPath(id: number): string {
  if (!Number.isSafeInteger(id) || id <= 0) {
    throw new Error(`Invalid item id: ${id}`);
  }
  return `/api/admin/items/${encodeURIComponent(id)}`;
}

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
    queryFn: () => apiClient.get<ItemDto>(itemPath(id)),
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

Regras:

1. Os hooks se chamam `use<Verbo><Recurso>`: `useItems`, `useItem`, `useCreateItem`, `useUpdateItem`, `useDeactivateItem`.
2. Hooks de lista paginada recebem `page` e `size` com valores padrão.
3. As chaves de query são constantes no topo do arquivo.
4. As variantes de uma chave de query são tuplas que começam pela constante e por um tipo: `[ITEMS_KEY, "list", page, size]`, `[ITEMS_KEY, "detail", id]`. Assim, invalidar `[ITEMS_KEY]` cobre todas as variantes.
5. Toda mutação invalida, no `onSuccess`, as chaves de query que afeta; não dependa de um `refetch` manual.
6. Os tipos do backend vêm de `@<scope>/types` (§5.1); não os declare no app.
7. O hook escreve a URL diretamente, o que o deixa autocontido; não existe uma camada separada de "endpoints". Query strings são montadas com `URLSearchParams`, e valores de caminho são validados e codificados como diz a §8, como faz o `itemPath`.
8. Componentes nunca chamam o cliente de API diretamente; eles usam um hook.

### 3.3 Formulários

Um formulário fica em `features/<feature>/<Feature>Form.tsx`:

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

Regras:

1. O schema Zod fica em `src/schemas/<entidade>.schema.ts` (§3.4).
2. O tipo dos dados do formulário é o `z.infer` do schema, exportado junto dele.
3. Todo formulário usa `zodResolver`.
4. A validação fica no schema; o `onSubmit` não acrescenta verificações avulsas.
5. Os campos usam os componentes de entrada do pacote de UI compartilhado, que associam ao controle um rótulo visível e a mensagem de erro (§11.1). Quando faltar um componente, adicione-o ao pacote de UI em vez de escrever um `<input>` cru.

### 3.4 Schemas Zod

```ts
// src/schemas/item.schema.ts
import { z } from "zod";

export const itemSchema = z.object({
  code: z.string().trim().min(1, "Code is required").max(50),
  name: z.string().trim().min(1, "Name is required").max(200),
});

export type ItemFormData = z.infer<typeof itemSchema>;
```

Regras:

1. Cada schema tem ao lado um `<entidade>.schema.test.ts`, com casos válidos e inválidos.
2. As mensagens são escritas no idioma da interface do app, porque os usuários as leem.
3. Campos opcionais e anuláveis correspondem exatamente à requisição do backend (`.optional()`, `.nullable()`); o schema não inventa regras que o backend não tem, e seus limites batem com a validação do backend.
4. Um campo numérico que chega como texto de um `<input type="number">` é convertido com `z.coerce.number()` ou registrado com `valueAsNumber: true`. Quando os tipos de entrada e de saída do schema diferem, como com `z.coerce`, o formulário passa os dois ao `useForm`: `useForm<z.input<typeof itemSchema>, unknown, z.output<typeof itemSchema>>`.

### 3.5 Tabelas

- Use o componente compartilhado `DataTable` (TanStack Table) do pacote de UI; estenda-o lá quando uma tabela precisar de um comportamento novo.
- Defina as colunas `ColumnDef<T>[]` no componente da página.
- Pagine no servidor, pelo `page` e `size` do hook de lista. Não carregue todas as linhas para paginar no navegador.

### 3.6 Rotas

- Declare as rotas num único lugar (`App.tsx`) com `createBrowserRouter` ou `<Routes>`.
- Envolva as rotas protegidas no componente de guarda de autenticação do app. A guarda manda para o login o usuário sem sessão; ela é uma conveniência de experiência, e o backend controla o acesso em cada requisição.
- Carregue páginas grandes sob demanda com `import()`.

### 3.7 Estado

| Estado | Onde fica |
| --- | --- |
| Dados do servidor (cache) | TanStack Query |
| Campos de formulário | React Hook Form |
| Estado local de UI, como um diálogo aberto | `useState` |
| Estado compartilhado entre páginas | Zustand, só quando justificado |
| Filtros, ordenação e paginação que um link deve preservar | Parâmetros de busca da URL (`useSearchParams`) |

Não copie dados do servidor para o Zustand ou para o `useState`: o TanStack Query é a fonte da verdade do estado do servidor.

## 4. Apps renderizados no servidor

### 4.1 Estrutura do código

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

### 4.2 Loaders num app público

Um app SSR público renderiza conteúdo anônimo:

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

Regras:

1. Os loaders chamam a API pelo `apiFetch` de `lib/api.server.ts`, nunca por `fetch` diretamente.
2. Os loaders de um app público chamam só o namespace público do backend e não enviam credenciais.
3. O loader lê e valida os parâmetros de busca e monta a requisição com `URLSearchParams`.
4. Os mapas de consulta de que uma página precisa (por exemplo, nomes por ID) são montados no loader, não no componente.
5. O export `meta` monta suas tags com os auxiliares de `lib/seo.ts`.
6. Listas filtradas guardam os filtros nos parâmetros de busca da URL, para que a navegação para trás e para a frente e os links compartilhados funcionem.

### 4.3 Apps SSR autenticados

Um app SSR que renderiza conteúdo para usuários com sessão escolhe o próprio mecanismo de autenticação e o registra. Ele também cumpre estas regras mínimas:

1. Todo loader e toda action protegidos autenticam e autorizam a requisição no servidor. Uma guarda no cliente não é controle de acesso.
2. Credenciais e dados do usuário ficam restritos à requisição. Eles nunca ficam em variáveis de módulo nem num cache compartilhado entre usuários.
3. Respostas personalizadas são enviadas com `Cache-Control: private, no-store` ou uma política mais restrita.
4. Mutações autenticadas por cookie são protegidas contra cross-site request forgery (CSRF).
5. Os testes cobrem uma requisição sem autenticação e uma requisição sem autorização para cada loader e action protegidos.

### 4.4 Vite e Vitest

O plugin de framework do React Router não roda no Vitest, então o `vite.config.ts` o deixa de fora no modo de teste:

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

## 5. Pacotes compartilhados

### 5.1 Tipos

O `@<scope>/types` espelha um a um os DTOs do backend.

- Altere-o no mesmo pull request do DTO do backend que ele espelha, sempre que os dois estiverem no mesmo repositório; caso contrário, na próxima mudança do frontend, com um link para a mudança do backend.
- Mantenha os nomes do backend (`ItemDto`, `ItemCreateRequest`, `PagedResponse`).
- Não coloque aqui tipos só do frontend: o tipo dos dados de um formulário fica com seu schema, no app.

### 5.2 Cliente de API

O `@<scope>/api-client` exporta `createApiClient({ baseUrl, getToken })`, que devolve `get`, `post`, `put`, `patch` e `delete`. O cliente:

- acrescenta o token bearer obtido por `getToken`, para que quem chama nunca passe tokens;
- lança `ApiError` com o status HTTP e uma mensagem tirada do corpo de erro do backend, quando houver um;
- não devolve corpo em respostas 204;
- interrompe a requisição depois de um tempo limite e a informa como `ApiError`.

Cada app cria uma instância em `lib/api.ts`:

```ts
import { createApiClient } from "@<scope>/api-client";
import { getAccessToken } from "@<scope>/auth";
import { getConfig } from "@<scope>/config";

export const apiClient = createApiClient({
  baseUrl: getConfig().apiBaseUrl,
  getToken: getAccessToken,
});
```

Auxiliares de transporte compartilhados, como downloads de arquivo e fluxos de server-sent events, também ficam neste pacote. Não altere o cliente de API para uma única feature; acrescente comportamento compartilhado, como uma política de nova tentativa, de forma genérica.

### 5.3 Pacote de UI

O `@<scope>/ui` reúne componentes Tailwind e CVA agrupados por categoria. O shadcn/ui pode servir de primitiva por baixo, mas os apps nunca usam componentes crus do shadcn/ui: eles são encapsulados no pacote de UI.

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

Regras:

1. As variantes são definidas com CVA: `<AppButton variant="primary" size="lg">`, e não props booleanas como `<AppButton isPrimary isLarge>`.
2. Todo componente exporta um tipo nomeado de props.
3. Os componentes não têm estado sempre que possível; quem chama é dono do estado.
4. Use `forwardRef` só onde a versão do React em uso o exige para repassar uma ref.
5. Componentes genéricos levam o prefixo `App` (`AppButton`, `AppTable`); componentes ligados ao domínio levam um nome de domínio (`ItemStatusBadge`). Evite nomes como `CustomBox` ou `BlueButton`.
6. Os componentes preservam a navegação por teclado, o foco visível, rótulos ou atributos ARIA e o contraste WCAG AA.
7. Um componente vai para o pacote de UI quando um segundo app ou feature o reutiliza; até lá, fica local.
8. Links específicos de framework são injetados (por exemplo, uma prop `linkComponent`), para que o pacote não dependa de uma configuração de rotas.
9. Um catálogo visual de componentes, como o Storybook, só é adicionado quando a aplicação decide isso e o registra.

A aplicação registra no próprio repositório o inventário de componentes e os componentes de domínio locais de cada app.

### 5.4 Autenticação

O `@<scope>/auth` encapsula o cliente OpenID Connect que a aplicação escolheu. Ele expõe um provider, um hook `useAuth`, uma fábrica tipada do cliente e uma função que entrega o token de acesso ao cliente de API. O contexto e o hook podem ser importados com segurança em código SSR; o adaptador que só roda no navegador é exportado à parte. Os apps não chamam a biblioteca OpenID Connect diretamente. A aplicação registra o provedor de identidade, os realms ou tenants e os client IDs.

### 5.5 Configuração

O `@<scope>/config` exporta `getConfig()`, que devolve a configuração tipada lida de `import.meta.env`. Os apps não leem `import.meta.env` diretamente. Todo valor lido assim é embutido no bundle do cliente no build e é público (§8).

## 6. Design system

### 6.1 Princípios

- Os tokens de design são a única fonte de cores, tipografia, espaçamentos, raios e breakpoints; os componentes não usam valores avulsos.
- Superfícies neutras predominam, e a cor de destaque é usada com moderação.
- A cor primária é consistente na navegação e nas ações principais.
- Os indicadores de status são claros e não dependem só da cor.
- Textos e elementos interativos atendem pelo menos ao contraste WCAG AA.
- Toda interação funciona pelo teclado e expõe a semântica ARIA correta.

### 6.2 Tokens semânticos

Os tokens têm nome de papel, não de cor:

| Grupo | Tokens |
| --- | --- |
| Marca | `primary`, `primary-light`, `primary-dark`, `secondary`, `secondary-light`, `accent`, `accent-light`, `accent-dark` |
| Neutros | `background`, `surface`, `border`, `text-primary`, `text-secondary`, `text-muted` |
| Status | `success`, `warning`, `destructive`, `info` |

Um tema escuro, quando a aplicação tem um, é outro conjunto de valores para os mesmos tokens.

### 6.3 Escalas e layouts

A aplicação registra como tokens a família de fonte e a escala tipográfica, uma escala de espaçamento numa grade de 4 px, os raios, os breakpoints e a largura do contêiner, além dos layouts que usa (por exemplo, um layout com barra lateral para operadores e um layout com navegação no topo para o público). Ela também registra como as tabelas se adaptam a telas pequenas: como cartões ou com rolagem horizontal. Os valores são decisões de marca e ficam na aplicação.

### 6.4 `@theme` do Tailwind

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

- Os tokens são declarados no `@theme`; não existe arquivo `tailwind.config.*`.
- Os tokens compartilhados ficam nos estilos do pacote de UI. Um app sobrescreve só os valores específicos dele.

### 6.5 Classes utilitárias

- Ordene as classes por categoria: layout, espaçamento, cor, tipografia, estado.
- Use a ordenação de classes do Biome onde ela se aplica; ordene à mão onde não se aplica.
- Evite `@apply`; extraia um componente.

## 7. Comunicação com o backend

### 7.1 Tipos

- Toda chamada de API é tipada com um tipo de `@<scope>/types`.
- Uma mudança de DTO no backend atualiza o pacote de tipos como diz a §5.1.
- Gerar os tipos a partir da descrição OpenAPI do backend é preferível quando a aplicação o configura; nesse caso, o [padrão de backend](java-quarkus-backend.pt-BR.md#102-openapi) coordena as mudanças incompatíveis de DTO.

### 7.2 Erros

O `ApiError` carrega o status HTTP e uma mensagem.

- 401: a sessão não existe ou expirou; o app manda o usuário para o login.
- 403: a requisição não é permitida; o app mostra um estado de acesso negado. Um redirecionamento para o login não concede acesso e pode entrar em loop quando o usuário já tem sessão. Uma aplicação que reautentica no 403 registra o motivo.
- Uma notificação genérica para requisições com falha pode ser configurada uma vez, por exemplo no `onError` do query client. Um componente trata o erro por conta própria só quando precisa de uma ação contextual:

```ts
export function useDeleteItem(onConflict: () => void) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiClient.delete<void>(itemPath(id)),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: [ITEMS_KEY] }),
    onError: (error) => {
      if (error instanceof ApiError && error.status === 409) {
        onConflict();
      }
    },
  });
}
```

Este hook fica em `features/items/api.ts`, junto dos outros, usa o `itemPath` da §3.2 e também importa `ApiError` de `@<scope>/api-client`.

## 8. Segurança

1. Tudo o que chega ao bundle do cliente é público. Por padrão, o Vite expõe em `import.meta.env` só as variáveis com o prefixo de cliente (`VITE_`) e os valores embutidos dele, mas outras configurações de build, como `define` ou um prefixo alterado, podem injetar mais. Nenhum segredo vai para uma variável exposta nem para essas configurações; segredos ficam nos servidores.
2. Um valor do usuário entra numa query string só por `URLSearchParams`. Um valor do usuário entra num segmento de caminho só depois de validado contra o formato esperado (por exemplo, um ID inteiro positivo ou um padrão de uma lista de permissões), o que rejeita `.` e `..`, e então codificado com `encodeURIComponent`. Só codificar não basta: a codificação mantém `.` e `..`, e a resolução da URL pode transformá-los num caminho diferente.
3. O React escapa texto por padrão. O `dangerouslySetInnerHTML` só é usado com conteúdo confiável ou com HTML limpo por um sanitizador baseado em lista de permissões.
4. Dados estruturados (JSON-LD) escritos num elemento `<script>` escapam cada `<` do JSON serializado como a sequência de seis caracteres `\u003c`, para que os dados não fechem o elemento. O resultado continua sendo lido como o mesmo valor:

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

5. Os tokens são obtidos pelo pacote de autenticação (§5.4); o código do app não os guarda em `localStorage` nem em `sessionStorage`.
6. Um app SSR autenticado segue a §4.3.

## 9. Testes

### 9.1 Mínimo obrigatório

| Código | O que os testes verificam |
| --- | --- |
| Schemas Zod | Casos válidos e inválidos, ao lado do schema (`item.schema.test.ts`) |
| Utilitários puros em `lib/` | Os resultados para entradas típicas e de borda |
| Auxiliares de SSR (`lib/seo.ts`, `lib/api.server.ts`) | A saída de meta e de dados estruturados; o fallback e o tratamento de erro com `fetch` simulado |
| Loaders e actions de SSR | As URLs montadas a partir de filtros e parâmetros de busca, os mapas de consulta e, nos protegidos, os casos da §4.3 |
| Handlers de tempo real e stores do cliente, quando o app os tem | A lógica pura extraída e testada em unidade; as assinaturas, a reconexão e as atualizações da store testadas com mocks ou num teste de integração |
| Auxiliares de segurança | Por exemplo, que a saída de `serializeJsonLd` não contém `<` e é lida de volta como a entrada |

O Vitest roda no ambiente `node`, com cobertura v8. Os arquivos de teste se chamam `<módulo>.test.ts` e ficam ao lado do código que testam. Testes de componente e de hook são opcionais; uma aplicação que os quiser acrescenta um ambiente DOM para esses arquivos e o registra.

### 9.2 Simular o `fetch`

```ts
import { afterEach, beforeEach, vi } from "vitest";

beforeEach(() => {
  vi.stubGlobal("fetch", vi.fn());
});

afterEach(() => {
  vi.unstubAllGlobals();
});
```

Uma verificação do JSON-LD:

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

### 9.3 Comandos

```bash
pnpm test                                       # all packages through Turborepo
pnpm --filter @<scope>/<app> test               # one app
pnpm --filter @<scope>/<app> test:coverage      # one app with coverage
pnpm --filter @<scope>/<app> exec vitest run <file>
```

## 10. Lint, formatação e build

### 10.1 Biome

O `biome.json` da raiz é a fonte da verdade: indentação de dois espaços, aspas duplas, ponto e vírgula sempre, organização de imports ativada e as regras recomendadas, incluindo as de acessibilidade.

```bash
pnpm lint                                                # whole monorepo
pnpm lint:fix                                            # apply safe fixes
pnpm --filter <package> exec biome format --write <file> # format one file
```

Formate só os arquivos que a mudança toca. Não rode `biome format --write` num diretório inteiro como parte de um trabalho não relacionado.

### 10.2 Build e servidor de desenvolvimento

```bash
pnpm build                          # every package through Turborepo
pnpm --filter @<scope>/<app> build  # one app or package
pnpm dev                            # every app
pnpm --filter @<scope>/<app> dev    # one app
```

Todo pull request passa em `pnpm build` e `pnpm lint`. A aplicação registra as portas dos seus apps.

## 11. Acessibilidade e idiomas

### 11.1 Acessibilidade

- Todo campo de entrada é associado a um rótulo visível, pelos componentes de campo do pacote de UI.
- Botões só com ícone têm `aria-label`.
- Todo elemento interativo mostra o foco visível (`focus-visible:` do Tailwind).
- Os tokens de cor atendem ao contraste WCAG AA (§6.1).

### 11.2 Idiomas

A aplicação declara o idioma da sua interface. Os textos do produto e as mensagens de validação usam esse idioma. Não adicione um framework de internacionalização nem chaves de tradução até a aplicação precisar de mais de um idioma de interface.

## 12. Antipadrões

| Não use | Use |
| --- | --- |
| `tailwind.config.js` ou `tailwind.config.ts` | `@theme` no CSS |
| ESLint ou Prettier | Biome |
| Aspas simples | Aspas duplas |
| Componentes de classe | Componentes de função |
| Um componente que chama o cliente de API | Um hook em `features/<feature>/api.ts` |
| Validação no `onSubmit` | Um schema Zod e `zodResolver` |
| Dados do servidor em `useState` ou Zustand | `useQuery` |
| Tipos do backend declarados num app | `@<scope>/types` |
| Um token bearer passado em cada chamada | `createApiClient` com `getToken` |
| Um componente do shadcn/ui copiado para um app | Um wrapper no pacote de UI |
| Um `<input>` cru, sem rótulo | Um componente de campo do pacote de UI |
| `fetch` num loader | `apiFetch` de `lib/api.server.ts` |
| `import.meta.env` lido num app | `getConfig()` de `@<scope>/config` |
| Um segredo na configuração do cliente | Um valor no servidor |
| Um valor do usuário concatenado numa URL | `URLSearchParams` em queries; segmentos de caminho validados e codificados (§8) |
| Saída de `JSON.stringify` escrita como está num `<script>` | `serializeJsonLd` (§8) |
| Redirecionamento para o login no 403 | Um estado de acesso negado |
| `biome format --write` num diretório inteiro | Formatar só os arquivos alterados |
| Props booleanas que multiplicam variantes | Variantes CVA |

## 13. Checklist de pull request

Todo pull request de frontend segue as seções que se aplicam. Um desvio é uma exceção e registra o dono, o motivo, o escopo, a data de expiração ou de revisão e a issue de acompanhamento exigidos pelo [índice dos padrões](README.pt-BR.md), seja no pull request, seja nas regras locais da aplicação.

- [ ] Features novas seguem a estrutura `features/<feature>/api.ts` e `pages/<feature>/` (§3.1, §3.2).
- [ ] Os hooks se chamam `use<Verbo><Recurso>`, e as mutações invalidam suas chaves de query (§3.2).
- [ ] Os tipos vêm de `@<scope>/types` (§5.1).
- [ ] Cada schema Zod está em `src/schemas/` com um teste ao lado, e os formulários usam `zodResolver` (§3.3, §3.4).
- [ ] Os componentes de UI vêm do pacote de UI (§5.3).
- [ ] As URLs levam valores do usuário só como diz a §8, e nenhum segredo chega ao bundle do cliente (§8).
- [ ] Loaders e actions SSR protegidos controlam o acesso no servidor (§4.3).
- [ ] Os testes cobrem o mínimo obrigatório para o código alterado (§9.1).
- [ ] `pnpm build`, `pnpm lint` e `pnpm test` passam.
