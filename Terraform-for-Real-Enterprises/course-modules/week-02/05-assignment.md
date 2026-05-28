# Week 2 — Assignment: Multi-Account Landing Zone Design Brief

**Weight:** Part of 15% assignments grade · **Due:** End of Week 2 · **Length:** 3–4 pages or 1000–1500 words

## Prompt

You are the lead platform engineer for a company adopting AWS Organizations. Current state:

- One AWS account with dev/test/prod separated by VPC and tags
- Week 1-style Terraform state in S3 (single account)
- No SCPs; IAM users with broad admin access
- Planned GitHub Actions Terraform pipeline (Week 4)

### Tasks

1. **Target architecture** — Propose OU hierarchy (Security, Infrastructure, Workloads minimum). Include Mermaid or diagram showing:
   - Management vs member accounts
   - Shared services (CI, DNS, logging)
   - Where Terraform state buckets live

2. **IAM model** — Describe cross-account roles for:
   - Human platform engineers (SSO)
   - CI OIDC role (shared services)
   - Per-environment `terraform-runner` roles

   Include trust policy **principles** (not full JSON required): ExternalId, `sub` conditions, least privilege.

3. **SCP recommendations** — List five SCP guardrails appropriate for this company. For each: intent, example API/action scope, and risk if omitted.

4. **Migration roadmap** — 6-month phased plan from single account to multi-account. Phases: account creation, state migration, SCP rollout, CI cutover. Include risks and rollback ideas.

5. **Terraform mapping table** — Columns: Stack name, Account, State S3 key, Runner role ARN pattern, Approval required (Y/N).

## Rubric

| Criterion | Excellent (90–100%) | Proficient (75–89%) | Needs work (<75%) |
|-----------|----------------------|---------------------|-------------------|
| OU / account design | Clear blast radius, realistic for company size | Mostly clear, minor gaps | Vague or single-account only without caveat |
| IAM / trust | Least privilege, OIDC-aware, ExternalId discussed | IAM described, gaps on CI | AdminAccess or root trust everywhere |
| SCPs | Specific, enforceable, tied to risk | Generic denies | Missing or incorrect (SCP grants access) |
| Migration | Phased, state called out, rollback | Some phases missing | Big-bang or unrealistic |
| Terraform table | Complete stacks mapped | Minor omissions | Missing |

## Submission format

- PDF or Markdown: `docs/assignments/week-02-yourname.md`
- Diagram: Mermaid embedded or PNG

## Academic integrity

Individual work unless cohort specifies pairs. Reference AWS Organizations and IAM documentation.
