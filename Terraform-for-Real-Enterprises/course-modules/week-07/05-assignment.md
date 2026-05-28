# Week 7 — Assignment: Governance Control Matrix

**Weight:** Part of 15% assignments grade · **Due:** End of Week 7 · **Length:** 3–4 pages or 1000–1500 words

## Prompt

You are designing **Terraform governance** for a 200-person engineering org moving to AWS Organizations with SCPs. Security requires evidence for an upcoming SOC2 audit.

### Tasks

1. **Control matrix** — Table mapping at least **8 controls** to implementations:

| Control objective | Terraform/platform implementation | Evidence artifact | Owner role |
|-------------------|-----------------------------------|-------------------|------------|

Include themes: IAM least privilege, secrets, tagging, static analysis, change management, state protection, drift, break-glass.

2. **IAM policy narrative** — Explain how your lab-hardened runner policy implements least privilege. Include one **intentional** permission that remains broad and why.

3. **Checkov exception process** — Define workflow for skipping a check: request, approval, ticket ID, expiry, re-scan. Give a realistic example finding (e.g. NAT instance vs managed NAT gateway cost tradeoff).

4. **Policy layering diagram** — Show how SCPs, IAM boundaries, Checkov, and module standards interact. When does Terraform fail vs AWS API deny?

## Rubric

| Criterion | Excellent (90–100%) | Proficient (75–89%) | Needs work (<75%) |
|-----------|----------------------|---------------------|-------------------|
| Control matrix | Specific, auditable evidence | Mostly complete | Vague controls |
| IAM narrative | Scoped actions, honest tradeoff | Superficial | Still admin-level |
| Exception process | Time-bound, accountable | Informal | Missing review |
| Layering diagram | Clear failure modes | Partial | Incorrect layering |

## Submission format

- PDF or Markdown: `docs/assignments/week-07-yourname.md`
- Attach `docs/security/week-07-validation-report.md` summary (or link)

## Academic integrity

Individual work. Do not paste proprietary employer policies verbatim—adapt and cite.
