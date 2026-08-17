# Week 1 — Assignment: Enterprise IaC Maturity Assessment

**Weight:** Part of 15% assignments grade · **Due:** End of Week 1 · **Length:** 2–3 pages or 800–1200 words

## Prompt

You are a consultant engaged by a company moving from manual AWS console changes to Terraform. They have:

- 3 AWS accounts (dev, staging, prod)
- 12 engineers with console admin access
- No remote state; Terraform used by one person locally
- No CI/CD for infrastructure

### Tasks

1. **Maturity assessment** — Rate the organization 1–5 on each pillar (define 1=ad hoc, 5=optimized):

   - State management
   - Repository structure & modules
   - CI/CD & peer review
   - Security & secrets
   - Operations (drift, rollback, monitoring)

2. **90-day roadmap** — Propose phased improvements aligned with this course’s 8 weeks. Each phase: goals, deliverables, risks.

3. **Tooling decision** — One page comparing Terraform vs CloudFormation **for this specific client**. Recommend a hybrid or single-tool approach with justification.

4. **Architecture diagram** — Include a diagram of proposed state backend layout (accounts, S3 buckets, state keys, locking).

## Rubric

| Criterion | Excellent (90–100%) | Proficient (75–89%) | Needs work (<75%) |
|-----------|----------------------|---------------------|-------------------|
| Maturity analysis | Specific gaps tied to risk | Generic gaps | Vague |
| Roadmap | Phased, realistic, maps to course | Some phases missing | Unrealistic or missing |
| Tool comparison | Nuanced, client-specific | Superficial | Incorrect facts |
| Diagram | Clear state boundaries | Minor gaps | Missing/wrong |

## Submission format

- PDF or Markdown in `docs/assignments/week-01-yourname.md`
- Diagram: Mermaid, draw.io, or PNG

## Academic integrity

Individual work unless cohort specifies team submission. Cite AWS/Terraform docs where applicable.
