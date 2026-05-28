## Week 2 — AWS Bedrock Deep Dive

This week turns “first model calls” into **secure, evaluable, repeatable** integrations suitable for production workflows.

### Learning objectives

By the end of Week 2, students can:

- Select an appropriate Bedrock model for a workload with constraints
- Build a least-privilege IAM design for Bedrock invocation from Lambda
- Implement prompt templates with versioning and evaluation against a golden set
- Explain how networking choices can affect secure deployments (conceptually)

### Core concepts (lecture notes)

- **Model selection**
  - Choose based on: task type (classify/summarize/route), latency needs, cost sensitivity, context length needs, output reliability requirements.
- **Prompt templates**
  - Standardize prompts for reuse (task, constraints, output schema, examples, refusal rules).
  - Version prompts; treat changes like code changes (review and evaluation).
- **Evaluation harness**
  - Golden set: representative inputs + expected outputs or acceptance criteria.
  - Score: pass/fail and a few quality dimensions (consistency, format correctness).
  - Compare prompt versions before promoting.
- **Security and IAM**
  - Least privilege for invocations (role-based access for Lambda/Step Functions).
  - Separate roles for build/deploy/runtime where possible.
  - Log metadata, not sensitive content.
- **Private networking (concepts)**
  - When you place functions in VPCs, watch for egress/endpoint considerations.
  - Treat networking as part of your threat model and audit posture.

### In-class activities (45–60 min)

- **Activity A — Model decision memo**
  - Pick one use case and write a 1-page memo: model choice, latency target, cost controls, expected volume.
- **Activity B — IAM threat modeling**
  - Identify what could go wrong with overly broad permissions and how to constrain.

### Demos (instructor-led)

- **Demo 1**: Lambda → Bedrock invocation with correlation ID logging.
- **Demo 2**: Prompt version A vs B evaluated on a small golden set.

### Hands-on labs (students)

Complete:

- `LABS_GUIDE.md` → **Week 2 Labs**: Lab 2.1 and Lab 2.2
- Runnable code: `labs/week02/` + deploy stack in `labs/README.md`

### Assignment (due end of week)

Submit:

- **Secure invocation proof**
  - Lambda role policy (or policy outline) demonstrating least privilege
  - evidence of successful invocations
- **Prompt evaluation report**
  - golden set definition (10–20 cases)
  - results table and recommendation
- **Secure Bedrock architecture note**
  - diagram + short explanation of logging/redaction boundaries

Rubric:

- See `ASSIGNMENTS_AND_RUBRICS.md` → **Week 2**

### Quiz (5–10 questions)

1. What are three criteria you would use to choose a model for classification?
2. Why should prompts be versioned and evaluated like code?
3. What is a “golden set” and why is it useful?
4. What does “least privilege” mean in an IAM design for Bedrock invocations?
5. Why is logging raw prompts/responses risky in enterprise environments?

### Architecture diagram

- [`diagrams/drawio/03-week02.drawio`](../diagrams/drawio/03-week02.drawio) · [PNG](../diagrams/png/03-week02.png) · [SVG](../diagrams/svg/03-week02.svg)

Also see IAM boundary diagram: [`10-iam`](../diagrams/png/10-iam.png)

### Expected artifacts (portfolio-ready)
- Prompt evaluation harness + decision note

