# Module 7 — Security, Identity & Zero-Trust Networking

**Production-Grade Microservices on AWS · BayAreaLa8s**

| | |
|---|---|
| **Duration** | 90 minutes lecture + 4 hours lab |
| **Week** | 7 of 10 |
| **Prerequisites** | Modules 2–4 |

---

## Learning Objectives

Students will be able to:

1. Explain **JWT** structure, validation, and trade-offs vs server-side sessions.
2. Configure **IAM execution and task roles** for ECS with least privilege.
3. Use **Secrets Manager** / environment patterns for secrets (never in Git).
4. Apply **security groups** and private subnets for defense in depth.
5. Conduct a lightweight **threat model** for the course platform.

---

## Session Agenda

| Segment | Time | Topic |
|---------|------|--------|
| Authentication & JWT | 25 min | Flow, bcrypt, Bearer tokens |
| IAM for ECS | 20 min | Execution vs task role |
| Secrets & config | 15 min | SM, SSM, .env.example |
| Network security | 15 min | SGs, private tasks, TLS extension |
| Threat modeling breakout | 10 min | STRIDE-lite exercise |
| Wrap-up | 5 min | Lab 07 |

**Diagrams:** [13-security-architecture](../docs/diagrams/13-security-architecture.md) · [AWS security stencil](../docs/diagrams/aws-stencils/png/13-security-iam-network-detail.png)

---

## 1. Authentication with JWT (25 minutes)

### 1.1 Registration and login flow

See sequence in [13-security-architecture](../docs/diagrams/13-security-architecture.md):

1. `POST /users` — password hashed with **bcrypt** (never store plaintext).
2. `POST /auth/login` — verify hash, return **JWT** `access_token`.
3. Protected routes — `Authorization: Bearer <token>`.

**Implementation:** `starters/python/user-service/app/auth.py`

### 1.2 JWT anatomy

```
header.payload.signature
```

| Part | Content |
|------|---------|
| **Header** | Algorithm (`HS256`), type |
| **Payload** | Claims: `sub`, `exp`, custom `user_id` |
| **Signature** | HMAC with `JWT_SECRET` |

**Validation checks:**

- Signature matches secret
- `exp` not passed
- Issuer/audience (if configured)

### 1.3 Stateless vs sessions

| JWT (stateless) | Server session |
|-----------------|----------------|
| No server store | Session DB/Redis |
| Easy horizontal scale | Requires sticky sessions or shared store |
| Hard to revoke instantly | Revoke session id |
| Secret compromise = bad | Same |

**Production extensions:** Short-lived access token + refresh token, rotation, denylist for logout.

### 1.4 Authorization vs authentication

- **Authentication:** Who are you?
- **Authorization:** What may you do?

Course focuses on auth; capstone may add role claims (`admin`, `customer`).

### 1.5 Password policy

Minimum length, complexity, rate limiting on login (extension), breach password list (Have I Been Pwned API).

---

## 2. IAM for ECS (20 minutes)

### 2.1 Two roles per task

| Role | Assumed by | Course permissions |
|------|------------|-------------------|
| **Task execution role** | ECS agent | `ecr:GetAuthorizationToken`, `logs:CreateLogStream`, pull images |
| **Task role** | Application | `events:PutEvents`, DynamoDB on orders table |

Defined in `infrastructure/terraform/iam.tf`.

### 2.2 Least privilege

Start with **minimum** actions and resources:

```hcl
# Conceptual — scope Resource to table ARN, not "*"
```

**Anti-pattern:** `AdministratorAccess` on task role “because it’s easier.”

### 2.3 IAM policy evaluation (quick)

1. Explicit deny wins
2. Allow if match
3. Default deny

### 2.4 Instance metadata (awareness)

Tasks do **not** use EC2 instance profile on Fargate the same way—**task role** credentials via container credentials endpoint.

**SSRF risk:** If app fetches user-supplied URLs, block `169.254.169.254` (threat modeling).

---

## 3. Secrets Management (15 minutes)

### 3.1 Never in Git

| Bad | Good |
|-----|------|
| `JWT_SECRET=abc` in repo | `.env.example` with placeholders |
| Secrets in Dockerfile | Runtime injection |

**Gitignored:** `.env`, `terraform.tfvars`, `*.tfstate`

### 3.2 AWS Secrets Manager vs SSM Parameter Store

| | Secrets Manager | Parameter Store |
|---|-----------------|-----------------|
| **Rotation** | Built-in for RDS etc. | Manual/Lambda |
| **Cost** | Per secret/month | Cheaper for plain config |
| **Course JWT** | Recommended for prod | SecureString OK for labs |

### 3.3 Injecting into ECS

Task definition `secrets` block maps SM ARN → env var (see `task-definition-user.example.json` in repo).

---

## 4. Network Security (15 minutes)

### 4.1 Defense in depth

```
Internet → ALB (public) → ECS tasks (private) → data stores
```

### 4.2 Security groups as firewalls

| SG | Rules (course) |
|----|----------------|
| ALB | Inbound 80 from world (lab); restrict to corp IP in enterprise |
| ECS | Inbound from ALB + self for inter-service |

**NACLs:** Subnet-level optional second layer.

### 4.3 TLS (extension)

Terminate **HTTPS** on ALB with ACM certificate; redirect HTTP→HTTPS.

### 4.4 Service-to-service auth (extension)

mTLS between services, or signed internal tokens—not required for base course.

---

## 5. Threat Modeling Breakout (10 minutes)

### STRIDE-lite prompts

| Threat | Example on platform | Mitigation |
|--------|---------------------|------------|
| **Spoofing** | Stolen JWT | Short expiry, HTTPS |
| **Tampering** | Modified order payload | Validation, authz |
| **Repudiation** | User denies order | Audit logs |
| **Info disclosure** | Logs contain passwords | Redact, structured logging |
| **DoS** | Flood `/orders` | Rate limit, WAF |
| **Elevation** | Task role too broad | Least privilege IAM |

**Breakout:** Groups pick two threats and present one mitigation each.

---

## Lab & Assignment

- **Lab 07:** [`labs/module-07/README.md`](../labs/module-07/README.md)
- **Checklist:** [`templates/security-checklist.md`](../templates/security-checklist.md)
- **Assignment 07:** [`assignments/module-07.md`](../assignments/module-07.md)

### Summary

Security is **layers**: identity, IAM, secrets, network, and observability. Microservices multiply attack surface—**contracts and roles** must be explicit.

---

## Discussion Questions

1. How do you revoke a JWT before `exp` without a session store?
2. Why should the execution role not include `dynamodb:*`?
3. What happens if `JWT_SECRET` is committed to a public GitHub repo?
4. Where would WAF sit relative to ALB?

---

*BayAreaLa8s · Production-Grade Microservices on AWS*
