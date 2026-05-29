# Student Handbook

Welcome to **Production-Grade Microservices on AWS** (BayAreaLa8s).

## What You Will Build

An e-commerce style platform:

- **User Service** — registration and authentication
- **Product Service** — catalog
- **Order Service** — place orders, emit events
- **Notification Service** — react to domain events

## Weekly Checklist

- [ ] Attend lecture (slides in `lectures/`)
- [ ] Complete lab in `labs/module-XX/`
- [ ] Submit assignment (see `assignments/`)
- [ ] Push code to your GitHub repo

## Architecture diagrams

Visual guides for every module: [diagrams/README.md](diagrams/README.md)

Start with: [Platform overview](diagrams/01-platform-overview.md) → [Place order sequence](diagrams/08-sequence-place-order.md)

## Getting Started

```bash
git clone <your-repo-url>
cd Course-Production-Grade-Microservices-on-AWS
cp .env.example .env
docker compose up --build
```

Test the platform:

```bash
# Create user
curl -X POST http://localhost:8001/users \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","name":"Alex Student","password":"learn123"}'

# List products
curl http://localhost:8002/products

# Place order (use product id from previous response)
curl -X POST http://localhost:8003/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id":"<USER_ID>","items":[{"product_id":"<PRODUCT_ID>","quantity":1}]}'
```

## Tracks

| Track | Path |
|-------|------|
| Python (default labs) | `starters/python/` |
| Java | `starters/java/` |
| Node.js | `starters/nodejs/` |

All tracks must honor OpenAPI contracts in `contracts/openapi/`.

## Getting Help

1. Lab troubleshooting sections
2. Cohort discussion channel
3. Office hours (see syllabus)

## Academic Integrity

Collaborate on concepts; submit your own code and diagrams. Cite any external templates.

## Capstone

See `capstone/README.md` — start planning in Week 3.
