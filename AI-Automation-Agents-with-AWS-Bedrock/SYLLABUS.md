## AI Automation & Agents with AWS Bedrock

### Course overview

**Title**: AI Automation & Agents with AWS Bedrock  
**Provider**: BayAreaLa8s  
**Tagline**: Build production-grade AI automation systems, intelligent workflows, and enterprise AI agents on AWS  
**Duration**: 8 weeks (64–72 hours)  
**Difficulty**: Intermediate to Advanced  
**Format**: Instructor-led / Hybrid / Self-paced

### Target audience

- Cloud Engineers
- DevOps Engineers
- Software Engineers
- AI Engineers
- Data Engineers
- Platform Engineers
- Solution Architects
- Senior students pursuing AI & Cloud careers

### Prerequisites

- Basic AWS knowledge
- Basic Python programming
- Familiarity with APIs and JSON
- Understanding of cloud services
- Introductory understanding of AI/LLMs (helpful but not mandatory)

### Course description

This course teaches students to design and build **production-grade AI automation systems** on AWS using:

- AWS Bedrock
- Step Functions
- Lambda
- EventBridge
- API Gateway
- DynamoDB
- Amazon S3
- CloudWatch

Students learn structured outputs, validation and guardrails, orchestration patterns (retries/backoff/idempotency), governance and audit logging, cost controls, and agentic systems (routing/memory/workflow chaining).

### Learning outcomes

By the end of the course, students can:

- Design enterprise-grade AI automation architectures
- Integrate Bedrock into workflows and APIs securely
- Build structured AI decision engines with validation and deterministic fallbacks
- Orchestrate workflows with Step Functions (retries, backoff, failure handling, idempotency)
- Implement governance, audit trails, and observability for AI systems
- Build enterprise AI agents with memory, routing, and event-driven chaining
- Operate scalable, production-ready AI platforms

### Reference architecture (concept)

```text
Event / API Request
        |
API Gateway / EventBridge
        |
Step Functions (Orchestration)
        |
AWS Bedrock (Claude / Titan)
        |
Lambda (Validation & Actions)
        |
DynamoDB / S3
        |
CloudWatch / Audit / Alerts
```

---

## Week-by-week syllabus

> For complete weekly modules (objectives, lecture notes, activities, labs, assignments, quizzes), see the `weeks/` folder.
>
> Architecture diagrams (Draw.io / PNG / SVG): see [`diagrams/README.md`](diagrams/README.md).

### Week 1 — Enterprise AI Foundations

**Topics**

- Enterprise AI architecture overview
- LLMs vs ML vs rules engines
- Where AI fits in enterprises
- Risks: hallucinations, cost, leakage
- AWS Bedrock introduction

**Hands-on labs**

- First Bedrock model invocation
- Compare AI model outputs
- Analyze latency and cost

**Deliverables**

- AI workflow architecture diagram
- Bedrock invocation examples
- AI usage analysis report

---

### Week 2 — AWS Bedrock Deep Dive

**Topics**

- Foundation models in Bedrock
- Claude, Titan, and model selection
- Prompt templates and versioning
- IAM and Bedrock security
- Private networking concepts

**Hands-on labs**

- Secure Bedrock integration
- Prompt evaluation framework
- Version-controlled prompts

**Deliverables**

- Secure Bedrock architecture
- Prompt evaluation results
- IAM access design

---

### Week 3 — AI Decision Engines & Structured Outputs

**Topics**

- Structured JSON outputs
- AI routing decisions
- Confidence scoring
- Deterministic fallbacks
- Hybrid AI + rules systems

**Hands-on labs**

- AI classification engine
- AI-based routing system
- Structured JSON response validation

**Deliverables**

- AI decision engine
- Validation workflow
- Classification API

---

### Week 4 — Orchestrating AI with Step Functions

**Topics**

- Step Functions architecture
- AI workflow orchestration
- Retry and backoff strategies
- Idempotency patterns
- Failure handling

**Hands-on labs**

- Build AI orchestration workflows
- Multi-step AI automation pipelines
- Failure simulation testing

**Deliverables**

- AI orchestration workflow
- State machine definitions
- Retry automation reports

---

### Week 5 — AI Automation APIs

**Topics**

- API Gateway + Lambda + Bedrock
- AI API security
- Rate limiting and throttling
- Cost-aware API design
- AI microservice patterns

**Hands-on labs**

- Build AI APIs:
  - `/classify`
  - `/summarize`
  - `/route`
- Secure AI endpoints

**Deliverables**

- AI API platform
- API documentation
- Secure endpoint workflows

---

### Week 6 — Observability, Governance & AI Safety

**Topics**

- Prompt/response logging
- Audit trails
- AI monitoring
- Cost tracking
- Human-in-the-loop systems
- Governance and compliance

**Hands-on labs**

- CloudWatch dashboards
- AI audit pipeline
- Cost monitoring system

**Deliverables**

- AI observability dashboards
- Governance workflow
- AI operations report

---

### Week 7 — Enterprise AI Agent Systems

**Topics**

- AI agent architecture
- Agent memory and context
- Multi-agent workflows
- Event-driven AI automation
- AI workflow chaining

**Hands-on labs**

- Build AI operational assistant
- Create workflow routing agents
- Implement AI memory patterns

**Deliverables**

- AI agent workflow
- Agent orchestration diagrams
- Multi-step automation system

---

### Week 8 — Capstone Project

**Capstone options**

1. **AI Operations Assistant**: AI-driven operational incident assistant
2. **AI File Automation Platform**: intelligent ingestion and routing workflows
3. **Enterprise AI Workflow Engine**: internal AI orchestration platform
4. **Internal AI API Platform**: reusable AI APIs and governance systems

**Capstone deliverables**

- AI architecture diagrams
- Source code repositories
- Workflow automation pipelines
- Cost and risk analysis
- Governance review
- Final demo presentation

---

## Tools & technologies covered

### AWS services

- AWS Bedrock
- AWS Lambda
- AWS Step Functions
- Amazon API Gateway
- Amazon EventBridge
- Amazon DynamoDB
- Amazon S3
- Amazon CloudWatch
- IAM

### Development tools

- Python
- JSON
- GitHub
- Docker (optional)
- AWS CLI
- Terraform (optional IaC track)

## Career outcomes (examples)

Roles this course supports:

- AI Engineer
- Cloud AI Engineer
- AI Platform Engineer
- Machine Learning Engineer
- DevOps + AI Engineer
- Solutions Architect
- AI Automation Engineer
- Platform Automation Engineer

Resume bullet example:

> Designed and implemented enterprise-grade AI automation workflows using AWS Bedrock, Step Functions, Lambda, and API Gateway with structured AI outputs, workflow orchestration, governance, and observability.

