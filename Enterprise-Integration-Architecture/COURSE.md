# Enterprise Integration Architecture

**BayAreaLa8s · BayLearn Academy**  
*Master curriculum — APIs, Messaging, Events, File Transfers, ESB & AI Agents*

**Subtitle:** Master APIs, Messaging, Events, File Transfers, ESB Modernization & AI-Agent Integration through Real-World Enterprise Architecture Labs.

| Attribute | Detail |
|-----------|--------|
| **Course ID** | `baylearn-eia-001` |
| **Level** | Advanced |
| **Duration** | 16 weeks · 90–120 hours |
| **Format** | Instructor-led (ILT), virtual ILT, hybrid, or self-paced with labs |
| **Passing grade** | Required modules, labs, architecture challenges, and four capstones |
| **Certificate** | BayLearn Certificate of Completion — Enterprise Integration Architecture |
| **Version** | 1.0.0 |
| **Status** | Ready for LMS, proposals, and BayLearn catalog |

---

## 1. Course objective

Build a complete hands-on BayLearn course that teaches students how to **design, build, secure, operate, troubleshoot, and modernize** enterprise integration architectures.

This is **not** a simple AWS services tutorial.

The primary learning objective:

> Teach students how an Enterprise Architect decides when and why to use APIs, messaging, event-driven architecture, file transfer, ESB/integration platforms, or AI-agent-based integration.

Students must repeatedly make architecture decisions rather than simply follow implementation instructions.

The course combines architecture concepts, enterprise integration patterns, AWS implementation, hands-on labs, architecture decision records, failure scenarios, security, observability, cost, AI/agent integration, legacy modernization, and four real-world capstones.

### Differentiator

```text
Business Requirement → Integration Characteristics → Pattern → Architecture
        → Technology → Implementation → Failure Testing → Operations
```

**Not:** AWS Service → Tutorial.

Every module answers three questions:

| Question | Meaning |
|----------|---------|
| **WHY?** | Why does this architecture or pattern exist? |
| **WHEN?** | When should an Enterprise Architect use it? |
| **HOW?** | How is it implemented in a real enterprise environment? |

Architecture decisions and tradeoffs matter more than memorizing AWS services.

---

## 2. Target audience

**Primary:** Enterprise Architects, Solution Architects, Integration Architects, Cloud Architects, Senior Software Engineers, Platform Engineers, Integration Engineers.

**Secondary:** DevOps Engineers, Backend Engineers, Technical Leads, Engineering Managers, and developers moving toward architecture roles.

---

## 3. Prerequisites

Students should understand:

- Basic AWS concepts
- HTTP, REST, JSON
- Basic Python
- Cloud fundamentals and IAM basics
- Basic distributed systems concepts

Do **not** require prior experience with Kafka, EventBridge, AWS Transfer Family, ESB, MCP, or AI agents. Those are introduced in the course.

**Lab environment:** AWS sandbox account (not production), AWS CLI, Terraform ≥ 1.5, Python 3.10+ (Lambda runtime 3.12).

---

## 4. Course outcomes

By completing the course, students should be able to:

1. Identify enterprise integration requirements.
2. Select the correct integration pattern.
3. Design synchronous integrations.
4. Design asynchronous integrations.
5. Design event-driven systems.
6. Build REST APIs.
7. Implement queues and pub/sub architectures.
8. Design enterprise file-transfer solutions.
9. Understand ESB architecture.
10. Modernize legacy ESB integrations.
11. Implement retry and failure-handling patterns.
12. Implement idempotent consumers.
13. Design DLQ and replay mechanisms.
14. Secure integrations.
15. Implement integration observability.
16. Design large-file processing architectures.
17. Design cross-enterprise integration.
18. Integrate AI agents with enterprise systems.
19. Apply human approval to agentic actions.
20. Create Architecture Decision Records.
21. Defend architecture choices.
22. Build production-oriented enterprise integration platforms.

---

## 5. Core architecture decision framework

This framework appears throughout the course. Students repeatedly answer:

> Should this integration use an **API**, **Message**, **Event**, **File**, **ESB/Adapter**, or **AI Agent**?

| Style | Use when | Do not use when | AWS examples |
|-------|----------|-----------------|--------------|
| **API** | Immediate response; consumer knows provider; request/reply; small payloads; real-time read | Large files; fire-and-forget work; unknown consumers | API Gateway, Lambda |
| **Message / Queue** | Async processing; guaranteed delivery; decoupling; work must survive outages; back-pressure | Broadcast to unknown consumers; “something happened” notifications | SQS |
| **Event** | Something happened; multiple consumers may react; producer should not know consumers | Command that must be processed by exactly one worker | EventBridge, SNS |
| **File** | Large/batch datasets; partners use SFTP; legacy cannot expose APIs | Low-latency single-record lookup | S3, Transfer Family |
| **ESB / Adapter** | Legacy protocols; central transformation still required; bus cannot be replaced immediately | Greenfield distributed systems; using the bus as a dumping ground | Conceptual + adapters |
| **AI Agent** | Natural language; tool orchestration; reasoning before action; operational assistant | Unrestricted data access; irreversible writes without policy | Bedrock + governed tools |

**Mandatory agent architecture:**

```text
User → Agent → Governed Tool → Integration Layer → Enterprise System
```

Never: `LLM → Production Database`.

---

## 6. Course structure

15 core modules + 4 capstones + final architecture assessment.

| # | Module | Lessons (selected) | Lab |
|---|--------|--------------------|-----|
| 1 | Enterprise Integration Fundamentals | Styles, sync vs async, P2P, decision framework | Classification of 15 requirements |
| 2 | API-Based Integration | REST, contracts, versioning, auth, idempotency | POST/GET orders |
| 3 | Enterprise Messaging | Delivery semantics, visibility, DLQ, FIFO | Producer → SQS → DLQ → replay |
| 4 | Pub/Sub Architecture | Fan-out, filtering, independent consumers | OrderCreated → 3 queues |
| 5 | Event-Driven Architecture | Events vs messages, EventBridge, replay, versioning | Order choreography |
| 6 | Enterprise File Transfer | SFTP, MFT, validation, checksums, archival | File landing + catalog (Transfer optional) |
| 7 | Large File Architecture | Claim Check, presigned upload, status API | Direct-to-S3 upload |
| 8 | ESB & Traditional Integration | Routing, transformation, canonical model, limits | Decision exercises |
| 9 | ESB Modernization | Strangler, distributed cloud integration | Legacy redesign + ADR |
| 10 | Enterprise Integration Patterns | 17 EIP with AWS mapping | Pattern challenges |
| 11 | Reliability & Resiliency | Timeouts, backoff, circuit breaker, idempotency | Chaos lab |
| 12 | Security | IAM, KMS, secrets, isolation, audit | Insecure architecture fix |
| 13 | Observability | Correlation, traces, business vs technical metrics | Operations dashboard |
| 14 | Architecture Decision Making | NFR → pattern → tech → ADR | Three scenario challenges |
| 15 | Integration Architecture for AI Agents | Tools, MCP, HITL, agent security | Operations agent |

---

## 7. Capstone projects

Each capstone is an enterprise architecture engagement. **Do not reveal the final architecture immediately.** Students receive business requirements, NFRs, constraints, existing architecture, and an integration inventory. They must design, then implement.

| Capstone | Domain | Portfolio title |
|----------|--------|-----------------|
| 1 | Banking payment integration | Enterprise Payment Integration Platform |
| 2 | E-commerce order platform | Event-Driven Commerce Platform |
| 3 | Healthcare interoperability | Secure Healthcare Integration Platform |
| 4 | Global manufacturing / supply chain | Global Supply Chain Integration Platform |

Each produces: architecture diagram, README, business requirements, ADRs, Terraform, application code, testing instructions, failure scenarios, security design, observability design.

### Suggested 16-week calendar

| Week | Focus |
|------|--------|
| 1 | Module 1 + Lab 1 |
| 2–7 | Modules 2–7 and matching AWS labs (Transfer Family off unless a live SFTP hour) |
| 8 | Modules 8–9 + Lab 8 |
| 9 | Module 10 |
| 10–13 | Modules 11–15 + Labs 11, 12, 13, 15 |
| 14–15 | Four capstones |
| 16 | Final assessment |

Self-paced learners follow the same order. See `GETTING_STARTED.md`.

---

## 8. Assessment and certificate

Do not make the final assessment purely multiple choice.

| Component | Requirement |
|-----------|-------------|
| Modules | All 15 required modules completed |
| Labs | All required labs (classification, AWS, chaos, security, observability, AI) |
| Architecture challenges | All 25 challenges with written rationale |
| Capstones | All four portfolio projects |
| Final assessment | Enterprise scenario design (inventory, patterns, diagram, security, resiliency, observability, AI boundaries, migration, ADRs) |

**Certificate title:**

# BayLearn Certificate of Completion

## Enterprise Integration Architecture

APIs • Messaging • Events • File Transfers • ESB • AI Agents

---

## 9. Lab design standard

Every lab follows:

1. Lab Overview  
2. Business Scenario  
3. Architecture  
4. Learning Objectives  
5. Prerequisites  
6. AWS Services Used  
7. Estimated Time  
8. Estimated AWS Cost  
9. Step 1 — Setup  
10. Step 2 — Infrastructure  
11. Step 3 — Application  
12. Step 4 — Integration  
13. Step 5 — Testing  
14. Step 6 — Failure Testing  
15. Step 7 — Observability  
16. Step 8 — Security Review  
17. Step 9 — Architecture Questions  
18. Step 10 — Cleanup (`terraform destroy`)

Automated validation prints **PASS** or **FAIL** with remediation.

Failure-first learning: wrong IAM, malformed events, duplicates, timeouts, throttling, backlogs, invalid schemas, unavailable dependencies.

---

## 10. Technologies

**Pattern first, then AWS.** Concepts are vendor-neutral.

**Core labs:** API Gateway, Lambda, S3, SQS, SNS, EventBridge, Step Functions, DynamoDB, Transfer Family, IAM, KMS, Secrets Manager, CloudWatch.

**Where useful:** ECS/Fargate, Cognito, CloudTrail.

**AI module:** governed tool-based agents (Bedrock optional; local simulator provided for cost control).

**IaC:** Terraform ≥ 1.5.

---

## 11. Cost controls (mandatory)

- Prefer serverless / free-tier-friendly components.
- Every lab states **Estimated AWS Cost**.
- Transfer Family is stopped or destroyed outside Lab 6 sessions.
- Terraform labs support `terraform destroy`.
- Avoid unnecessary persistent resources (NAT gateways, always-on EC2).

---

## 12. BayAreaLa8s positioning

BayLearn delivers **Enterprise Architecture Training + Integration Engineering + AWS Hands-On Labs + Real-World Capstones + Agentic AI**.

The student should finish able to answer:

> “How should these two enterprise systems integrate, and why?”

rather than merely:

> “How do I configure this AWS service?”

### Delivery modes

- Public cohort  
- Private corporate (NDA-friendly capstone briefs)  
- Workshop intensive (modules 1–7 compressed)  
- Train-the-trainer (enterprise contract)

### Related catalog

- Self-Serve Enterprise File Transfer on AWS  
- Production-Grade Microservices on AWS  
- AI Automation & Agents with AWS Bedrock  
- Terraform for Real Enterprises  
- Enterprise Architecture Leadership Masterclass  

---

## 13. Document version

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Status** | Ready for LMS, proposals, and BayLearn catalog |
| **Last updated** | 2026-08-18 |
| **Owner** | BayAreaLa8s / BayLearn Academy |
