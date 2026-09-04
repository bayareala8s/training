# BayLearn - Advanced Enterprise Java Engineering

## Complete Cursor Master Build Specification

**Version 1.0 | September 2026**

## 1. Product Vision

Build a production-grade advanced BayLearn course for experienced engineers. The learning philosophy is:

**BUILD -> MODERNIZE -> DEPLOY -> BREAK -> DIAGNOSE -> OPERATE -> ARCHITECT -> DEFEND**

The course uses a single fictional enterprise case study, **BayPay Financial Services**, and an evolving reference platform, **BayPay Enterprise Payment Platform**, so students gain continuity rather than completing disconnected tutorials.

## 2. Positioning

**Course title:** Advanced Enterprise Java Engineering  
**Subtitle:** From Legacy Java to Cloud-Native Production Platforms  
**Level:** Advanced / Professional  
**Primary domains:** Java, Spring Boot, JVM, WebSphere ND, Liberty, Containers, OpenShift, Kubernetes, AWS, Terraform, Ansible, CI/CD, Production Engineering, AI-assisted operations, Technical Interviews.

**Audience:** Java Engineers, Senior Software Engineers, Platform/DevOps/Cloud Engineers, Technical Leads, Staff Engineers, Principal Engineer candidates and architects seeking deeper Java-platform knowledge.

**Prerequisites:** Working Java knowledge, Git, basic Linux, REST/API fundamentals and basic cloud concepts.

## 3. Course Targets

- 16 modules
- Approximately 50 hands-on labs
- 4 major capstones
- 100 advanced interview questions
- Approximately 70 professional diagrams
- Reusable BayPay reference application
- Progressive production-incident simulator
- BayOps AI teaching prototype
- Student portfolio artifacts
- Instructor/reference solutions
- BayLearn-native progress, quiz and certificate integration

## 4. Core Case Study - BayPay Financial Services

BayPay is fictional. It operates a mission-critical enterprise payment platform with legacy Java application-server workloads, messaging, relational data, external integrations and modernization pressure.

Initial conceptual state:

```text
Customers -> Load Balancer -> WebSphere ND Cluster
                              |-> Payment Application
                              |-> Refund Application
                              -> Enterprise Messaging -> Database -> Reporting
```

The platform progressively moves toward Liberty, containers, OpenShift/Kubernetes, AWS container services, infrastructure as code, observability, HA/DR and AI-assisted operations.

## 5. BayPay Reference Application

Create `/reference-apps/baypay/` using Java 21 where practical, Spring Boot, Maven, REST, JPA, H2 for local development, PostgreSQL-compatible production configuration, Actuator, Bean Validation, JUnit, Testcontainers where useful, OpenAPI and structured logging.

Suggested components:
- payment-service
- refund-service
- notification-service
- transaction-worker
- shared

Core entities:
- Customer
- Account
- Payment
- Refund
- Transaction
- TransactionEvent
- AuditEvent

Payment state model:
`RECEIVED -> VALIDATING -> AUTHORIZED -> PROCESSING -> COMPLETED`, with failure/reversal paths.

Implement idempotency as a real requirement. Do not create unnecessary microservices merely to make the architecture look sophisticated. Explicitly teach when a modular monolith is preferable.

## Module 1 - Enterprise Java Engineering

### Required lesson coverage
- Modern Java/JDK/JVM overview
- Object design, SOLID and immutability
- Collections and generics
- Exceptions, records, streams and Optional
- Enterprise coding practices

### Required labs
- BUILD-101 Build BayPay transaction domain model
- BUILD-102 Implement payment validation
- FIX-103 Refactor deliberately poor Java code
- CHALLENGE-104 Optimize transaction processing

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 2 - Advanced Java Concurrency

### Required lesson coverage
- Threads and Java memory visibility
- synchronized, volatile, locks and atomics
- Concurrent collections
- Executors and CompletableFuture
- Virtual threads
- Race conditions and deadlocks

### Required labs
- BREAKFIX-201 Duplicate Payment Incident
- INCIDENT-202 Deadlocked Payment Workers
- ARCHITECT-203 Safe concurrent payment processing

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 3 - Spring Boot Engineering

### Required lesson coverage
- IoC and dependency injection
- REST APIs and validation
- Exception handling and configuration
- JPA and transaction management
- Actuator and production health
- Testing

### Required labs
- BUILD-301 Payment REST API
- BUILD-302 Refund API
- BUILD-303 Persistence
- FIX-304 Transaction rollback bug
- BUILD-305 Health/readiness endpoints

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 4 - Jakarta EE and Enterprise Runtime Concepts

### Required lesson coverage
- Servlet/Jakarta EE model
- JPA, JTA, JMS and JNDI
- DataSources and connection pools
- Sessions and class loading
- Application server fundamentals

### Required labs
- ARCHITECT-401 Map Spring to Jakarta concepts
- INCIDENT-402 Connection pool exhaustion
- INCIDENT-403 Transaction boundary failure

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 5 - WebSphere Network Deployment

### Required lesson coverage
- Cell, DMGR, node, node agent and server
- Clusters and deployments
- JDBC/JNDI/JMS
- JVM configuration and pools
- Security, SSL and sessions
- Operations and troubleshooting

### Required labs
- ARCHITECT-501 Design WebSphere ND BayPay
- INCIDENT-502 Cluster members stop processing
- INCIDENT-503 JDBC pool exhaustion
- INCIDENT-504 Deployment failure

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 6 - WebSphere Liberty Modernization

### Required lesson coverage
- Traditional WebSphere vs Liberty
- Liberty features and server.xml
- Compatibility assessment
- Configuration externalization
- Migration strategy and rollback

### Required labs
- MODERNIZE-601 WebSphere-to-Liberty assessment
- MODERNIZE-602 Adapt BayPay for Liberty
- MODERNIZE-603 Externalize configuration
- ARCHITECT-604 Migration waves and rollback

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 7 - JVM Internals and Performance

### Required lesson coverage
- Heap, stacks, metaspace and native memory
- Class loading
- JIT compilation
- Garbage collection
- Allocation behavior
- JVM in containers

### Required labs
- LAB-701 Observe JVM memory
- LAB-702 Controlled object allocation
- LAB-703 Observe GC
- LAB-704 JVM/container memory experiment

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 8 - JVM Troubleshooting

### Required lesson coverage
- Thread-dump analysis
- Heap-dump reasoning
- CPU saturation
- Memory leaks
- GC pauses
- Thread starvation
- Container OOM

### Required labs
- INCIDENT-801 CPU 98 percent
- INCIDENT-802 Memory leak
- INCIDENT-803 Deadlock
- INCIDENT-804 Thread-pool exhaustion
- INCIDENT-805 Excessive GC
- INCIDENT-806 Container OOM

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 9 - Containers for Java

### Required lesson coverage
- OCI/container concepts
- Docker and Podman
- Images and registries
- Networking and volumes
- Secrets and configuration
- Java resource sizing
- Container security

### Required labs
- BUILD-901 Containerize BayPay
- FIX-902 Repair poor Dockerfile
- SECURITY-903 Harden container
- PERFORMANCE-904 Optimize Java container

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 10 - Kubernetes and OpenShift

### Required lesson coverage
- Pods, deployments and ReplicaSets
- Services, ingress and OpenShift Routes
- ConfigMaps and Secrets
- RBAC and networking
- Probes and resources
- Autoscaling and rollout/rollback

### Required labs
- INCIDENT-1001 CrashLoopBackOff
- INCIDENT-1002 OOMKilled
- INCIDENT-1003 Readiness failure
- INCIDENT-1004 Bad Secret
- INCIDENT-1005 TLS/certificate issue
- INCIDENT-1006 Service routing failure

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 11 - AWS Container Platforms

### Required lesson coverage
- ECR
- ECS and Fargate
- EKS
- ALB/NLB and Route 53
- IAM, Secrets Manager and KMS
- CloudWatch
- RDS/S3
- Autoscaling and cost

### Required labs
- BUILD-1101 Deploy BayPay on ECS/Fargate
- ARCHITECT-1102 ECS vs EKS vs OpenShift
- SECURITY-1103 IAM, secrets and KMS
- INCIDENT-1104 Unhealthy ALB target
- COST-1105 Cost optimization

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 12 - Terraform, Ansible and CI/CD

### Required lesson coverage
- Git workflow
- CI build/test
- Container publishing
- Terraform foundations and modules
- Configuration automation
- Deployment validation and rollback

### Required labs
- BUILD-1201 Terraform AWS environment
- BUILD-1202 Reusable Terraform modules
- BUILD-1203 Configuration automation
- BUILD-1204 CI/CD pipeline
- INCIDENT-1205 Failed deployment and rollback

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 13 - Production Engineering and Observability

### Required lesson coverage
- Logs, metrics and traces
- RED/USE concepts
- SLIs and SLOs
- Alerting and dashboards
- Capacity planning
- Incident response and RCA
- Change management

### Required labs
- BUILD-1300 BayPay operations dashboard
- INCIDENT-1301 Throughput collapse and P99 latency spike

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 14 - Security, High Availability and Disaster Recovery

### Required lesson coverage
- TLS and PKI
- IAM and secrets
- Encryption
- Networking/DNS/load balancing
- HA and failure domains
- RTO/RPO and DR
- Capacity planning

### Required labs
- ARCHITECT-1401 Design BayPay for 99.99 percent
- INCIDENT-1402 Certificate expiration
- DR-1403 Regional outage tabletop
- SECURITY-1404 Threat model BayPay

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 15 - BayOps AI - AI-Assisted Operations

### Required lesson coverage
- Incident summarization
- Evidence vs hypothesis
- RCA hypothesis generation
- Runbook recommendations
- Human approval
- AI evaluation and hallucination detection

### Required labs
- AI-1501 Incident summarization
- AI-1502 RCA hypotheses
- AI-1503 Runbook recommendation
- AI-1504 Evaluate hallucinated diagnosis

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## Module 16 - Advanced Engineer Interview Simulator

### Required lesson coverage
- Java/JVM round
- Spring/Jakarta round
- WebSphere/Liberty round
- Containers/Kubernetes round
- AWS round
- Automation round
- Production incident round
- System design round
- Leadership/architecture round

### Required labs
- INTERVIEW-1601 Practice mode
- INTERVIEW-1602 Rapid fire
- INTERVIEW-1603 Troubleshooting interview
- INTERVIEW-1604 System design
- INTERVIEW-1605 Full mock loop

### Required module assets
- Module overview and business context
- Learning objectives and prerequisites
- Detailed lesson content
- Professional diagrams and alt text
- Code/configuration examples
- Production failure modes and trade-offs
- Interview perspective
- Knowledge checks
- Module quiz with answer explanations
- Lab student guide
- Instructor/reference solution
- Rubric
- Student portfolio artifact
- Related PAKS deep-dive links where appropriate


## 22. Four Major Capstones
### Capstone 1 - Build BayPay
Build a production-quality Java/Spring Boot payment service with API, persistence, tests, validation, error handling and observability.

### Capstone 2 - Modernize BayPay
Assess a fictional legacy WebSphere ND deployment, migrate toward Liberty and containers, and design OpenShift/Kubernetes deployment with test and rollback strategy.

### Capstone 3 - Cloud BayPay
Deploy/design the platform on AWS with containers, Terraform, security, monitoring, scaling, resilience, cost analysis and cleanup.

### Capstone 4 - BayPay Production Crisis
Handle a progressive SEV-1 simulation: triage, stabilize, diagnose, communicate, remediate, recover, write RCA and propose prevention.


## 23. Lab Taxonomy and UX

Every lab must use one of these reusable types:

`BUILD`, `ARCHITECT`, `MODERNIZE`, `BREAK/FIX`, `INCIDENT`, `SECURITY`, `PERFORMANCE`, `COST`, `AI`, `INTERVIEW`, `CAPSTONE`.

Every lab page must include:
1. Scenario
2. Business context
3. Learning objectives
4. Architecture
5. Prerequisites
6. Environment setup
7. Challenge/tasks
8. Validation
9. Troubleshooting
10. Expected outcome
11. Interview questions
12. Architecture/trade-off questions
13. Cleanup
14. Cost estimate where relevant
15. Hidden/revealable solution
16. What you learned
17. Portfolio deliverable

Challenge and incident labs must not reveal the answer upfront.

## 24. Incident Simulator

Implement a reusable BayLearn incident experience. Students receive an incident timeline and progressively request evidence such as dashboards, logs, thread dumps, deployment history, JVM/container metrics, database metrics, queue depth and dependency latency.

The student records:
- current hypothesis
- supporting evidence
- next investigation
- stabilization action
- remediation
- communication update

Do not expose all evidence immediately. Optionally score diagnostic efficiency.

Standard scoring:
- Technical accuracy: 25%
- Diagnostic method: 20%
- Production awareness: 15%
- Trade-off analysis: 15%
- Security/reliability: 10%
- Communication: 10%
- Efficiency: 5%

A lucky root-cause guess must not receive the same score as disciplined evidence-based diagnosis.

## 25. Interview Bank and Simulator

Create exactly 100 high-quality advanced questions:
- Java/JVM: 20
- Spring/Jakarta: 10
- WebSphere/Liberty: 15
- Containers/Kubernetes/OpenShift: 15
- AWS: 10
- Automation: 8
- Linux/Networking/TLS: 7
- Production Engineering: 7
- HA/Security: 4
- Leadership/Architecture: 4

Each question record must include:
`id`, `domain`, `difficulty`, `question`, `followUps`, `expectedConcepts`, `seniorAnswer`, `staffAnswer`, `principalAnswer`, `commonMistakes`, `scoreRubric`.

Simulator modes:
- Practice
- Timed Interview
- Rapid Fire
- Troubleshooting
- System Design
- Full Mock Loop

Answer maturity must differentiate Engineer, Senior, Staff and Principal reasoning rather than presenting one memorized answer.

## 26. BayOps AI

Build a teaching prototype using synthetic/sanitized operational data only. It may use Amazon Bedrock, Lambda, S3, DynamoDB, API Gateway and CloudWatch.

Outputs must explicitly separate:
- Evidence
- Hypotheses
- Recommended investigation
- Suggested remediation

Never present an AI-generated root cause as proven without supporting evidence. Include a lab where students identify and correct an AI hallucination or unsupported diagnosis.

## 27. Diagram Generation Standard

Target approximately 70 diagrams across the course.

Diagram types:
- concept
- component
- deployment
- sequence
- request/data flow
- security/trust boundary
- network
- current-state/target-state
- modernization
- incident
- troubleshooting decision tree
- executive view

For AWS architecture diagrams, use current official AWS Architecture Icons where supported by the asset pipeline. Do not replace AWS services with generic icons when an official icon is available. For non-AWS vendor products, use licensed/approved marks only when permitted; otherwise use clean labeled components.

Every diagram must have:
- diagram ID
- title
- module/lesson mapping
- learning purpose
- complexity level
- editable source
- SVG
- PNG
- alt text

Use progressive complexity:
1. Concept
2. Application
3. Production
4. Enterprise

Keep text readable, flows directional, lines uncrossed where practical, boundaries explicit and diagrams presentation-quality.

## 28. AWS Lab Standards

Every AWS lab must include:
- architecture diagram
- service list
- region assumptions
- prerequisites
- least-privilege/security notes
- estimated duration
- estimated cost and cost-warning
- IaC where appropriate
- validation
- failure scenario
- troubleshooting
- cleanup
- expected final state

Prefer low-cost/serverless or short-lived resources. Avoid unnecessary NAT Gateways, EKS clusters, always-on EC2, OpenSearch and other expensive infrastructure unless the learning objective specifically requires them and the cost is clearly disclosed.

Tag resources consistently with Course, Module, Lab, Environment and Expiration metadata.

## 29. Content Standard for Every Lesson

Each lesson must contain:
1. Why this matters
2. Learning objectives
3. Concept explanation
4. Visual explanation
5. Architecture
6. Production example
7. Code/configuration example
8. Trade-offs
9. Failure modes
10. Security/reliability implications
11. Interview perspective
12. Key takeaways
13. Knowledge check
14. Related lab
15. Related PAKS deep dive

PAKS is supplemental; the BayLearn lesson must remain understandable on its own.

## 30. Student Portfolio

Persist or export portfolio-ready artifacts from major labs/capstones, including:
- Java service
- concurrency RCA
- WebSphere architecture
- Liberty migration assessment
- JVM incident RCA
- container architecture
- Kubernetes/OpenShift deployment
- AWS architecture
- Terraform
- CI/CD design
- security model
- DR strategy
- production RCA
- AI-operations evaluation
- system-design response

Completion should demonstrate end-to-end enterprise Java modernization capability, not merely video consumption.

## 31. Required Repository Structure

```text
advanced-enterprise-java-engineering/
├── README.md
├── COURSE_MASTER_SPEC.md
├── COURSE_IMPLEMENTATION_PLAN.md
├── COURSE_MANIFEST.json
├── BAYLEARN_INTEGRATION_MAP.md
├── course/
│   ├── metadata/
│   ├── modules/
│   ├── lessons/
│   ├── quizzes/
│   └── assessments/
├── reference-apps/
│   └── baypay/
│       ├── payment-service/
│       ├── refund-service/
│       ├── notification-service/
│       ├── transaction-worker/
│       └── shared/
├── labs/
├── incidents/
│   ├── jvm/
│   ├── kubernetes/
│   ├── aws/
│   └── production/
├── capstones/
├── interview-bank/
├── diagrams/
│   ├── java/
│   ├── spring/
│   ├── websphere/
│   ├── liberty/
│   ├── jvm/
│   ├── containers/
│   ├── kubernetes/
│   ├── openshift/
│   ├── aws/
│   ├── devops/
│   ├── observability/
│   ├── security/
│   ├── ai/
│   └── capstones/
├── infrastructure/
│   ├── terraform/
│   ├── kubernetes/
│   ├── openshift/
│   └── scripts/
├── instructor/
├── student/
├── datasets/
├── solutions/
├── baylearn-seed/
└── qa/
```

## 32. BayLearn Integration Requirements

Cursor must inspect the existing BayLearn repository before implementing. Reuse existing:
- data models
- routing
- authentication
- catalog cards
- progress tracking
- lesson layouts
- lab components
- quiz engine
- certificate logic
- content/seed loaders
- design tokens
- AWS lab patterns

Add new platform capabilities only where the course genuinely requires them, especially:
- labType metadata/badges
- progressive incident simulator
- interview simulator
- portfolio artifact tracking

Any shared change must be backward-compatible with existing BayLearn courses.

## 33. QA and Definition of Done

Automate checks for:
- missing modules/lessons/labs
- broken links
- invalid JSON
- missing solutions/rubrics
- AWS labs without cleanup or cost disclosure
- diagrams without alt text
- duplicate interview questions
- Java code that does not compile
- failing tests
- invalid Terraform
- invalid Kubernetes YAML where validation is available
- missing prerequisites
- placeholder/TODO content
- unsupported factual claims
- accidental use of real confidential enterprise data

Generate `COURSE_QA_REPORT.md`.

The course is complete only when all 16 modules, approximately 50 labs, 4 capstones, 100 interview questions, diagram library, incident simulator, interview simulator, reference application, seed data, instructor assets, student assets and QA checks are implemented and integrated without breaking existing courses.

## 34. Cursor Execution Plan

**Stage 1 - Inspect and plan:** Create `COURSE_IMPLEMENTATION_PLAN.md`, `COURSE_MANIFEST.json`, `BAYLEARN_INTEGRATION_MAP.md`; stop for review.

**Stage 2 - BayPay:** Build and test reference application; stop.

**Stage 3 - Modules 1-4:** Content, code, labs, quizzes, diagrams; QA; stop.

**Stage 4 - Modules 5-6:** WebSphere/Liberty modernization assets and simulations; QA; stop.

**Stage 5 - Modules 7-8:** JVM internals/troubleshooting and incident datasets; QA; stop.

**Stage 6 - Modules 9-10:** Containers/Kubernetes/OpenShift; QA; stop.

**Stage 7 - Modules 11-12:** AWS and automation; Terraform validation; QA; stop.

**Stage 8 - Modules 13-14:** Production engineering, security, HA/DR; QA; stop.

**Stage 9 - Module 15:** BayOps AI; evaluation and safety checks; QA; stop.

**Stage 10 - Module 16:** 100-question bank and interview simulator; QA; stop.

**Stage 11 - Capstones:** Build all four; QA.

**Stage 12 - Diagram library:** Generate/export/validate all required diagrams.

**Stage 13 - PAKS integration:** Add curated deep-dive links without making them required for course comprehension.

**Stage 14 - Final validation:** Run full test/build/QA suite and produce final manifest and report.

## 35. Initial Cursor Prompt

```text
Read COURSE_MASTER_SPEC.md completely.

We are adding "Advanced Enterprise Java Engineering" to the existing BayLearn platform.

Do NOT implement immediately.

First inspect the complete BayLearn repository and identify:
- course/module/lesson schemas
- labs and validation
- quizzes and assessments
- progress tracking
- authentication/authorization
- course catalog and routing
- styling/design system
- diagrams
- certificates
- seed/import mechanisms
- AWS lab patterns
- reusable UI components

Then create:
1. COURSE_IMPLEMENTATION_PLAN.md
2. COURSE_MANIFEST.json
3. BAYLEARN_INTEGRATION_MAP.md

COURSE_IMPLEMENTATION_PLAN.md must map every requirement from this specification to the existing BayLearn implementation.

COURSE_MANIFEST.json must enumerate all 16 modules, lessons, approximately 50 labs, 4 capstones, approximately 70 diagrams, 100 interview questions, code components, incident datasets, quizzes and assessments.

BAYLEARN_INTEGRATION_MAP.md must document exactly which existing BayLearn components, routes, schemas and services will be reused and which new capabilities are required.

Constraints:
- Do not redesign BayLearn unnecessarily.
- Do not break existing courses.
- Prefer reuse over duplicate infrastructure.
- Clearly document technical risks and assumptions.
- Keep all fictional enterprise data synthetic.
- Stop after these three artifacts and provide a concise implementation summary for review.
```

## 36. Guardrails

- All BayPay and incident data must be fictional/synthetic.
- Do not reproduce confidential employer architectures, runbooks, logs or internal procedures.
- Do not claim affiliation with a real employer based on course inspiration.
- Avoid teaching obsolete approaches as recommended current practice; historical technology may be taught for modernization context.
- Explain trade-offs instead of declaring one universal architecture.
- Keep cloud cost and cleanup visible.
- Keep security, reliability and operability present in technical designs.
- Prefer evidence-based troubleshooting.
- Never make AI the final authority for production RCA.
- Keep reference solutions separate from student-facing challenge material.
