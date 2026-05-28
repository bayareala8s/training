# Week 5 — Assignment: Promotion & Drift Governance Design

**Weight:** Part of 15% assignments grade · **Due:** End of Week 5 · **Length:** 3–4 pages or 1000–1500 words

## Prompt

You are the lead platform engineer for a company with **dev, test, and prod** AWS accounts. Teams complain that production “drifts” weekly due to console fixes during incidents. Promotion from test to prod is ad hoc—sometimes skipped under pressure.

### Tasks

1. **Promotion pipeline design** — Diagram and describe a promotion flow from dev → test → prod including:
   - Git branching strategy
   - CI jobs per environment
   - Required artifacts (plan files, approvals)
   - Who may trigger prod apply

2. **Drift management program** — Propose:
   - Detection (tools, frequency, read-only credentials)
   - Severity matrix and SLAs
   - Remediation runbook outline (tie to course drift report template)
   - Three prevention controls (IAM, SCP, or process)

3. **Refactoring case study** — A team wants to move all EC2 instances into `module.compute`. Write a **risk assessment** and step-by-step migration plan using `moved` blocks and/or `state mv`, including rollback if plan shows replacements.

4. **Executive summary** — Half page for a VP: business risk of uncontrolled drift vs cost of governance tooling.

## Rubric

| Criterion | Excellent (90–100%) | Proficient (75–89%) | Needs work (<75%) |
|-----------|----------------------|---------------------|-------------------|
| Promotion design | Clear gates, artifacts, roles; aligns with CI | Mostly complete | Missing prod controls |
| Drift program | Detect/remediate/prevent with SLAs | Generic advice | No operational detail |
| Refactoring plan | Addresses replacement risk, env order | High level only | Unsafe or vague |
| Executive summary | Business language, quantified risk | Technical only | Missing |

## Submission format

- PDF or Markdown: `docs/assignments/week-05-yourname.md`
- Include at least one Mermaid or architecture diagram

## Academic integrity

Individual work unless cohort specifies teams. Cite Terraform and AWS documentation.
