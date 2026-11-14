English | [Português](java-quarkus-backend.pt-BR.md)

# Java/Quarkus backend

This standard applies to backend services built with Java, Quarkus and Maven. It sets the layering, naming, persistence, REST, security, test and observability rules that application repositories on this stack share. An application records its own module list, table prefixes, namespaces, roles, exact versions and stricter rules in its own repository, as described in [Using these standards](README.md#using-these-standards).

The examples use a neutral `inventory` module with an `Item` entity, the placeholder package `<base>` and English identifiers. They illustrate the rules; they are not compiled as part of this catalog.

## 1. Stack

### 1.1 Components

| Layer | Technology |
| --- | --- |
| Language | Java, an LTS release |
| Build | Maven through the Maven Wrapper (`mvnw`) |
| Runtime | Quarkus |
| REST | RESTEasy Reactive with Jackson |
| Persistence | Hibernate ORM with Panache |
| Validation | Hibernate Validator (Jakarta Validation) |
| Authentication | Quarkus OIDC (`quarkus-oidc`) against an OpenID Connect provider |
| Database | PostgreSQL |
| Migrations | Flyway (`quarkus-flyway`) |
| API description | `quarkus-smallrye-openapi` |
| Health checks | `quarkus-smallrye-health` |

This standard pins no version. Each application pins exact versions in its own files: the Java release (for example in `.sdkmanrc`), the Maven version in the wrapper properties, and the Quarkus platform and extensions in `pom.xml`. Additional extensions, such as a cache backend or an identity-provider admin client, are application decisions.

### 1.2 Canonical annotations

Use exactly these packages in new code, and replace other imports when you refactor.

| Purpose | Annotation | Package |
| --- | --- | --- |
| JPA entity | `@Entity`, `@Table`, `@Column`, `@Id`, `@ManyToOne`, … | `jakarta.persistence.*` |
| Bean Validation | `@NotNull`, `@NotBlank`, `@Size`, `@Valid` | `jakarta.validation.*` |
| CDI scope | `@ApplicationScoped`, `@Singleton`, `@RequestScoped` | `jakarta.enterprise.context.*`, `jakarta.inject.*` |
| Injection | `@Inject` | `jakarta.inject.Inject` |
| Transactions | `@Transactional` | `jakarta.transaction.Transactional` |
| JAX-RS | `@Path`, `@GET`, `@POST`, `@PathParam`, `@QueryParam`, `Response` | `jakarta.ws.rs.*`, `jakarta.ws.rs.core.*` |
| REST security | `@RolesAllowed`, `@PermitAll`, `@DenyAll` | `jakarta.annotation.security.*` |
| OpenAPI | `@Tag`, `@Operation`, `@Parameter`, `@APIResponse` | `org.eclipse.microprofile.openapi.annotations.*` |
| Exception mapper | `@ServerExceptionMapper` | `org.jboss.resteasy.reactive.server.ServerExceptionMapper` |
| Panache repository | `PanacheRepository<T>` | `io.quarkus.hibernate.orm.panache.PanacheRepository` |
| Panache sort | `Sort` | `io.quarkus.panache.common.Sort` |
| Declarative cache, when the application uses Quarkus Cache | `@CacheResult`, `@CacheInvalidate` | `io.quarkus.cache.*` |

Prohibited:

- Java EE `javax.*` packages replaced by Jakarta EE (such as `javax.persistence`, `javax.ws.rs`, `javax.inject`, `javax.validation`, `javax.transaction`); use their `jakarta.*` equivalents. Java SE packages such as `javax.sql` and `javax.crypto` remain allowed.
- Spring annotations (`@Service`, `@Repository`, `@Autowired`).
- `@Path` annotations from more than one package.

## 2. Module structure

### 2.1 Four layers

Every module has the same four layers. Do not add others.

```text
<base>.<module>/
├── domain/            ← JPA entities, enums, value objects, repository interfaces, domain exceptions
├── application/       ← services (@ApplicationScoped), mappers, orchestration
│   └── dto/           ← request and response DTOs (records)
├── infrastructure/    ← Panache repository implementations, external integrations
└── interfaces/        ← JAX-RS resources
```

### 2.2 One-way dependencies

```text
interfaces  →  application  →  domain
                                  ↑
                          infrastructure
```

- `domain/` imports from no other layer of its module.
- `application/` does not import from `interfaces/` or `infrastructure/`.
- `infrastructure/` imports from `domain/` to implement its contracts.
- `interfaces/` calls `application/`. It never creates or changes entities from `domain/` directly; it calls a service.

### 2.3 Cross-module references by ID

A module refers to another module's entities only through a `Long` ID. Never use `@ManyToOne` or import an entity across modules.

```java
// Correct: an entity in another module that refers to an item
@Column(name = "item_id", nullable = false)
private Long itemId;

// Prohibited
@ManyToOne
private Item item;
```

Relationships inside the same module may use JPA associations.

### 2.4 Modules and table prefixes

Each module that owns tables has its own short table prefix (for example `inv_` for `inventory`). Modules without tables, such as a shared module or a module that only aggregates queries, have no prefix. The application lists its modules and prefixes in its own documentation.

## 3. Domain layer

### 3.1 Entities

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

Rules:

1. An entity that holds business state extends the application's audit base class (`AuditedEntity` in these examples). The base class provides the creation and update timestamps, set in `@PrePersist` and `@PreUpdate`, and the creation and update actors, set by an entity listener from the user-context service (§6.6). Do not add these fields by hand.
2. An entity that does not extend the base class states the reason in a comment on the class. Append-only logs that record their own author and time, pure join tables, reference data and children of an audited parent are typical cases; each application decides which of them it accepts.
3. The primary key is `Long id` with `GenerationType.IDENTITY`.
4. Do not use Lombok. Write getters and setters explicitly; the application may set their layout.
5. Booleans are primitive fields with a default, such as `private boolean active = true;`, read through `isActive()`.
6. Enums use `@Enumerated(EnumType.STRING)`.
7. Dates use `LocalDate` for a date without time (`DATE`) and `LocalDateTime` for a timestamp (`TIMESTAMP`). Never use `java.util.Date`.
8. Short bounded strings use `@Column(length = N)` with `VARCHAR(N)`; long or free text uses `@Column(columnDefinition = "TEXT")` with `TEXT`.
9. State transitions and invariants live in entity methods, such as `publish()` above, not in services.

### 3.2 Repository interface

The repository interface lives in `domain/` and speaks in domain terms; it does not expose Panache.

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

Use one consistent method vocabulary across the application, in the language it chose for code identifiers. The names must not collide with Panache methods (`findById`, `list`, `count`, `delete`, `persist`, …): the implementation also implements `PanacheRepository`, and a method with the same name either fails to compile or replaces the Panache method. These examples use:

| Operation | Method |
| --- | --- |
| Find by ID | `fetchById(id)` returning `Optional` |
| Find by another field | `findBy<Field>(…)` returning `Optional` or `List` |
| Paginated list | `listPage(page, size)` |
| Filtered paginated list | `findBy<X>(x, page, size)` |
| Count all | `countAll()` |
| Count filtered | `countBy<X>(x)` |
| Create or update | `save(entity)` |
| Delete | `remove(entity)` |
| Existence | `existsBy<X>(x)` |

### 3.3 Domain exceptions

Keep a small set of shared exceptions in the shared module and map them to HTTP in one global exception mapper (`@ServerExceptionMapper` methods in one class).

| Exception (example name) | HTTP | When |
| --- | --- | --- |
| `ResourceNotFoundException` | 404 | No entity with the requested ID |
| `ResourceConflictException` | 409 | Duplicate or unique-constraint conflict |
| `PolicyViolationException` | 400 | Valid input that breaks a business rule in the current context |
| `AccessDeniedException` | 403 | Authenticated user without access to the resource |
| `IllegalStateException` | 409 | Invalid state transition |
| `ConstraintViolationException` (Bean Validation) | 400 | Invalid request input |

Do not create module-specific exceptions unless the domain needs the concept; such an exception extends a shared one so it keeps its HTTP status. The application defines the error body (for example `{ "status": 404, "message": "…" }`) and uses it for every mapped exception.

## 4. Application layer

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

Rules:

1. Services are `@ApplicationScoped`.
2. Services inject the repository interface from `domain/`, never its implementation.
3. Public write methods use `@Transactional`; read methods do not.
4. Never put `@Transactional` on a private method; the CDI proxy does not intercept it.
5. A private lookup helper throws the not-found exception, so every method reports a missing entity the same way.
6. Services return DTOs, never entities.
7. Paginated lists return the page wrapper (§6.5); short unpaginated lists return `List<T>`.

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

Each record goes in its own file; they are shown together here for brevity.

Rules:

1. DTOs are `record`s, not mutable classes.
2. Bean Validation annotations go only on request DTOs. An update request used by PUT replaces every editable field and carries the same constraints as create. A partial update (PATCH) that allows omitted fields needs a constraint that accepts `null` but applies the create rules to a supplied value, for example a custom constraint; the application documents it.
3. Naming: `<Entity>Dto` for a response, `<Entity>DetailDto` for a detailed or aggregated response, `<Entity>CreateRequest` and `<Entity>UpdateRequest` for writes, and `<Verb><Entity>Request` for other operations (for example `PublishItemRequest`).
4. DTOs live in `application/dto/`, never inline in a resource.
5. A DTO never contains an entity. To include data from another entity, build an aggregated DTO in the service or mapper.

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

Mappers are hand-written `@ApplicationScoped` beans. Do not use MapStruct or another mapping generator.

## 5. Infrastructure layer

### 5.1 Repository implementations

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

### 5.2 How Panache is used

Panache is the persistence standard, used only inside repository implementations:

- Entities are plain JPA classes; they do not extend `PanacheEntity`.
- Services never inject `PanacheRepository<T>` and never call Panache methods.
- A repository implementation implements the domain interface and `PanacheRepository<Entity>`, and uses Panache methods such as `findByIdOptional`, `find`, `findAll`, `count` and `persistAndFlush`.

This keeps services dependent only on `domain/`, so unit tests can mock them easily, while repository implementations stay short.

### 5.3 Native queries

For PostgreSQL features such as full-text search, JSONB or window functions, declare the method in the domain interface, inject `EntityManager` into the repository implementation and use a native query with bound parameters. Pass user search text to a function made for raw input, such as `websearch_to_tsquery` or `plainto_tsquery`; building a `to_tsquery` expression from user text fails on punctuation and operators.

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

## 6. Interfaces layer (REST)

### 6.1 API namespaces

Separate the API into namespaces by path prefix, for example `/api/public` for anonymous access and `/api/admin` for authenticated operators. Each namespace has an explicit authentication requirement and a role rule. The application documents its namespaces, their prefixes, the identity realm or tenant that authenticates each one and the roles each requires.

### 6.2 Resource names

Name a resource after its namespace and subject, with the namespace as a prefix: `Public<X>Resource`, `Admin<X>Resource`, and the same pattern for other namespaces. When editing a resource with an older name, keep it; renaming is a separate change.

### 6.3 Resource structure

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

### 6.4 Resource rules

1. Methods return `Response`, not a DTO, list or page directly. This keeps status codes explicit and makes headers such as `Location` or `ETag` easy to add. Convert older resources when you next change them.
2. Status codes: GET returns 200; a POST that creates returns 201 with `Location`; PUT and PATCH return 200; DELETE returns 204.
3. Request bodies (`*CreateRequest`, `*UpdateRequest` and other request DTOs) carry `@NotNull @Valid`: `@Valid` alone does not reject a missing or `null` body.
4. Every resource outside the anonymous namespace has `@RolesAllowed`. A missing role annotation is a security defect.
5. Every resource has `@Tag`, and every method has `@Operation(summary = …)`, so the generated OpenAPI is usable by clients.
6. No records or DTOs are declared inside a resource; they live in `application/dto/`.
7. Resources hold no business logic: they read parameters, call one service and build the `Response`.
8. Resources do not use `@Transactional`; transactions belong to services.
9. Resources never access repositories.
10. Pagination uses `@QueryParam("page") @DefaultValue("0")` and `@QueryParam("size") @DefaultValue("20")`. A short list usually shown whole, such as types or enumerations, may default to 50. Validate both parameters: `page` is between 0 and a maximum and `size` is between 1 and a maximum, both set by the application (10000 and 100 in the example), so an invalid value returns 400 instead of an error or an unbounded query. Choose the maximums so that the offset `page × size` fits in an `int`, which is what Panache and JPA accept as the first result.

### 6.5 Page wrapper

The application has exactly one generic page wrapper (`PagedResponse<T>` in these examples), built with a factory such as `PagedResponse.of(content, page, size, total)`. Its JSON shape is fixed and documented:

```json
{ "content": [], "page": 0, "size": 20, "total": 150, "totalPages": 8 }
```

### 6.6 User context

Resources and services get the authenticated user from one injectable user-context service of the application (`UserContext` in these examples), not from `SecurityIdentity` or token claims directly. That service is the only place that reads identity claims.

```java
@Inject
UserContext userContext;

String userId = userContext.currentUserId();
```

## 7. Database and migrations

### 7.1 Schema conventions

- Tables: `<prefix>_<snake_case>`, such as `inv_item`.
- Columns: `snake_case`, such as `available_from`.
- Primary key: `id BIGSERIAL PRIMARY KEY`.
- Foreign-key column: `<entity>_id BIGINT NOT NULL`, nullable only when the relationship is optional.
- Foreign-key constraints only inside one module; cross-module references are plain ID columns (§2.3).
- Indexes: `idx_<table>_<columns>`; unique constraints: `uk_<table>_<columns>`.
- Audit columns, on tables of audited entities (§7.3): creation and update timestamps as `TIMESTAMP NOT NULL`, creation and update actors as `VARCHAR(255)`, named by the application (for example `created_at`, `updated_at`, `created_by`, `updated_by`).

### 7.2 Flyway

- Migrations live in `src/main/resources/db/migration/` as `V<version>__<description>.sql`.
- Versions are sequential and never reused. Check the highest existing version before adding one.
- Never edit a migration after it is merged; add a new one. An application that needs a one-time exception documents it, with its scope and repair procedure, in its own standard.
- Migrations contain DDL and structural DML only. Demo or sample data goes in a separate seed location that only the development profile loads and the test profile excludes.
- Use PostgreSQL features where they help: JSONB, full-text search with `tsvector`, GIN indexes, generated columns.

### 7.3 Audit columns

For a table whose entity extends the audit base class, declare the four audit columns explicitly in the migration that creates the table; do not rely on Hibernate schema generation. The base class (§3.1) fills them. A table whose entity is an accepted exception (§3.1, rule 2) has no audit columns unless its own model needs them, such as the author and time of an append-only log entry.

### 7.4 Configuration

Keep configuration in one `application.properties`, with `%dev.`, `%test.` and `%prod.` profile prefixes. Do not create `application-<profile>.properties` files. Secrets and machine-specific values come from environment variables, never from versioned files.

## 8. Security

### 8.1 Authentication

Clients send an OIDC bearer token in the `Authorization` header, and `quarkus-oidc` validates it against the identity provider. When different user populations authenticate against different realms or tenants, the application documents which namespace each one serves and how requests are routed to it.

### 8.2 Roles

The application documents its roles: the name, the client applications that use it, what it grants, and how it is assigned. Resources reference those roles; they do not invent new ones.

### 8.3 Authorization in depth

1. Resource: a class-level `@RolesAllowed` is the first barrier.
2. Operation: a method-level `@RolesAllowed` replaces the class-level annotation for that method; it does not add to it. Use it when one operation needs a different role, and list every role that may call the method. When a caller must satisfy both conditions, check the second one explicitly in the service.
3. Service: when a role is not enough, the service checks ownership or tenancy (for example, a user sees only their own records) and throws the access-denied exception (403).
4. Public resources use their own DTOs, separate from authenticated DTOs, and never return sensitive fields.

### 8.4 Security rules

1. Every authenticated endpoint rejects anonymous requests with 401.
2. Public APIs return only fields that are safe to publish (§8.5).
3. Tokens never appear in logs.
4. Every request DTO is validated with Bean Validation (`@NotBlank`, `@Size`, `@Email`, …).
5. User-controlled values reach every query (Panache, JPQL and native) only as bound parameters, never by string concatenation. Dynamic identifiers, such as a sort field or direction chosen by the client, are mapped from an allowlist.
6. Untrusted text is safe to render: frontends encode or escape it for the output context (HTML text, attribute, URL, JavaScript), even though the API is JSON only. Where the product intends to render user-supplied HTML, the backend or the frontend cleans it with an allowlist-based HTML sanitizer.
7. CORS is configured per profile: local origins in development, an explicit list of origins in production, set through configuration.
8. Production traffic uses HTTPS; TLS may terminate at the reverse proxy.

### 8.5 Fields never returned by public APIs

- personal contact data such as email addresses, unless the law makes them public;
- internal user IDs;
- audit fields (who created or changed a record);
- tokens or session data;
- system configuration details.

### 8.6 Audit trail

Every write to a domain entity records an audit event through one application service (`AuditTrail` in the §4.1 example), called by the service method that performs the write in the same transaction: who (the user ID from the token), what (entity type, ID and changed fields), when (timestamp) and context (for example as JSONB).

### 8.7 CORS configuration

Configure CORS in `application.properties`, with the allowed production origins supplied by an environment variable.

## 9. Tests

### 9.1 Test types

| Type | Suffix | Runs with | Covers |
| --- | --- | --- | --- |
| Unit | `*Test.java` | JUnit 5 and Mockito, no container | services, mappers, domain logic |
| Integration | `*IT.java` | `@QuarkusTest` against PostgreSQL, through Testcontainers or a dedicated test database | resources, real repositories, migrations |

### 9.2 Unit test

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

### 9.3 Integration test

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

### 9.4 Test rules

1. Every protected resource has at least one integration test that expects 401 without a token.
2. Every entity state transition has a unit test.
3. Tests use their own database, configured under `%test`, and their own fixtures. They never depend on the development seed.
4. Claims beyond user and roles are set with `@JwtSecurity` (`quarkus-test-security-jwt`) together with `@TestSecurity`.
5. Known pitfalls:
   - A JSONB column mapped to `String` needs `@JdbcTypeCode(SqlTypes.JSON)` and `@Column(columnDefinition = "JSONB")`.
   - Two entities with the same simple name in different modules fail with `DuplicateMappingException` when `@QuarkusTest` starts, not at compile time. Give them distinct names.
   - `@TestSecurity` replaces token authentication only in the tests it annotates. When the test profile has no reachable identity provider, tests that use `@TestSecurity` can run with `%test.quarkus.oidc.enabled=false`; real bearer-token validation is then tested in a separate profile with a test provider (for example Keycloak Dev Services or an OIDC server mock).
   - A class-level `@TestSecurity` also applies to the 401 tests, and REST Assured's `.auth().none()` does not remove it. Put `@TestSecurity` on methods in classes that test 401.
   - Each new `@Inject` in a service with a unit test needs a matching `@Mock`; otherwise `@InjectMocks` leaves the field `null` without an error.
   - Some integration tests depend on order or shared data. Before calling a failure a regression, run the full suite, and run it on the base branch to see whether the failure already existed.

### 9.5 Commands

```bash
./mvnw test                                       # unit tests
./mvnw test -Dtest="*Item*"                       # a subset
(set -o pipefail; ./mvnw test 2>&1 | grep -E "Tests run:|BUILD")   # summary, keeps the Maven exit status
```

The application documents how its integration tests run (for example `./mvnw verify` with a property that enables `*IT`).

## 10. Observability and operations

### 10.1 Logging

- Use `org.jboss.logging.Logger`: `private static final Logger LOG = Logger.getLogger(ItemService.class);`.
- Never use `System.out` or `System.err`.
- Personal data (national ID numbers, email addresses, phone numbers) is omitted or masked in logs at every level, including DEBUG. An exception needs the application's documented policy.

### 10.2 OpenAPI

The OpenAPI document is served at `/q/openapi`. The Swagger UI is served at `/q/swagger-ui` in dev and test modes only, unless the application enables it for production with `quarkus.swagger-ui.always-include=true`. Applications may change these paths. When a frontend generates types from it, a breaking DTO change is coordinated with that frontend in the same change or a linked one.

### 10.3 Health

`quarkus-smallrye-health` exposes `/q/health`, `/q/health/live` and `/q/health/ready`.

## 11. Anti-patterns

| Do not use | Use |
| --- | --- |
| Java EE `javax.*` packages replaced by Jakarta EE | `jakarta.*` |
| Spring annotations (`@Service`, `@Repository`, `@Autowired`) | CDI with `@ApplicationScoped` and `@Inject` |
| Lombok | Explicit getters and setters |
| `PanacheEntity` (active record) | Plain JPA entity and a repository implementation |
| A service that injects `PanacheRepository<T>` | The repository interface from `domain/` |
| A resource that returns an entity | A DTO from a service |
| A resource that returns a DTO without `Response` | `Response.ok(dto).build()` |
| A protected resource without `@RolesAllowed` | Class-level `@RolesAllowed` |
| A record declared inside a resource | A record in `application/dto/` |
| Hand-written audit fields | The audit base class |
| A cross-module `@ManyToOne` | A `Long <entity>Id` column |
| Editing a merged migration | A new migration |
| A generic CRUD base service | An explicit service per module |
| `@Transactional` on a private method | A public transactional method |
| `application-<profile>.properties` | `%<profile>.` prefixes in `application.properties` |

## 12. Pull request checklist

Every backend pull request follows the sections that apply. A deviation is an exception and records the owner, reason, scope, expiry or review date and tracking issue required by the [standards index](README.md), whether it is written in the pull request or in the application's local rules.

- [ ] Annotations come from the canonical packages (§1.2).
- [ ] The four layers and their dependencies are respected (§2.1, §2.2).
- [ ] Cross-module references use IDs (§2.3).
- [ ] Entities extend the audit base class or state why not (§3.1).
- [ ] The repository interface is in `domain/` and its Panache implementation in `infrastructure/` (§3.2, §5.1).
- [ ] Services are `@ApplicationScoped`, return DTOs and use `@Transactional` on writes (§4.1).
- [ ] DTOs are records in `application/dto/` (§4.2).
- [ ] Resources return `Response` and have `@RolesAllowed` when protected, `@Tag` and `@Operation` (§6.3, §6.4).
- [ ] New migrations are sequential, and merged migrations are unchanged (§7.2).
- [ ] Unit tests cover new service logic and state transitions; each new protected resource has a 401 test (§9.4).
- [ ] `./mvnw clean compile` and `./mvnw test` pass.
