# Lab 2 — Build User & Product Services

**Duration:** 4 hours | **Module 2**

## Objectives

- Implement REST APIs matching OpenAPI contracts
- Apply validation and consistent error responses
- Run services locally and test with curl

## Prerequisites

- Python 3.12+ (or Java/Node track)
- Completed Lab 1

## Starter Code

Python (reference): `starters/python/user-service`, `starters/python/product-service`

```bash
cd starters/python/user-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

## Part A — User Service (90 min)

1. Review `contracts/openapi/user-service.yaml`
2. Implement or extend:
   - `POST /users` — register (409 on duplicate email)
   - `GET /users/{id}`
   - `POST /auth/login` — return JWT
3. Run tests: `pytest -q`

**Verify:**

```bash
curl -X POST http://localhost:8001/users \
  -H "Content-Type: application/json" \
  -d '{"email":"you@school.edu","name":"Your Name","password":"password123"}'
```

## Part B — Product Service (90 min)

1. Review `contracts/openapi/product-service.yaml`
2. Implement CRUD for products
3. Confirm seed data loads on startup

```bash
curl http://localhost:8002/products
```

## Part C — API Documentation (45 min)

- Export OpenAPI from FastAPI: `http://localhost:8001/docs`
- Save spec snapshots to `docs/your-name/api/`

## Part D — Error Handling Review (45 min)

Document how your services return:

- 400 validation errors
- 404 not found
- 409 conflicts

## Verify your work

```bash
docker compose up -d --build   # if not running
./labs/module-02/verify.sh
```

## Deliverables

- [ ] Working User and Product services
- [ ] OpenAPI export or screenshot of `/docs`
- [ ] Short `api-contracts.md` noting versioning strategy

## Extension

Add `PUT /products/{id}` for inventory updates.
