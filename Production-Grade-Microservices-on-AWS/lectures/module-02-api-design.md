# Module 2 — API Design & Contract-Driven Development

**Production-Grade Microservices on AWS · BayAreaLa8s**

| | |
|---|---|
| **Duration** | 90 minutes lecture + 4 hours lab |
| **Week** | 2 of 10 |
| **Prerequisites** | Module 1, HTTP/REST basics |

---

## Learning Objectives

Students will be able to:

1. Apply **API-first** workflow: OpenAPI spec before implementation.
2. Design **RESTful** resources with correct HTTP verbs, status codes, and error shapes.
3. Explain **contract-driven development** across Python, Java, and Node tracks.
4. Trace the **place-order** synchronous path across User, Product, Order, and Notification services.
5. Navigate and test APIs using **FastAPI OpenAPI** (`/docs`) and the course contracts.

---

## Session Agenda

| Segment | Time | Topic |
|---------|------|--------|
| API-first & contracts | 15 min | OpenAPI, versioning, consumer-driven mindset |
| REST design | 25 min | Resources, verbs, status codes, pagination |
| Validation & errors | 20 min | Consistent error JSON, 4xx vs 5xx |
| Live demo | 25 min | Docker Compose + `/docs` walkthrough |
| Multi-track & wrap-up | 5 min | Java/Node alignment, Lab 02 |

**Diagrams:** [05-c4-container](../docs/diagrams/05-c4-container-diagram.md) · [06-api-contracts](../docs/diagrams/06-api-contracts.md) · [08-sequence-place-order](../docs/diagrams/08-sequence-place-order.md)

---

## 1. API-First Development (15 minutes)

### 1.1 Why design the API before code?

In microservices, the **API is the product** your team sells to other teams. Changing it without notice breaks consumers.

**API-first workflow:**

1. Product + engineering agree on use cases.
2. Architects draft **OpenAPI 3.x** in `contracts/openapi/`.
3. Review with consumers (Order team needs Product’s catalog API).
4. Implement service; generate mocks/tests from spec.
5. Publish versioned docs (Swagger UI, portal, or repo).

### 1.2 Contract-driven development (CDD)

| Role | Responsibility |
|------|----------------|
| **Provider** | Implements spec; does not break consumers without version bump |
| **Consumer** | Codes against spec; contract tests in CI |
| **Platform** | Stores contracts in Git; optional breaking-change checks |

**Course repo layout:**

```
contracts/
  openapi/
    user-service.yaml
    product-service.yaml
    order-service.yaml
  events/
    order-placed.json
```

Python services are the **reference implementation**. Java (`starters/java/`) and Node (`starters/nodejs/`) must match the same contracts.

### 1.3 Versioning strategies

| Strategy | Example | When to use |
|----------|---------|-------------|
| **URL path** | `/v1/users`, `/v2/users` | Clear, cache-friendly; course default for extensions |
| **Header** | `Accept: application/vnd.company.v2+json` | Avoid URL pollution |
| **Additive changes** | New optional fields | Preferred—no version bump if non-breaking |

**Breaking changes (require new version):** Remove field, change type, rename field, new required field.

**Deprecation policy (enterprise):** Announce sunset date, monitor traffic, remove after window.

---

## 2. REST Best Practices (25 minutes)

### 2.1 Resource-oriented URLs

Use **nouns** for resources, not verbs:

| Good | Avoid |
|------|-------|
| `POST /users` | `POST /createUser` |
| `GET /products/:id` | `GET /getProduct` |
| `POST /orders` | `POST /placeOrder` (acceptable as action on collection) |

**Course API surface** (see diagram 06):

| Service | Key endpoints |
|---------|---------------|
| User :8001 | `POST /users`, `POST /auth/login`, `GET /users/:id` |
| Product :8002 | `GET /products`, `GET /products/:id`, `POST /products` |
| Order :8003 | `POST /orders`, `GET /orders/:id` |
| Notification :8004 | `POST /events`, `GET /events` |

### 2.2 HTTP methods and safety

| Method | Safe? | Idempotent? | Typical use |
|--------|-------|-------------|-------------|
| GET | Yes | Yes | Read |
| POST | No | No | Create |
| PUT | No | Yes | Replace |
| PATCH | No | No* | Partial update |
| DELETE | No | Yes | Remove |

*PATCH idempotency depends on implementation.

### 2.3 Status codes (course standard)

| Code | Meaning | Course example |
|------|---------|----------------|
| **200** | OK | Login success, GET product |
| **201** | Created | Register user, create order |
| **400** | Bad request | Validation failure |
| **401** | Unauthorized | Missing/invalid JWT |
| **404** | Not found | Unknown product in order |
| **409** | Conflict | Duplicate email |
| **422** | Unprocessable (FastAPI validation) | Invalid body schema |
| **500** | Server error | Unhandled exception—fix in prod |
| **503** | Unavailable | Downstream timeout (extension) |

**Teaching rule:** Do not return `200` with `{ "error": true }`—use proper HTTP semantics.

### 2.4 Request/response examples

**Register user:**

```http
POST /users HTTP/1.1
Content-Type: application/json

{"email": "student@example.com", "password": "SecurePass123!"}
```

```http
HTTP/1.1 201 Created
Content-Type: application/json

{"user_id": "usr_abc123", "email": "student@example.com"}
```

**Create order (simplified):**

```json
{
  "user_id": "usr_abc123",
  "items": [{"product_id": "prod_1", "quantity": 2}]
}
```

Order service **calls Product** for price/stock—not a shared DB.

### 2.5 Pagination & filtering (catalog)

For `GET /products`:

| Pattern | Example |
|---------|---------|
| Limit/offset | `?limit=20&offset=40` |
| Cursor | `?cursor=eyJpZCI6...` (production at scale) |

Document in OpenAPI with `parameters` section.

---

## 3. Validation & Error Handling (20 minutes)

### 3.1 Consistent error shape

All course services return structured errors:

```json
{
  "detail": "Validation error",
  "errors": [
    {"field": "email", "message": "invalid email format"}
  ]
}
```

**Why it matters:** Mobile and web clients parse one schema; observability can index `detail`.

### 3.2 Validation layers

| Layer | Responsibility |
|-------|----------------|
| **Schema** | Pydantic / OpenAPI types (required fields, formats) |
| **Business** | “Insufficient stock”, “User not found” → 404/409 |
| **Infrastructure** | DB down → 503 with retry guidance |

### 3.3 Security in errors

**Never expose:** stack traces to clients in production, internal hostnames, SQL fragments.

Log full detail server-side (Module 8).

---

## 4. C4 Container Diagram & Place-Order Flow (integrated in demo)

### 4.1 Containers (Level 2)

[05-c4-container-diagram](../docs/diagrams/05-c4-container-diagram.md) shows deployable units:

- ALB (AWS) or localhost paths (local)
- Four FastAPI containers
- EventBridge (AWS) / HTTP events (local)
- Data stores per service

### 4.2 Sequence: place order

Walk through [08-sequence-place-order](../docs/diagrams/08-sequence-place-order.md):

1. Register → `POST /users`
2. Login → `POST /auth/login` → JWT
3. Browse → `GET /products`
4. Checkout → `POST /orders`
5. Order → `GET /products/:id` per line item
6. Order → `POST /events` (OrderPlaced) to Notification
7. Customer → `GET /events` to verify

**Failure scenarios (discussion):** Product 404, Product timeout—what should Order return?

---

## 5. Live Demo (25 minutes)

### 5.1 Start platform

```bash
cd <course-repo>
docker compose up --build -d
./scripts/demo-platform.sh   # optional end-to-end script
```

### 5.2 OpenAPI UI

| Service | Swagger URL |
|---------|-------------|
| User | http://localhost:8001/docs |
| Product | http://localhost:8002/docs |
| Order | http://localhost:8003/docs |
| Notification | http://localhost:8004/docs |

### 5.3 Demo script (instructor)

1. Create user via `/docs` on port 8001.
2. Login; copy `access_token`.
3. List products on 8002 (seeded data).
4. Create order on 8003 with valid `product_id`.
5. Show events on 8004.

### 5.4 Contract verification

```bash
./scripts/run-all-tests.sh
./labs/module-02/verify.sh
```

---

## 6. Multi-Track Note & Wrap-Up (5 minutes)

| Track | Path | Requirement |
|-------|------|---------------|
| **Python** | `starters/python/*` | Reference—extend in labs |
| **Java** | `starters/java/README.md` | Implement same OpenAPI |
| **Node** | `starters/nodejs/README.md` | Implement same OpenAPI |

**Lab 02:** [`labs/module-02/README.md`](../labs/module-02/README.md)  
**Assignment 02:** [`assignments/module-02.md`](../assignments/module-02.md)

### Summary

- **OpenAPI first** reduces integration pain.
- **REST semantics** and **status codes** are part of the public contract.
- **Place-order** flow is the backbone narrative for the rest of the course.

---

## Discussion Questions

1. Why should Order Service not expose Product’s database schema in its API responses?
2. When is a new URL version (`/v2`) required vs adding an optional JSON field?
3. How do contract tests differ from unit tests?
4. What HTTP status should Order return if Product Service times out?

---

*BayAreaLa8s · Production-Grade Microservices on AWS*
