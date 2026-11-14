[English](java-quarkus-backend.md) | Português

# Backend Java/Quarkus

Este padrão vale para serviços de backend feitos com Java, Quarkus e Maven. Ele define as regras de camadas, nomes, persistência, REST, segurança, testes e observabilidade que os repositórios de aplicação dessa stack compartilham. Cada aplicação registra no próprio repositório a lista de módulos, os prefixos de tabela, os namespaces, os papéis, as versões exatas e as regras mais estritas, como descrito em [Como usar estes padrões](README.pt-BR.md#como-usar-estes-padrões).

Os exemplos usam um módulo neutro `inventory` com a entidade `Item`, o pacote genérico `<base>` e identificadores em inglês. Eles ilustram as regras; não são compilados como parte deste catálogo.

## 1. Stack

### 1.1 Componentes

| Camada | Tecnologia |
| --- | --- |
| Linguagem | Java, uma versão LTS |
| Build | Maven pelo Maven Wrapper (`mvnw`) |
| Runtime | Quarkus |
| REST | RESTEasy Reactive com Jackson |
| Persistência | Hibernate ORM com Panache |
| Validação | Hibernate Validator (Jakarta Validation) |
| Autenticação | Quarkus OIDC (`quarkus-oidc`) com um provedor OpenID Connect |
| Banco de dados | PostgreSQL |
| Migrações | Flyway (`quarkus-flyway`) |
| Descrição da API | `quarkus-smallrye-openapi` |
| Health checks | `quarkus-smallrye-health` |

Este padrão não fixa versões. Cada aplicação fixa versões exatas nos próprios arquivos: a versão do Java (por exemplo, em `.sdkmanrc`), a versão do Maven nas propriedades do wrapper e a plataforma Quarkus e as extensões no `pom.xml`. Extensões adicionais, como um backend de cache ou um cliente de administração do provedor de identidade, são decisões da aplicação.

### 1.2 Anotações canônicas

Use exatamente estes pacotes em código novo e troque outros imports ao refatorar.

| Finalidade | Anotação | Pacote |
| --- | --- | --- |
| Entidade JPA | `@Entity`, `@Table`, `@Column`, `@Id`, `@ManyToOne`, … | `jakarta.persistence.*` |
| Bean Validation | `@NotNull`, `@NotBlank`, `@Size`, `@Valid` | `jakarta.validation.*` |
| Escopo CDI | `@ApplicationScoped`, `@Singleton`, `@RequestScoped` | `jakarta.enterprise.context.*`, `jakarta.inject.*` |
| Injeção | `@Inject` | `jakarta.inject.Inject` |
| Transações | `@Transactional` | `jakarta.transaction.Transactional` |
| JAX-RS | `@Path`, `@GET`, `@POST`, `@PathParam`, `@QueryParam`, `Response` | `jakarta.ws.rs.*`, `jakarta.ws.rs.core.*` |
| Segurança REST | `@RolesAllowed`, `@PermitAll`, `@DenyAll` | `jakarta.annotation.security.*` |
| OpenAPI | `@Tag`, `@Operation`, `@Parameter`, `@APIResponse` | `org.eclipse.microprofile.openapi.annotations.*` |
| Mapeador de exceções | `@ServerExceptionMapper` | `org.jboss.resteasy.reactive.server.ServerExceptionMapper` |
| Repositório Panache | `PanacheRepository<T>` | `io.quarkus.hibernate.orm.panache.PanacheRepository` |
| Ordenação Panache | `Sort` | `io.quarkus.panache.common.Sort` |
| Cache declarativo, quando a aplicação usa Quarkus Cache | `@CacheResult`, `@CacheInvalidate` | `io.quarkus.cache.*` |

Proibido:

- pacotes `javax.*` do Java EE substituídos pelo Jakarta EE (como `javax.persistence`, `javax.ws.rs`, `javax.inject`, `javax.validation`, `javax.transaction`); use os equivalentes `jakarta.*`. Pacotes do Java SE como `javax.sql` e `javax.crypto` continuam permitidos;
- anotações do Spring (`@Service`, `@Repository`, `@Autowired`);
- anotações `@Path` de mais de um pacote.

## 2. Estrutura de módulos

### 2.1 Quatro camadas

Todo módulo tem as mesmas quatro camadas. Não crie outras.

```text
<base>.<module>/
├── domain/            ← JPA entities, enums, value objects, repository interfaces, domain exceptions
├── application/       ← services (@ApplicationScoped), mappers, orchestration
│   └── dto/           ← request and response DTOs (records)
├── infrastructure/    ← Panache repository implementations, external integrations
└── interfaces/        ← JAX-RS resources
```

### 2.2 Dependências num só sentido

```text
interfaces  →  application  →  domain
                                  ↑
                          infrastructure
```

- `domain/` não importa de nenhuma outra camada do seu módulo.
- `application/` não importa de `interfaces/` nem de `infrastructure/`.
- `infrastructure/` importa de `domain/` para implementar os contratos dela.
- `interfaces/` chama `application/`. Nunca cria nem altera entidades de `domain/` diretamente; chama um service.

### 2.3 Referências entre módulos por ID

Um módulo se refere a entidades de outro módulo só por um ID `Long`. Nunca use `@ManyToOne` nem importe uma entidade de outro módulo.

```java
// Correct: an entity in another module that refers to an item
@Column(name = "item_id", nullable = false)
private Long itemId;

// Prohibited
@ManyToOne
private Item item;
```

Relacionamentos dentro do mesmo módulo podem usar associações JPA.

### 2.4 Módulos e prefixos de tabela

Cada módulo que tem tabelas usa um prefixo de tabela curto e próprio (por exemplo, `inv_` para `inventory`). Módulos sem tabelas, como um módulo compartilhado ou um módulo que só agrega consultas, não têm prefixo. A aplicação lista seus módulos e prefixos na própria documentação.

## 3. Camada de domínio

### 3.1 Entidades

```java
package <base>.inventory.domain;

import <base>.shared.domain.AuditedEntity;
import jakarta.persistence.*;

@Entity
@Table(name = "inv_item",
       indexes = {
           @Index(name = "idx_inv_item_code", columnList = "code")
       })
public class Item extends AuditedEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 50)
    private String code;

    @Column(nullable = false, length = 200)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private ItemStatus status = ItemStatus.DRAFT;

    private boolean active = true;

    public void publish() {
        if (status != ItemStatus.DRAFT) {
            throw new IllegalStateException("Only a draft item can be published");
        }
        status = ItemStatus.PUBLISHED;
    }

    public Long getId() { return id; }
    public String getCode() { return code; }
    public void setCode(String code) { this.code = code; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public boolean isActive() { return active; }
    // other getters and setters
}
```

Regras:

1. Uma entidade que guarda estado de negócio estende a classe base de auditoria da aplicação (`AuditedEntity` nestes exemplos). A classe base fornece as datas de criação e de atualização, preenchidas em `@PrePersist` e `@PreUpdate`, e os autores da criação e da atualização, preenchidos por um entity listener a partir do serviço de contexto do usuário (§6.6). Não adicione esses campos à mão.
2. Uma entidade que não estende a classe base informa o motivo num comentário na classe. Logs só de inclusão que registram o próprio autor e horário, tabelas de associação puras, dados de referência e filhas de uma entidade auditada são casos típicos; cada aplicação decide quais deles aceita.
3. A chave primária é `Long id` com `GenerationType.IDENTITY`.
4. Não use Lombok. Escreva getters e setters explicitamente; a aplicação pode definir o formato deles.
5. Booleanos são campos primitivos com valor padrão, como `private boolean active = true;`, lidos por `isActive()`.
6. Enums usam `@Enumerated(EnumType.STRING)`.
7. Datas usam `LocalDate` para data sem hora (`DATE`) e `LocalDateTime` para data e hora (`TIMESTAMP`). Nunca use `java.util.Date`.
8. Strings curtas e limitadas usam `@Column(length = N)` com `VARCHAR(N)`; texto longo ou livre usa `@Column(columnDefinition = "TEXT")` com `TEXT`.
9. Transições de estado e invariantes ficam em métodos da entidade, como `publish()` acima, e não nos services.

### 3.2 Interface do repositório

A interface do repositório fica em `domain/` e usa termos do domínio; ela não expõe o Panache.

```java
package <base>.inventory.domain;

import java.util.List;
import java.util.Optional;

public interface ItemRepository {
    Optional<Item> fetchById(Long id);
    List<Item> listPage(int page, int size);
    long countAll();
    Item save(Item item);
    void remove(Item item);
}
```

Use um vocabulário de métodos único e consistente em toda a aplicação, no idioma que ela escolheu para os identificadores do código. Os nomes não podem colidir com métodos do Panache (`findById`, `list`, `count`, `delete`, `persist`, …): a implementação também implementa `PanacheRepository`, e um método com o mesmo nome ou não compila ou substitui o método do Panache. Estes exemplos usam:

| Operação | Método |
| --- | --- |
| Buscar por ID | `fetchById(id)`, que retorna `Optional` |
| Buscar por outro campo | `findBy<Field>(…)`, que retorna `Optional` ou `List` |
| Lista paginada | `listPage(page, size)` |
| Lista paginada com filtro | `findBy<X>(x, page, size)` |
| Contar todos | `countAll()` |
| Contar com filtro | `countBy<X>(x)` |
| Criar ou atualizar | `save(entity)` |
| Excluir | `remove(entity)` |
| Existência | `existsBy<X>(x)` |

### 3.3 Exceções de domínio

Mantenha um conjunto pequeno de exceções compartilhadas no módulo compartilhado e mapeie-as para HTTP num único mapeador global de exceções (métodos `@ServerExceptionMapper` numa só classe).

| Exceção (nome de exemplo) | HTTP | Quando |
| --- | --- | --- |
| `ResourceNotFoundException` | 404 | Não existe entidade com o ID pedido |
| `ResourceConflictException` | 409 | Duplicidade ou conflito com restrição de unicidade |
| `PolicyViolationException` | 400 | Entrada válida que viola uma regra de negócio no contexto atual |
| `AccessDeniedException` | 403 | Usuário autenticado sem acesso ao recurso |
| `IllegalStateException` | 409 | Transição de estado inválida |
| `ConstraintViolationException` (Bean Validation) na entrada da requisição | 400 | Parâmetros ou corpo inválidos de um método de resource |

Uma violação de Bean Validation em outro ponto, como numa chamada de service ou num valor de retorno, é um defeito do servidor e retorna 500. O tratamento padrão do Quarkus faz essa distinção; um mapeador próprio para `ConstraintViolationException` a mantém, por exemplo retornando 400 só para violações nos parâmetros de métodos de resource.

Não crie exceções específicas de um módulo, a menos que o domínio precise do conceito; essa exceção estende uma compartilhada para manter o status HTTP. A aplicação define o corpo de erro (por exemplo, `{ "status": 404, "message": "…" }`) e o usa em toda exceção mapeada.

## 4. Camada de aplicação

### 4.1 Services

```java
package <base>.inventory.application;

import <base>.inventory.application.dto.*;
import <base>.inventory.domain.Item;
import <base>.inventory.domain.ItemRepository;
import <base>.shared.application.AuditTrail;
import <base>.shared.application.PagedResponse;
import <base>.shared.domain.ResourceNotFoundException;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;

@ApplicationScoped
public class ItemService {

    @Inject
    ItemRepository repository;   // the domain interface, not the implementation

    @Inject
    ItemMapper mapper;

    @Inject
    AuditTrail auditTrail;       // records the audit event of every write (§8.6)

    public PagedResponse<ItemDto> list(int page, int size) {
        var content = repository.listPage(page, size).stream().map(mapper::toDto).toList();
        return PagedResponse.of(content, page, size, repository.countAll());
    }

    public ItemDto findById(Long id) {
        return mapper.toDto(find(id));
    }

    @Transactional
    public ItemDto create(ItemCreateRequest request) {
        var item = repository.save(mapper.toEntity(request));
        auditTrail.created(item);
        return mapper.toDto(item);
    }

    @Transactional
    public ItemDto update(Long id, ItemUpdateRequest request) {
        var item = find(id);
        var before = auditTrail.snapshot(item);
        mapper.apply(request, item);
        repository.save(item);
        auditTrail.updated(before, item);
        return mapper.toDto(item);
    }

    @Transactional
    public void delete(Long id) {
        var item = find(id);
        repository.remove(item);
        auditTrail.deleted(item);
    }

    private Item find(Long id) {
        return repository.fetchById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Item", id));
    }
}
```

Regras:

1. Services são `@ApplicationScoped`.
2. Services injetam a interface do repositório de `domain/`, nunca a implementação.
3. Métodos públicos de escrita usam `@Transactional`; métodos de leitura não.
4. Nunca coloque `@Transactional` num método privado; o proxy CDI não o intercepta.
5. Um método auxiliar privado de busca lança a exceção de não encontrado, para que todo método trate uma entidade ausente do mesmo jeito.
6. Services retornam DTOs, nunca entidades.
7. Listas paginadas retornam o envelope de página (§6.5); listas curtas sem paginação retornam `List<T>`.

### 4.2 DTOs

```java
package <base>.inventory.application.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.time.LocalDateTime;

public record ItemDto(Long id, String code, String name, LocalDateTime createdAt) {}

public record ItemCreateRequest(
    @NotBlank @Size(max = 50) String code,
    @NotBlank @Size(max = 200) String name
) {}

public record ItemUpdateRequest(
    @NotBlank @Size(max = 200) String name
) {}
```

Cada record fica no próprio arquivo; aqui aparecem juntos para abreviar.

Regras:

1. DTOs são `record`s, não classes mutáveis.
2. Anotações de Bean Validation ficam só nos DTOs de requisição. Uma requisição de atualização usada por PUT substitui todos os campos editáveis e tem as mesmas restrições da criação. Uma atualização parcial (PATCH), que permite omitir campos, precisa de uma restrição que aceite `null` mas aplique as regras da criação a um valor informado, por exemplo uma restrição personalizada; a aplicação a documenta.
3. Nomes: `<Entity>Dto` para uma resposta, `<Entity>DetailDto` para uma resposta detalhada ou agregada, `<Entity>CreateRequest` e `<Entity>UpdateRequest` para escritas e `<Verb><Entity>Request` para outras operações (por exemplo, `PublishItemRequest`).
4. DTOs ficam em `application/dto/`, nunca declarados dentro de um resource.
5. Um DTO nunca contém uma entidade. Para incluir dados de outra entidade, monte um DTO agregado no service ou no mapper.

### 4.3 Mappers

```java
package <base>.inventory.application;

import <base>.inventory.application.dto.*;
import <base>.inventory.domain.Item;
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class ItemMapper {

    public ItemDto toDto(Item item) {
        return new ItemDto(item.getId(), item.getCode(), item.getName(), item.getCreatedAt());
    }

    public Item toEntity(ItemCreateRequest request) {
        var item = new Item();
        item.setCode(request.code());
        item.setName(request.name());
        return item;
    }

    public void apply(ItemUpdateRequest request, Item item) {
        item.setName(request.name());
    }
}
```

Mappers são beans `@ApplicationScoped` escritos à mão. Não use MapStruct nem outro gerador de mapeamento.

## 5. Camada de infraestrutura

### 5.1 Implementações de repositório

```java
package <base>.inventory.infrastructure;

import <base>.inventory.domain.Item;
import <base>.inventory.domain.ItemRepository;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import io.quarkus.panache.common.Sort;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;
import java.util.Optional;

@ApplicationScoped
public class ItemRepositoryImpl implements ItemRepository, PanacheRepository<Item> {

    private static final Sort DEFAULT_SORT = Sort.by("id", Sort.Direction.Descending);

    @Override
    public Optional<Item> fetchById(Long id) {
        return findByIdOptional(id);
    }

    @Override
    public List<Item> listPage(int page, int size) {
        return findAll(DEFAULT_SORT).page(page, size).list();
    }

    @Override
    public long countAll() {
        return count();
    }

    @Override
    public Item save(Item item) {
        persistAndFlush(item);
        return item;
    }

    @Override
    public void remove(Item item) {
        delete(item);
    }
}
```

### 5.2 Como o Panache é usado

O Panache é o padrão de persistência, usado só dentro das implementações de repositório:

- Entidades são classes JPA simples; não estendem `PanacheEntity`.
- Services nunca injetam `PanacheRepository<T>` nem chamam métodos do Panache.
- Uma implementação de repositório implementa a interface do domínio e `PanacheRepository<Entity>` e usa métodos do Panache como `findByIdOptional`, `find`, `findAll`, `count` e `persistAndFlush`.

Assim os services dependem só de `domain/` e os testes unitários conseguem simulá-los com facilidade, enquanto as implementações de repositório continuam curtas.

### 5.3 Consultas nativas

Para recursos do PostgreSQL como busca textual, JSONB ou funções de janela, declare o método na interface do domínio, injete `EntityManager` na implementação do repositório e use uma consulta nativa com parâmetros vinculados. Passe o texto de busca do usuário a uma função feita para entrada livre, como `websearch_to_tsquery` ou `plainto_tsquery`; montar uma expressão `to_tsquery` a partir do texto do usuário falha com pontuação e operadores.

```java
// ItemRepository declares: List<Item> search(String text, int page, int size);

@Inject
EntityManager em;

@Override
public List<Item> search(String text, int page, int size) {
    return em.createNativeQuery(
            "SELECT * FROM inv_item "
            + "WHERE to_tsvector('english', name) @@ websearch_to_tsquery('english', :q) "
            + "ORDER BY id DESC LIMIT :size OFFSET :offset", Item.class)
            .setParameter("q", text)
            .setParameter("size", size)
            .setParameter("offset", page * size)
            .getResultList();
}
```

## 6. Camada de interfaces (REST)

### 6.1 Namespaces da API

Separe a API em namespaces por prefixo de caminho, por exemplo `/api/public` para acesso anônimo e `/api/admin` para operadores autenticados. Cada namespace tem um requisito de autenticação explícito e uma regra de papéis. A aplicação documenta seus namespaces, os prefixos, o realm ou tenant de identidade que autentica cada um e os papéis que cada um exige.

### 6.2 Nomes de resources

Dê ao resource o nome do namespace e do assunto, com o namespace como prefixo: `Public<X>Resource`, `Admin<X>Resource` e o mesmo padrão para outros namespaces. Ao editar um resource com nome antigo, mantenha o nome; renomear é uma mudança separada.

### 6.3 Estrutura de um resource

```java
package <base>.inventory.interfaces;

import <base>.inventory.application.ItemService;
import <base>.inventory.application.dto.*;
import jakarta.annotation.security.RolesAllowed;
import jakarta.inject.Inject;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.eclipse.microprofile.openapi.annotations.Operation;
import org.eclipse.microprofile.openapi.annotations.tags.Tag;
import java.net.URI;

@Path("/api/admin/items")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
@Tag(name = "Admin - Items")
@RolesAllowed("admin")
public class AdminItemResource {

    @Inject
    ItemService service;

    @GET
    @Operation(summary = "List items")
    public Response list(
            @QueryParam("page") @DefaultValue("0") @Min(0) @Max(10000) int page,
            @QueryParam("size") @DefaultValue("20") @Min(1) @Max(100) int size) {
        return Response.ok(service.list(page, size)).build();
    }

    @GET
    @Path("/{id}")
    @Operation(summary = "Get an item")
    public Response findById(@PathParam("id") Long id) {
        return Response.ok(service.findById(id)).build();
    }

    @POST
    @Operation(summary = "Create an item")
    public Response create(@NotNull @Valid ItemCreateRequest request) {
        var dto = service.create(request);
        return Response.created(URI.create("/api/admin/items/" + dto.id())).entity(dto).build();
    }

    @PUT
    @Path("/{id}")
    @Operation(summary = "Update an item")
    public Response update(@PathParam("id") Long id, @NotNull @Valid ItemUpdateRequest request) {
        return Response.ok(service.update(id, request)).build();
    }

    @DELETE
    @Path("/{id}")
    @Operation(summary = "Delete an item")
    public Response delete(@PathParam("id") Long id) {
        service.delete(id);
        return Response.noContent().build();
    }
}
```

### 6.4 Regras de resources

1. Os métodos retornam `Response`, não um DTO, uma lista ou uma página diretamente. Isso deixa os códigos de status explícitos e facilita adicionar cabeçalhos como `Location` ou `ETag`. Converta resources antigos na próxima vez que mudá-los.
2. Códigos de status: GET retorna 200; um POST que cria retorna 201 com `Location`; PUT e PATCH retornam 200; DELETE retorna 204.
3. Corpos de requisição (`*CreateRequest`, `*UpdateRequest` e outros DTOs de requisição) levam `@NotNull @Valid`: só `@Valid` não rejeita um corpo ausente ou `null`.
4. Todo resource fora do namespace anônimo tem `@RolesAllowed`. A falta da anotação de papel é um defeito de segurança.
5. Todo resource tem `@Tag` e todo método tem `@Operation(summary = …)`, para que o OpenAPI gerado sirva aos clientes.
6. Nenhum record ou DTO é declarado dentro de um resource; eles ficam em `application/dto/`.
7. Resources não têm lógica de negócio: leem parâmetros, chamam um service e montam a `Response`.
8. Resources não usam `@Transactional`; transações são dos services.
9. Resources nunca acessam repositórios.
10. A paginação usa `@QueryParam("page") @DefaultValue("0")` e `@QueryParam("size") @DefaultValue("20")`. Uma lista curta que costuma aparecer inteira, como tipos ou enumerações, pode usar 50 como padrão. Valide os dois parâmetros: `page` fica entre 0 e um máximo e `size` fica entre 1 e um máximo, ambos definidos pela aplicação (10000 e 100 no exemplo), para que um valor inválido retorne 400 em vez de um erro ou de uma consulta sem limite. Escolha os máximos de modo que o offset `page × size` caiba num `int`, que é o que o Panache e o JPA aceitam como primeiro resultado.

### 6.5 Envelope de página

A aplicação tem exatamente um envelope de página genérico (`PagedResponse<T>` nestes exemplos), criado por uma fábrica como `PagedResponse.of(content, page, size, total)`. O formato JSON é fixo e documentado:

```json
{ "content": [], "page": 0, "size": 20, "total": 150, "totalPages": 8 }
```

### 6.6 Contexto do usuário

Resources e services obtêm o usuário autenticado por um único serviço injetável de contexto do usuário da aplicação (`UserContext` nestes exemplos), e não por `SecurityIdentity` ou pelas claims do token diretamente. Esse serviço é o único lugar que lê claims de identidade.

```java
@Inject
UserContext userContext;

String userId = userContext.currentUserId();
```

## 7. Banco de dados e migrações

### 7.1 Convenções de esquema

- Tabelas: `<prefix>_<snake_case>`, como `inv_item`.
- Colunas: `snake_case`, como `available_from`.
- Chave primária: `id BIGSERIAL PRIMARY KEY`.
- Coluna de chave estrangeira: `<entity>_id BIGINT NOT NULL`, anulável só quando o relacionamento é opcional.
- Restrições de chave estrangeira só dentro de um módulo; referências entre módulos são colunas de ID simples (§2.3).
- Índices: `idx_<table>_<columns>`; restrições de unicidade: `uk_<table>_<columns>`.
- Colunas de auditoria, nas tabelas de entidades auditadas (§7.3): datas de criação e atualização como `TIMESTAMP NOT NULL` e autores da criação e da atualização como `VARCHAR(255)`, com nomes definidos pela aplicação (por exemplo, `created_at`, `updated_at`, `created_by`, `updated_by`).

### 7.2 Flyway

- As migrações ficam em `src/main/resources/db/migration/` como `V<version>__<description>.sql`.
- As versões são sequenciais e nunca reaproveitadas. Confira a maior versão existente antes de criar uma.
- Nunca edite uma migração depois do merge; crie uma nova. Uma aplicação que precise de uma exceção única a documenta, com o escopo e o procedimento de reparo, no próprio padrão.
- Migrações contêm só DDL e DML estrutural. Dados de demonstração ou exemplo ficam num local de seed separado, que só o perfil de desenvolvimento carrega e o perfil de teste exclui.
- Use recursos do PostgreSQL quando ajudarem: JSONB, busca textual com `tsvector`, índices GIN, colunas geradas.

### 7.3 Colunas de auditoria

Numa tabela cuja entidade estende a classe base de auditoria, declare as quatro colunas de auditoria explicitamente na migração que cria a tabela; não dependa da geração de esquema do Hibernate. A classe base (§3.1) as preenche. Uma tabela cuja entidade é uma exceção aceita (§3.1, regra 2) não tem colunas de auditoria, a menos que o próprio modelo precise delas, como o autor e o horário de um registro de log só de inclusão.

### 7.4 Configuração

Mantenha a configuração num único `application.properties`, com os prefixos de perfil `%dev.`, `%test.` e `%prod.`. Não crie arquivos `application-<profile>.properties`. Segredos e valores específicos da máquina vêm de variáveis de ambiente, nunca de arquivos versionados.

## 8. Segurança

### 8.1 Autenticação

Os clientes enviam um token bearer OIDC no cabeçalho `Authorization`, e o `quarkus-oidc` o valida com o provedor de identidade. Quando grupos diferentes de usuários se autenticam em realms ou tenants diferentes, a aplicação documenta qual namespace cada um atende e como as requisições são encaminhadas para ele.

### 8.2 Papéis

A aplicação documenta seus papéis: o nome, as aplicações cliente que o usam, o que ele permite e como é atribuído. Os resources usam esses papéis; não inventam papéis novos.

### 8.3 Autorização em camadas

1. Resource: um `@RolesAllowed` na classe é a primeira barreira.
2. Operação: um `@RolesAllowed` no método substitui o da classe para aquele método; ele não se soma ao da classe. Use-o quando uma operação exige outro papel e liste todos os papéis que podem chamar o método. Quando quem chama precisa atender às duas condições, confira a segunda explicitamente no service.
3. Service: quando o papel não basta, o service confere a posse ou o tenant (por exemplo, um usuário vê só os próprios registros) e lança a exceção de acesso negado (403).
4. Resources públicos usam DTOs próprios, separados dos DTOs autenticados, e nunca retornam campos sensíveis.

### 8.4 Regras de segurança

1. Todo endpoint autenticado rejeita requisições anônimas com 401.
2. APIs públicas retornam só campos que podem ser publicados (§8.5).
3. Tokens nunca aparecem em logs.
4. Todo DTO de requisição é validado com Bean Validation (`@NotBlank`, `@Size`, `@Email`, …).
5. Valores controlados pelo usuário entram em qualquer consulta (Panache, JPQL e nativa) só como parâmetros vinculados, nunca por concatenação de strings. Identificadores dinâmicos, como um campo ou uma direção de ordenação escolhidos pelo cliente, são mapeados a partir de uma lista de permissões.
6. Texto não confiável é seguro para renderizar: os frontends o codificam ou escapam conforme o contexto de saída (texto HTML, atributo, URL, JavaScript), mesmo a API sendo só JSON. Quando o produto pretende renderizar HTML enviado pelo usuário, o backend ou o frontend o limpa com um sanitizador de HTML baseado em lista de permissões.
7. O CORS é configurado por perfil: origens locais em desenvolvimento e uma lista explícita de origens em produção, definida por configuração.
8. O tráfego de produção usa HTTPS; o TLS pode terminar no proxy reverso.

### 8.5 Campos que APIs públicas nunca retornam

- dados pessoais de contato, como endereços de email, a menos que a lei os torne públicos;
- IDs internos de usuários;
- campos de auditoria (quem criou ou alterou um registro);
- tokens ou dados de sessão;
- detalhes de configuração do sistema.

### 8.6 Trilha de auditoria

Toda escrita numa entidade de domínio registra um evento de auditoria por um único serviço da aplicação (`AuditTrail` no exemplo da §4.1), chamado pelo método do service que faz a escrita, na mesma transação: quem (o ID do usuário do token), o quê (tipo da entidade, ID e campos alterados), quando (data e hora) e o contexto (por exemplo, em JSONB).

### 8.7 Configuração de CORS

Configure o CORS no `application.properties`, com as origens permitidas em produção vindas de uma variável de ambiente.

## 9. Testes

### 9.1 Tipos de teste

| Tipo | Sufixo | Roda com | Cobre |
| --- | --- | --- | --- |
| Unitário | `*Test.java` | JUnit 5 e Mockito, sem contêiner | services, mappers, lógica de domínio |
| Integração | `*IT.java` | `@QuarkusTest` com PostgreSQL, por Testcontainers ou por um banco de teste dedicado | resources, repositórios reais, migrações |

### 9.2 Teste unitário

```java
@ExtendWith(MockitoExtension.class)
class ItemServiceTest {

    @Mock ItemRepository repository;
    @Mock ItemMapper mapper;
    @Mock AuditTrail auditTrail;
    @InjectMocks ItemService service;

    @Test
    void throwsWhenItemIsMissing() {
        when(repository.fetchById(99L)).thenReturn(Optional.empty());
        assertThrows(ResourceNotFoundException.class, () -> service.findById(99L));
    }
}
```

### 9.3 Teste de integração

```java
@QuarkusTest
class AdminItemResourceIT {

    @Test
    @TestSecurity(user = "admin", roles = "admin")
    void listsItems() {
        given()
            .when().get("/api/admin/items")
            .then()
            .statusCode(200)
            .body("content", notNullValue());
    }

    @Test
    void rejectsAnonymousRequest() {
        given()
            .when().get("/api/admin/items")
            .then()
            .statusCode(401);
    }
}
```

### 9.4 Regras de teste

1. Todo resource protegido tem pelo menos um teste de integração que espera 401 sem token.
2. Toda transição de estado de entidade tem um teste unitário.
3. Os testes usam banco próprio, configurado em `%test`, e fixtures próprias. Nunca dependem do seed de desenvolvimento.
4. Claims além de usuário e papéis são definidas com `@JwtSecurity` (`quarkus-test-security-jwt`) junto com `@TestSecurity`.
5. Armadilhas conhecidas:
   - Uma coluna JSONB mapeada para `String` precisa de `@JdbcTypeCode(SqlTypes.JSON)` e `@Column(columnDefinition = "JSONB")`.
   - Duas entidades com o mesmo nome simples em módulos diferentes falham com `DuplicateMappingException` quando o `@QuarkusTest` sobe, não na compilação. Dê nomes distintos a elas.
   - `@TestSecurity` substitui a autenticação por token só nos testes que anota. Quando o perfil de teste não tem um provedor de identidade acessível, os testes que usam `@TestSecurity` podem rodar com `%test.quarkus.oidc.enabled=false`; a validação real de tokens bearer é então testada num perfil separado, com um provedor de teste (por exemplo, Keycloak Dev Services ou um mock de servidor OIDC).
   - Um `@TestSecurity` na classe vale também para os testes de 401, e o `.auth().none()` do REST Assured não o remove. Em classes que testam 401, coloque `@TestSecurity` nos métodos.
   - Cada novo `@Inject` num service com teste unitário precisa do `@Mock` correspondente; sem ele, o `@InjectMocks` deixa o campo `null` sem erro.
   - Alguns testes de integração dependem da ordem ou de dados compartilhados. Antes de chamar uma falha de regressão, rode a suíte completa e rode-a também no branch base para ver se a falha já existia.

### 9.5 Comandos

```bash
./mvnw test                                       # unit tests
./mvnw test -Dtest="*Item*"                       # a subset
(set -o pipefail; ./mvnw test 2>&1 | grep -E "Tests run:|BUILD")   # summary, keeps the Maven exit status
```

A aplicação documenta como seus testes de integração rodam (por exemplo, `./mvnw verify` com uma propriedade que habilita os `*IT`).

## 10. Observabilidade e operação

### 10.1 Logs

- Use `org.jboss.logging.Logger`: `private static final Logger LOG = Logger.getLogger(ItemService.class);`.
- Nunca use `System.out` nem `System.err`.
- Dados pessoais (números de documento de identificação, endereços de email, telefones) são omitidos ou mascarados nos logs em todos os níveis, inclusive DEBUG. Uma exceção depende da política documentada da aplicação.

### 10.2 OpenAPI

O documento OpenAPI fica em `/q/openapi`. A Swagger UI fica em `/q/swagger-ui` só nos modos dev e test, a menos que a aplicação a habilite em produção com `quarkus.swagger-ui.always-include=true`. As aplicações podem mudar esses caminhos. Quando um frontend gera tipos a partir dele, uma mudança incompatível num DTO é coordenada com esse frontend na mesma mudança ou numa mudança vinculada.

### 10.3 Health

O `quarkus-smallrye-health` expõe `/q/health`, `/q/health/live` e `/q/health/ready`.

## 11. Antipadrões

| Não use | Use |
| --- | --- |
| Pacotes `javax.*` do Java EE substituídos pelo Jakarta EE | `jakarta.*` |
| Anotações do Spring (`@Service`, `@Repository`, `@Autowired`) | CDI com `@ApplicationScoped` e `@Inject` |
| Lombok | Getters e setters explícitos |
| `PanacheEntity` (active record) | Entidade JPA simples e uma implementação de repositório |
| Um service que injeta `PanacheRepository<T>` | A interface do repositório de `domain/` |
| Um resource que retorna uma entidade | Um DTO vindo de um service |
| Um resource que retorna um DTO sem `Response` | `Response.ok(dto).build()` |
| Um resource protegido sem `@RolesAllowed` | `@RolesAllowed` na classe |
| Um record declarado dentro de um resource | Um record em `application/dto/` |
| Campos de auditoria escritos à mão | A classe base de auditoria |
| Um `@ManyToOne` entre módulos | Uma coluna `Long <entity>Id` |
| Editar uma migração já mergeada | Uma migração nova |
| Um service base genérico de CRUD | Um service explícito por módulo |
| `@Transactional` num método privado | Um método público transacional |
| `application-<profile>.properties` | Prefixos `%<profile>.` no `application.properties` |

## 12. Checklist de pull request

Todo pull request de backend segue as seções que se aplicam. Um desvio é uma exceção e registra o dono, o motivo, o escopo, a data de expiração ou de revisão e a issue de acompanhamento exigidos pelo [índice dos padrões](README.pt-BR.md), seja no pull request, seja nas regras locais da aplicação.

- [ ] As anotações vêm dos pacotes canônicos (§1.2).
- [ ] As quatro camadas e suas dependências são respeitadas (§2.1, §2.2).
- [ ] Referências entre módulos usam IDs (§2.3).
- [ ] As entidades estendem a classe base de auditoria ou dizem por que não (§3.1).
- [ ] A interface do repositório está em `domain/` e a implementação Panache em `infrastructure/` (§3.2, §5.1).
- [ ] Os services são `@ApplicationScoped`, retornam DTOs e usam `@Transactional` nas escritas (§4.1).
- [ ] Os DTOs são records em `application/dto/` (§4.2).
- [ ] Os resources retornam `Response` e têm `@RolesAllowed` quando protegidos, `@Tag` e `@Operation` (§6.3, §6.4).
- [ ] As migrações novas são sequenciais, e as já mergeadas não mudaram (§7.2).
- [ ] Testes unitários cobrem a nova lógica de service e as transições de estado; cada novo resource protegido tem um teste de 401 (§9.4).
- [ ] `./mvnw clean compile` e `./mvnw test` passam.
