# Enterprise Integration Architecture

**BayAreaLa8s · BayLearn Academy**

# Master APIs, Messaging, Events, File Transfers, ESB Modernization & AI-Agent Integration through Real-World Enterprise Architecture Labs.

| | |
|---|---|
| **Difficulty** | Advanced |
| **Duration** | 16 weeks · 90–120 hours |
| **Format** | Instructor-led, hybrid, or self-paced with labs |
| **Hands-on** | 12 labs · 25 architecture challenges · 4 capstones |
| **Stack** | AWS · Terraform · Python · AI Agents |
| **Certificate** | BayLearn Certificate of Completion |

This is **not** an AWS services tutorial.

The primary learning objective is to teach students how an Enterprise Architect decides **when and why** to use APIs, messaging, event-driven architecture, file transfer, ESB/integration platforms, or AI-agent-based integration.

> Do not start with an AWS service. Start with the integration requirement.

```text
Business Requirement
        ↓
Integration Characteristics
        ↓
Pattern
        ↓
Architecture
        ↓
Technology
        ↓
Implementation
        ↓
Failure Testing
        ↓
Operations
```

---

## Open the course

**Students start here:** [`GETTING_STARTED.md`](GETTING_STARTED.md)

```bash
python3 scripts/check_prereqs.py
python3 -m pip install -r requirements.txt
./scripts/start_course.sh
```

Then open [http://localhost:8080/course-ui/](http://localhost:8080/course-ui/) (use **Start** in the nav).

Do not open `course-ui/index.html` as a `file://` page — lessons will not load.

The player includes the landing page, getting started, dashboard, lessons, labs, architecture challenges, capstones, final assessment, progress tracking, and certificate.

## Repository layout

```text
enterprise-integration-architecture/
├── GETTING_STARTED.md        # Student day-one
├── COURSE.md                 # Master curriculum
├── modules/                  # 15 instructional modules
├── labs/                     # 12 lab workbooks
├── capstones/                # Banking, e-commerce, healthcare, manufacturing
├── terraform/                # Per-lab AWS infrastructure
├── lambda/                   # Application code for labs
├── diagrams/                 # Architecture diagrams (Mermaid)
├── sample-data/              # Files, events, and payloads
├── templates/                # ADR and portfolio templates
├── assessments/              # Challenges + final architecture assessment
├── course-ui/                # BayLearn landing page, dashboard, certificate
├── lms/                      # LMS import manifests
├── baylearn-seed/            # BayLearn Portal seed JSON
├── marketing/                # Academy listing copy
└── scripts/                  # Validate, deploy, destroy
```

## Syllabus

| Module | Topic | Lab |
|--------|-------|-----|
| 1 | [Enterprise Integration Fundamentals](modules/01-fundamentals/README.md) | Pattern classification |
| 2 | [API-Based Integration](modules/02-api-integration/README.md) | API Gateway → Lambda → DynamoDB |
| 3 | [Enterprise Messaging](modules/03-messaging/README.md) | SQS, DLQ, replay |
| 4 | [Pub/Sub Architecture](modules/04-pubsub/README.md) | SNS fan-out |
| 5 | [Event-Driven Architecture](modules/05-event-driven/README.md) | EventBridge choreography |
| 6 | [Enterprise File Transfer](modules/06-file-transfer/README.md) | Transfer Family → S3 pipeline |
| 7 | [Large File Architecture](modules/07-large-files/README.md) | Direct S3 upload + status API |
| 8 | [ESB & Traditional Integration](modules/08-esb/README.md) | Conceptual + decision lab |
| 9 | [ESB Modernization](modules/09-esb-modernization/README.md) | Strangler + ADR |
| 10 | [Enterprise Integration Patterns](modules/10-patterns/README.md) | Pattern catalog |
| 11 | [Reliability & Resiliency](modules/11-resiliency/README.md) | Chaos lab |
| 12 | [Security](modules/12-security/README.md) | Insecure architecture fix |
| 13 | [Observability](modules/13-observability/README.md) | Operations dashboard |
| 14 | [Architecture Decision Making](modules/14-architecture-decisions/README.md) | Three NFR challenges |
| 15 | [AI-Agent Integration](modules/15-ai-agents/README.md) | Operations agent + HITL |

**Capstones:** [Banking](capstones/banking/) · [E-Commerce](capstones/ecommerce/) · [Healthcare](capstones/healthcare/) · [Manufacturing](capstones/manufacturing/)

## Quick start for learners

Follow [`GETTING_STARTED.md`](GETTING_STARTED.md). Short version:

1. `python3 scripts/check_prereqs.py` then `./scripts/start_course.sh`
2. Complete Module 1 and Lab 1 (no AWS).
3. AWS labs: `./scripts/lab_up.sh lab-02-api` → `python3 scripts/validate_lab.py lab-02-api` → `./scripts/lab_down.sh lab-02-api`

Handbook: [`docs/STUDENT_HANDBOOK.md`](docs/STUDENT_HANDBOOK.md) · Instructors: [`docs/INSTRUCTOR_GUIDE.md`](docs/INSTRUCTOR_GUIDE.md)

## Cost control

Every AWS lab is serverless and designed to stay near free-tier when destroyed after use. Transfer Family (Lab 6) is the primary hourly cost — keep it **OFFLINE** or destroyed when not in a lab session.

```bash
./scripts/lab_down.sh lab-06-file-transfer
# or destroy everything
./scripts/destroy_all.sh --yes
```

Estimated lab costs are listed in each lab workbook.

## Alignment with BayAreaLa8s platforms

Curriculum is informed by production integration patterns used in **BayRelay** (file/event orchestration) and **BayServe** (self-serve control planes), plus governed agent access to enterprise tools. Labs remain vendor-neutral: the **pattern** is taught first, then an AWS implementation.

## Contact

- **Academy:** [academy@bayareala8s.com](mailto:academy@bayareala8s.com)
- **Enterprise workshops:** [training@bayareala8s.com](mailto:training@bayareala8s.com)
- **Web:** [bayareala8s.com](https://www.bayareala8s.com/)

Course materials © BayAreaLa8s. For instructor and authorized cohort use unless otherwise licensed.
