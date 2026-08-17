## AI Automation & Agents with AWS Bedrock — Course Guide

This document is the **instructor + operations guide** for delivering the course consistently across live, hybrid, and self-paced formats.

**BayLearn course:** https://baylearn.bayareala8s.com/courses/9d6c8974-eab4-45b3-aa0d-a058b9cda228/  
**LMS file map:** `BAYLEARN_MODULE_MAP.md` · **Student onboarding:** `STUDENT_START_HERE.md` · **Quiz keys:** `INSTRUCTOR_QUIZ_ANSWERS.md`

### Course positioning (what this is / isn’t)

- **This is**: enterprise AI automation engineering—workflow orchestration, guardrails, observability, governance, reliability, and cost control.
- **This is not**: a chatbot-only prompt engineering course.

### High-level architecture students build toward

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

## Delivery models

### Live cohort (recommended)

- **Cadence**: 2 sessions/week (approx. 4 hours each) or 1 longer session/week
- **Each week**:
  - Lecture + guided demo
  - Lab build (in-class start + take-home finish)
  - Short architecture review / show-and-tell
  - Assignment submission

### Hybrid

- Live “anchor session” weekly (90–120 min) + office hours
- Students complete labs async with check-ins and automated validation

### Self-paced

- Video modules mapped to the slide outline
- Labs with explicit acceptance criteria + reference outputs
- Weekly quizzes + rubrics for peer/self assessment

---

## Suggested pacing (64–72 hours total)

> Adjust by audience: engineers with strong AWS backgrounds typically move faster; students new to serverless may need more guided time in Weeks 2–5.

- **Lecture / demos**: 22–26 hours
- **Hands-on labs**: 28–32 hours
- **Assignments + writing**: 8–10 hours
- **Capstone**: 6–10 hours (spread across Weeks 6–8)

---

## Environment and setup (recommended baseline)

### AWS account approach

- Preferred: **one sandbox AWS account per student** (or per team) with budget guardrails.
- Alternative: shared account with strict IAM boundaries and naming conventions.

### Required AWS services

- Bedrock access enabled for at least one foundation model
- Lambda, Step Functions, API Gateway, EventBridge, DynamoDB, S3, CloudWatch, IAM

### Local tooling

- Python 3.10+ (3.11 recommended)
- AWS CLI (configured)
- Git + GitHub
- Optional: Docker, Terraform

### Repository conventions (recommended)

- `docs/` for diagrams, decision logs, and runbooks
- `infra/` for IaC (optional track)
- `services/` for Lambda + API code (if building a monorepo)
- `state-machines/` for Step Functions definitions

---

## Course policies (copy/paste friendly)

### AI usage policy

- Students may use AI tools for:
  - summarizing docs, generating scaffolds, debugging
  - brainstorming prompts and validation rules
- Students must still:
  - cite assumptions in design docs
  - demonstrate understanding during reviews
  - keep secrets out of prompts/logs

### Security and data handling

- **No secrets in repos** (AWS keys, tokens, `.env` files).
- Use **least privilege** IAM; prefer per-lab roles.
- Do not put regulated data into prompts or logs.

### Cost controls

- Enable budgets/alerts for the course account(s)
- Prefer small payloads, caching, and throttling
- Require cost estimates in Week 6+ deliverables

---

## Assessment operations

### Submission expectations (recommended)

Each week, students submit:

- **Code**: repo link or zip with run instructions
- **Architecture artifact**: diagram + short design notes
- **Evidence**: screenshots/log excerpts showing successful runs

### Grading consistency

- Use the rubrics in `ASSIGNMENTS_AND_RUBRICS.md`
- Require students to state:
  - inputs/outputs for each workflow
  - failure modes + fallback behavior
  - cost and security considerations

---

## Instructor run-of-show template (per session)

- **Warmup (5–10 min)**: recap + “what good looks like”
- **Lecture (25–40 min)**: concept + patterns + pitfalls
- **Demo (20–30 min)**: show the end-to-end “happy path”
- **Lab kickoff (40–60 min)**: students start with checkpoints
- **Break (5–10 min)**
- **Deepening (20–30 min)**: failure injection + observability
- **Close (10 min)**: what to submit, common mistakes, office hours

---

## Recommended artifacts students produce (portfolio-ready)

- State machine definitions (with retries, fallbacks, idempotency)
- A Bedrock-backed API service with structured outputs + validation
- Audit logs / dashboards for prompts, responses, cost, and failures
- A capstone with a clear business narrative + production concerns

