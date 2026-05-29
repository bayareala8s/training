# Module 2 Lecture — API Design & Development

**Duration:** 90 minutes

## 1. API-First Development (15 min)

- Design OpenAPI before implementation
- Contract-driven development between teams
- Versioning: URL (`/v1`) vs header

## 2. REST Best Practices (25 min)

- Nouns for resources (`/users`, `/orders`)
- HTTP verbs correctly (GET safe, POST create)
- Status codes: 201, 400, 404, 409, 500
- Pagination, filtering (preview for catalog)

## 3. Validation & Errors (20 min)

```json
{
  "detail": "Validation error",
  "errors": [{"field": "email", "message": "invalid format"}]
}
```

Consistent error shape across all course services.

## 4. Live Demo (25 min)

Walk through FastAPI `/docs` for user-service and product-service.

```bash
docker compose up --build
```

## 5. Multi-Track Note (5 min)

Python labs are reference; Java/Node must match `contracts/openapi/`.

## Lab

`labs/module-02/README.md`
