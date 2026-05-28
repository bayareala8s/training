# Week 4 — Assignment: Terraform CI/CD Pipeline Design Document

**Weight:** Part of 15% assignments grade · **Due:** End of Week 4 · **Length:** 3–4 pages or 1000–1500 words + diagram

## Prompt

Design the **target** CI/CD pipeline for a company running Terraform across three AWS accounts (dev, test, prod) with GitHub Enterprise. Current state: engineers run apply locally; no scanners; static AWS keys in one repo.

### Tasks

1. **Pipeline diagram** — Mermaid or equivalent showing:
   - PR triggers (path filters)
   - Jobs: fmt, validate, tflint, checkov, plan
   - Merge to main → apply with environments
   - OIDC auth flow (no access keys in diagram)

2. **Role model** — Table: Role name, Account, Trust principal, Can plan?, Can apply?, Notes

3. **GitHub Environments** — Protection rules for `dev` vs `prod` (reviewers, branch limits, secrets).

4. **Security scanning policy** — When to hard-fail vs soft-fail; exception process; example finding and handling.

5. **Failure runbook** — Three common CI failures (OIDC, state lock, SCP deny) with diagnostic steps and owner role.

6. **Migration plan** — 90-day rollout from local apply to full GitOps; include Week 2 cross-account roles and Week 3 module pins.

## Rubric

| Criterion | Excellent (90–100%) | Proficient (75–89%) | Needs work (<75%) |
|-----------|----------------------|---------------------|-------------------|
| Diagram | Complete, OIDC, plan/apply split | Minor gaps | Missing apply gate or OIDC |
| IAM roles | Least privilege, separate plan/apply optional | Reasonable | Admin keys or single mega-role |
| Environments | Realistic prod protections | Basic | No prod distinction |
| Scanning policy | Actionable hard/soft fail + exceptions | Generic | Missing |
| Runbook | Specific commands/log locations | Partial | Vague |
| Migration | Phased, references prior weeks | Some gaps | Big-bang |

## Submission format

- `docs/assignments/week-04-yourname.md`
- Embed Mermaid or attach PNG

## Academic integrity

Individual work. Reference GitHub OIDC and HashiCorp automation docs.
