# Module 3 — Containerization & Local Distributed Systems

**Production-Grade Microservices on AWS · BayAreaLa8s**

| | |
|---|---|
| **Duration** | 90 minutes lecture + 4 hours lab |
| **Week** | 3 of 10 |
| **Prerequisites** | Module 2, Docker installed |

---

## Learning Objectives

Students will be able to:

1. Explain **images vs containers** and how layers affect build cache and security.
2. Write production-oriented **Dockerfiles** (dependency order, health checks, non-root where applicable).
3. Orchestrate four services locally with **Docker Compose** and environment-based configuration.
4. Describe how **Amazon ECR** fits into the deploy pipeline.
5. Apply container **security hygiene** (no secrets in layers, scan on push, pin bases).

---

## Session Agenda

| Segment | Time | Topic |
|---------|------|--------|
| Images & containers | 20 min | Layers, immutability, registries |
| Dockerfile engineering | 25 min | Cache, multi-stage, health checks |
| Docker Compose | 25 min | Networking, env vars, course stack |
| ECR & AWS path | 15 min | Registry, linux/amd64 for Fargate |
| Security & pitfalls | 5 min | Scanning, secrets, image size |

**Diagrams:** [07-local-docker-compose](../docs/diagrams/07-local-docker-compose.md)

---

## 1. Images vs Containers (20 minutes)

### 1.1 Concepts

| Concept | Definition | Analogy |
|---------|------------|---------|
| **Image** | Immutable, layered filesystem + metadata | Class / blueprint |
| **Container** | Running instance of an image | Object / process |
| **Registry** | Storage for images (Docker Hub, **ECR**) | App store for artifacts |

### 1.2 Why containers for microservices

- **Parity:** Same artifact from laptop → CI → ECS Fargate.
- **Isolation:** Dependencies bundled; no “works on my machine.”
- **Density:** Smaller unit than VMs; faster boot than full machines.
- **Versioning:** Tag images (`:abc123`) and roll back deployments.

### 1.3 Image layers and cache

Each Dockerfile instruction can create a **layer**. Docker reuses cached layers when inputs unchanged.

**Best practice order:**

1. Base image (`FROM python:3.12-slim`)
2. OS packages (rarely change)
3. **Dependency files** (`requirements.txt`) + `pip install`
4. Application code (`COPY app/`) — changes often

Changing code should **not** invalidate the dependency layer.

---

## 2. Dockerfile Engineering (25 minutes)

### 2.1 Course service Dockerfile pattern

Example from `starters/python/user-service/Dockerfile`:

- Slim Python base
- `WORKDIR /app`
- Copy `requirements.txt` → install → copy source
- Expose service port
- `CMD` runs Uvicorn

### 2.2 Multi-stage builds (concept)

| Stage | Purpose |
|-------|---------|
| **builder** | Compile wheels, run tests |
| **runtime** | Copy only artifacts—smaller attack surface |

For Python FastAPI, slim images often suffice; Java/Spring benefits more from multi-stage.

### 2.3 Health checks

Compose and ECS use health checks to know when a container is **ready**.

Course services expose `GET /health`:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
  interval: 30s
  timeout: 5s
  retries: 3
```

ECS task definitions use similar probes (Module 4).

### 2.4 Process model

- **One main process per container** (Uvicorn per service).
- Avoid systemd inside containers; let orchestrator restart failed tasks.

### 2.5 User identity

Run as **non-root** in production when possible (`USER app`). Reduces container escape impact.

---

## 3. Docker Compose — Local Distributed System (25 minutes)

### 3.1 Architecture

See [07-local-docker-compose](../docs/diagrams/07-local-docker-compose.md):

```
Host
 └── docker compose network
      ├── user-service:8001
      ├── product-service:8002
      ├── order-service:8003
      └── notification-service:8004
```

### 3.2 Service discovery (local)

Order service reaches Product via **environment variables**:

| Variable | Example (compose) |
|----------|---------------------|
| `PRODUCT_SERVICE_URL` | `http://product-service:8002` |
| `EVENT_HTTP_ENDPOINT` | `http://notification-service:8004/events` |

Docker Compose **DNS** resolves service names on the internal network.

### 3.3 docker-compose.yml walkthrough

Key sections:

- **build:** context per service
- **ports:** publish `8001:8001` for host access
- **environment:** URLs, `JWT_SECRET`, `DATABASE_URL` (SQLite in container)
- **depends_on:** startup order (does not wait for healthy—use healthchecks in production)

### 3.4 Commands students must know

```bash
docker compose up --build -d    # build & start detached
docker compose ps               # status
docker compose logs -f order-service
docker compose down             # stop & remove
docker compose exec user-service bash
```

### 3.5 Demo

```bash
make up          # or docker compose up --build -d
make demo        # ./scripts/demo-platform.sh
make test        # ./scripts/run-all-tests.sh
```

---

## 4. Amazon ECR & Path to AWS (15 minutes)

### 4.1 Elastic Container Registry

| Feature | Benefit |
|---------|---------|
| Private repos per service | Access via IAM |
| Image scanning | CVE detection on push |
| Lifecycle policies | Prune old tags |

Course Terraform creates four repositories: `user-service`, `product-service`, `order-service`, `notification-service`.

### 4.2 Build for Fargate architecture

**Critical:** Apple Silicon Macs build `arm64` by default; **ECS Fargate in this course uses `linux/amd64`.**

```bash
docker build --platform linux/amd64 -t <ecr-url>:latest .
```

Scripts `scripts/aws-start.sh` and `scripts/aws-deploy.sh` handle this.

### 4.3 Tagging strategy

| Tag | Use |
|-----|-----|
| `latest` | Dev only—mutable |
| `git-sha` | Traceability in prod |
| `v1.2.3` | Release semver |

---

## 5. Security & Common Pitfalls (5 minutes)

| Pitfall | Risk | Mitigation |
|---------|------|------------|
| Secrets in Dockerfile `ENV` | Leak via image history | Secrets Manager / runtime env |
| `:latest` in production | Unpredictable deploys | Immutable tags |
| Huge images | Slow deploy, CVE surface | Slim bases, multi-stage |
| Root user | Privilege escalation | `USER` directive |
| No health check | Traffic to broken tasks | `/health` + ECS checks |

**Scan on push:** Enable ECR scanning; fail CI on critical CVEs (extension).

---

## Lab & Assignment

- **Lab 03:** [`labs/module-03/README.md`](../labs/module-03/README.md)
- **Verify:** `./labs/module-03/verify.sh`
- **Assignment 03:** [`assignments/module-03.md`](../assignments/module-03.md)

### Pre-read for Week 4

- Skim [`infrastructure/terraform/`](../infrastructure/terraform/)
- Review [10-aws-deployment-architecture](../docs/diagrams/10-aws-deployment-architecture.md) and [AWS stencil VPC diagram](../docs/diagrams/aws-stencils/png/10-vpc-ecs-deployment-detail.png)

---

## Discussion Questions

1. Why copy `requirements.txt` before application code in a Dockerfile?
2. What breaks if Order Service uses `localhost:8002` inside a container?
3. Why must images be `linux/amd64` for this course’s Fargate deployment?
4. How is Compose networking different from ECS `awsvpc` mode?

---

*BayAreaLa8s · Production-Grade Microservices on AWS*
