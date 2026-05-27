# Self-Serve Enterprise File Transfer on AWS

**BayAreaLa8s · BayLearn Academy**  
*Commercial training program — master curriculum document*

---

## 1. Course overview

Modern enterprises still depend on **batch file exchange**—payroll feeds, claims files, vendor catalogs, regulatory submissions—while demanding **cloud scale**, **auditability**, and **self-service** for business and integration teams. Legacy MFT appliances and ad-hoc scripts fail on cost, velocity, and governance.

**Self-Serve Enterprise File Transfer on AWS** teaches how to design and implement a **governed, API-driven file transfer platform** on AWS: managed protocols (SFTP/FTPS), object storage landing zones, identity and encryption, workflow orchestration, observability, and optional **agent-assisted** operations—without sacrificing enterprise controls.

Participants progress from **Transfer Family fundamentals** through **automation (Lambda, Step Functions)**, **self-serve portals (Cognito + API)**, and a **capstone reference architecture** suitable for production proposals and internal platform roadmaps.

### Who should attend

- Cloud / platform engineers building integration platforms  
- Solutions architects owning B2B file exchange  
- DevOps and SRE engineers modernizing MFT  
- Integration developers (SFTP, EDI, flat-file pipelines)  
- Technical leads evaluating AWS vs. legacy MFT  

### Prerequisites

- AWS account with admin access in a **sandbox** (not production)  
- Comfort with IAM, VPC basics, S3, and CloudWatch  
- Familiarity with one IaC tool (Terraform preferred in labs)  
- Optional: Python or Node.js for Lambda labs  

---

## 2. Learning outcomes

By the end of this program, participants will be able to:

1. **Explain** enterprise file-transfer patterns (push/pull, hub-and-spoke, landing zones, idempotency) and map them to AWS services.  
2. **Design** secure SFTP/FTPS endpoints using **AWS Transfer Family** with IAM-scoped access to S3.  
3. **Implement** server-side and connector-based flows (`S3 ↔ SFTP`, multi-party routing).  
4. **Automate** transfers with **Lambda**, **Step Functions**, and **EventBridge** including retries, checkpoints, and dead-letter handling.  
5. **Apply** encryption (KMS), least-privilege IAM, VPC endpoints, and audit logging for compliance-ready designs.  
6. **Build** a **self-serve** experience: authenticated users, connection catalog, job history, and operational runbooks.  
7. **Operate** platforms with CloudWatch metrics, alarms, structured logging, and cost controls.  
8. **Deliver** a **capstone** architecture document, IaC skeleton, and demo script aligned to stakeholder review.  

---

## 3. Enterprise use cases

| Use case | Business driver | AWS pattern |
|----------|-----------------|-------------|
| **B2B vendor inbound** | Partners upload catalogs/invoices | Transfer Family SFTP → S3 landing → processing pipeline |
| **Payroll / HR outbound** | Regulated delivery to banks | S3 → SFTP connector, scheduled Step Functions |
| **Healthcare / claims** | HIPAA-style controls, audit | KMS, bucket policies, CloudTrail, least privilege |
| **Financial regulatory filing** | Immutable audit trail | S3 Object Lock, versioning, segregated accounts |
| **Retail EDI / flat files** | High volume, many partners | Per-partner IAM roles, prefix isolation |
| **Insurance FNOL / documents** | Spiky uploads, self-serve | Cognito + API catalog + Transfer users |
| **Manufacturing IoT batches** | Large files, resumable | Multipart S3, transfer over VPC |
| **Legacy MFT migration** | Exit data center MFT | Phased: protocol parity → automation → decommission |

---

## 4. Eight-week syllabus (summary)

| Week | Theme | Key topics | Deliverable |
|------|-------|------------|-------------|
| **1** | Enterprise MFT on AWS | Patterns, Transfer Family, S3 landing zones | Architecture diagram + SFTP endpoint |
| **2** | Security & governance | IAM, KMS, VPC, logging, compliance framing | Security baseline checklist |
| **3** | Automation core | Lambda, S3 events, idempotency | Event-driven copy/validate function |
| **4** | Orchestration | Step Functions, retries, DLQ | Multi-step transfer workflow |
| **5** | Connectors & multi-hop | SFTP connectors, routing, partner model | Connector lab + partner matrix |
| **6** | Self-serve platform | Cognito, API Gateway, catalog, jobs | API + minimal UI or Postman collection |
| **7** | Operations & scale | Observability, cost, DR, runbooks | Operations runbook draft |
| **8** | Capstone | End-to-end platform + presentation | Capstone package (see `docs/capstone.md`) |
| **9** *(stretch)* | ECS Fargate large files | Fargate worker + SHA-256 manifest ([Lab 9](docs/labs/lab-09-ecs-fargate-large-files.md)) |

Detailed weekly objectives, readings, and discussion prompts: [`docs/syllabus/`](docs/syllabus/).  
**Full instructional module content (lectures, diagrams, labs alignment, knowledge checks):** [`docs/modules/`](docs/modules/).

---

## 5. Hands-on labs and deliverables

| Lab | Week | Hours (est.) | Output |
|-----|------|--------------|--------|
| Lab 1: Transfer Family SFTP server | 1 | 3 | Working SFTP → S3 upload |
| Lab 2: Security hardening | 2 | 3 | Hardened roles + KMS-encrypted bucket |
| Lab 3: S3 event processor | 3 | 4 | Lambda validate/route |
| Lab 4: Step Functions workflow | 4 | 4 | Stateful transfer state machine |
| Lab 5: SFTP connector flows | 5 | 4 | S3 ↔ remote SFTP demo |
| Lab 6: Self-serve API surface | 6 | 5 | Connections + jobs API |
| Lab 7: Observability pack | 7 | 3 | Dashboards + alarms |
| Lab 8: Capstone integration | 8 | 8+ | Full demo path |
| Lab 9: ECS Fargate large files *(stretch)* | 5+ | 4 | Large-file worker + manifest |

Full instructions: [`docs/labs/`](docs/labs/).

---

## 6. Capstone projects

Participants choose **one** track (or hybrid with instructor approval):

### Track A — Self-serve control plane

Build a minimal **connection catalog**, **job submission API**, and **status/history** store (DynamoDB) with Cognito-authenticated access. Demo: business user registers a connection template; operator triggers S3→SFTP job.

### Track B — Governed automation hub

Implement **Step Functions**-orchestrated transfers with **idempotency keys**, partner-scoped IAM, and **audit export** to S3/CloudWatch. Demo: replay-safe transfer with failure injection.

### Track C — Migration accelerator

Document **as-is MFT** (hypothetical or real anonymized) and deliver **to-be AWS architecture**, phased cutover plan, and Terraform module layout.

Rubrics and submission checklist: [`docs/capstone.md`](docs/capstone.md).

---

## 7. Assessment structure

| Component | Weight | Description |
|-----------|--------|-------------|
| Weekly labs | 40% | Rubric per lab (completeness, security, operability) |
| Quizzes (weeks 1–6) | 15% | 10–15 questions/week, open-book |
| Participation / reviews | 10% | Architecture reviews, peer feedback |
| Capstone | 35% | Architecture + demo + documentation |

Pass threshold: **≥ 80%** overall with **capstone ≥ 70%**.  
Details: [`docs/assessment.md`](docs/assessment.md).

---

## 8. Career outcomes

Graduates are prepared for roles such as:

- **Cloud Integration Engineer** — AWS file pipelines and partner onboarding  
- **Platform Engineer (MFT)** — Internal self-serve transfer products  
- **Solutions Architect** — B2B and regulated file-exchange designs  
- **DevOps / SRE** — Operate Transfer Family and workflow automation  

Skills matrix and interview topics: [`docs/career-outcomes.md`](docs/career-outcomes.md).

---

## 9. Technologies covered

**Core:** AWS Transfer Family, Amazon S3, IAM, AWS KMS, Amazon VPC, AWS Lambda, AWS Step Functions, Amazon EventBridge, Amazon DynamoDB, Amazon API Gateway, Amazon Cognito, Amazon CloudWatch, AWS CloudTrail, Terraform (labs).

**Lab 9 (included in Terraform stack):** Amazon ECS Fargate workers for large/long file processing — see `docs/modules/week-09-ecs-fargate.md`.

**Additional stretch:** Amazon Bedrock Agents, OpenSearch Serverless (knowledge bases) — aligned to agentic control-plane patterns.

Service matrix and prerequisites: [`docs/technologies.md`](docs/technologies.md).

---

## 10. BayAreaLa8s positioning and value proposition

### Why BayAreaLa8s

BayAreaLa8s delivers **production-aligned** training—not slide-only cloud overview. Curriculum is informed by real **self-serve** and **orchestration** implementations (BayServe-style portals, BayRelay-style deterministic execution) used in enterprise workshops and consulting engagements.

### Value proposition

| Stakeholder | Value |
|-------------|-------|
| **Learners** | Job-ready patterns, portfolio capstone, interview-ready architecture narratives |
| **L&D / enterprise** | 8-week measurable outcomes, labs with artifacts, proposal-ready syllabus |
| **BayLearn academy** | Standardized modules, LMS manifest, brochure + listing copy |
| **Consulting alignment** | Graduates speak the same language as BayAreaLa8s delivery teams |

### BayLearn delivery modes

- **Public cohort** — Fixed schedule, cohort Slack/forum, group office hours  
- **Private corporate** — Custom partner scenarios, NDA-friendly capstone briefs  
- **Workshop intensive** — 3–5 day executive + builder hybrid (weeks 1–4 compressed)  
- **Train-the-trainer** — Instructor guide addendum (available on enterprise contract)  

### Differentiators

1. **Self-serve by design** — Not only SFTP pipes; catalog, identity, and job visibility.  
2. **Governance first** — IAM, KMS, audit, and idempotency woven through every week.  
3. **Automation-native** — Step Functions and event-driven patterns, not cron-on-EC2.  
4. **Capstone = proposal artifact** — Suitable for internal funding and vendor comparisons.  

---

## 11. Instructor resources

- Weekly slides: derive from [`docs/syllabus/`](docs/syllabus/) learning objectives  
- Solution sketches: available to **licensed instructors** under enterprise contract  
- Demo AWS account: isolated OU, SCP guardrails, monthly budget alarm  
- Academic integrity: learners use own sandboxes; capstone must be original work  

---

## 12. Document version

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Status** | Ready for LMS, proposals, and BayLearn catalog |
| **Last updated** | 2026-05-27 |
