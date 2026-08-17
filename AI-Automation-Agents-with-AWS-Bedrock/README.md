## AI Automation & Agents with AWS Bedrock

Professional course curriculum by **BayAreaLa8s**.

> Build production-grade AI automation systems, intelligent workflows, and enterprise AI agents on AWS.

**BayLearn:** https://baylearn.bayareala8s.com/courses/9d6c8974-eab4-45b3-aa0d-a058b9cda228/  
**Students:** start with [`STUDENT_START_HERE.md`](STUDENT_START_HERE.md)

## Overview

Modern enterprises are adopting AI to automate operations, improve decision-making, enhance productivity, and build intelligent internal platforms. This course focuses on **production-grade AI systems**—not chatbots—covering orchestration, governance, guardrails, observability, and real-world reliability patterns.

## Course facts

- **Duration**: 8 weeks (64–72 hours)
- **Format**: Instructor-led / Hybrid / Self-paced
- **Level**: Intermediate to Advanced
- **Audience**: Cloud/DevOps/Software/AI/Data/Platform Engineers, Solution Architects, advanced students

## Prerequisites

- Basic AWS knowledge
- Basic Python
- Familiarity with APIs and JSON
- General cloud services understanding
- Intro LLM knowledge helpful (not required)

## What students will be able to do

- Design enterprise-grade AI automation architectures
- Integrate AWS Bedrock into cloud workflows
- Build AI-powered APIs and automation systems
- Implement structured outputs and AI validation/guardrails
- Orchestrate AI workflows with Step Functions (retries, fallbacks, idempotency)
- Build enterprise AI agents with routing and memory patterns
- Operate AI systems reliably (observability, governance, cost controls)

## Real-world use cases

- **IT & Operations**: incident triage, intelligent ticket routing, operational assistants
- **Financial Services**: document classification, compliance summarization, workflow approvals
- **Healthcare**: ingestion workflows, intelligent document processing
- **Enterprise Productivity**: assistants, workflow automation, knowledge systems

## Reference architecture

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

## Tools & technologies

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

## Assessment (suggested weighting)

| Assessment           | Weight |
| -------------------- | ------ |
| Weekly Labs          | 35%    |
| Assignments          | 15%    |
| Architecture Reviews | 10%    |
| Final Capstone       | 30%    |
| Participation        | 10%    |

## Syllabus

See `SYLLABUS.md` for the full week-by-week outline, labs, deliverables, and capstone options.

## Weekly modules

For complete weekly course content (lecture notes, activities, labs, assignments, and quizzes), see `weeks/`.

## Hands-on labs (AWS)

Runnable lab code and deployment instructions: [`labs/README.md`](labs/README.md).

## Architecture diagrams

AWS stencil diagrams (Draw.io, PNG, SVG) for all weeks: [`diagrams/README.md`](diagrams/README.md).

Student-focused sequence flows, cheat sheets, and lab guides: [`diagrams/student/README.md`](diagrams/student/README.md).

## Marketing creatives

BayServe brand style (same as Terraform / Data Engineering / BayServe):

- [`docs/course-ai-automation-agents-bedrock-marketing.png`](docs/course-ai-automation-agents-bedrock-marketing.png) — 1920×1080 (course overview)
- [`docs/course-ai-automation-agents-bedrock-marketing-square.png`](docs/course-ai-automation-agents-bedrock-marketing-square.png) — 1080×1080 LinkedIn
- [`docs/course-ai-automation-agents-bedrock-personas.png`](docs/course-ai-automation-agents-bedrock-personas.png) — 1920×1080 (who benefits / career outcomes)
- [`docs/course-ai-automation-agents-bedrock-personas-square.png`](docs/course-ai-automation-agents-bedrock-personas-square.png) — 1080×1080 LinkedIn personas

Regenerate:
```bash
python3 scripts/generate-course-marketing.py
python3 scripts/generate-course-personas-marketing.py
```
(requires Pillow)

## Instructor & LMS resources

| Resource | Purpose |
|----------|---------|
| [`CAPSTONE_PROJECTS.md`](CAPSTONE_PROJECTS.md) | All 4 Capstone projects — status & how to run |
| [`STUDENT_START_HERE.md`](STUDENT_START_HERE.md) | Student onboarding |
| [`BAYLEARN_MODULE_MAP.md`](BAYLEARN_MODULE_MAP.md) | Week → file mapping for BayLearn uploads |
| [`INSTRUCTOR_QUIZ_ANSWERS.md`](INSTRUCTOR_QUIZ_ANSWERS.md) | Quiz answer keys (weeks 1–8) |
| [`COURSE_GUIDE.md`](COURSE_GUIDE.md) | Delivery guide |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | CI: pytest + SAM validate |

