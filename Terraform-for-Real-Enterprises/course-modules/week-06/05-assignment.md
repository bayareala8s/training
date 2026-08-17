# Week 6 — Assignment: DR Tabletop & Recovery Playbook

**Weight:** Part of 15% assignments grade · **Due:** End of Week 6 · **Length:** 3–4 pages or 1000–1500 words

## Prompt

Your organization’s Terraform state bucket lives in **us-west-2**. The platform team runs 40 stacks across dev/test/prod accounts. You must prepare for operational failures—not hypothetical “everything is fine” documentation.

### Tasks

1. **Failed apply tabletop** — Narrate a scenario where an apply fails mid-way creating an ALB and target group. Document:
   - First 15 minutes of response (commands, who to notify)
   - How you decide forward fix vs revert
   - What you log for post-incident review

2. **State recovery decision tree** — When do you use each?
   - `terraform state pull` backup
   - S3 version restore
   - `state rm` + import
   - Git revert + apply  
   Include **one example where state restore is the wrong choice**.

3. **Disaster scenario** — Tabletop: state bucket is unavailable (regional impairment). Describe RTO/RPO targets, cross-region replication recommendation, and how teams can **read** infrastructure if apply is blocked for 4 hours.

4. **Runbook gap analysis** — Compare your lab `docs/runbooks/terraform-recovery.md` to the above scenarios. List three gaps and how you would close them.

## Rubric

| Criterion | Excellent (90–100%) | Proficient (75–89%) | Needs work (<75%) |
|-----------|----------------------|---------------------|-------------------|
| Failed apply response | Concrete commands, roles, timelines | General steps | Impractical or dangerous |
| State recovery tree | Correct tradeoffs, wrong-choice example | Mostly correct | Confuses Git vs state |
| DR scenario | RTO/RPO, replication, read-only ops | Partial | Ignores state dependency |
| Gap analysis | Specific improvements to own runbook | Generic | Not tied to lab work |

## Submission format

- PDF or Markdown: `docs/assignments/week-06-yourname.md`
- Attach or link completed `docs/runbooks/terraform-recovery.md`

## Academic integrity

Individual work. Tabletop is fictional—do not run destructive tests in shared prod accounts.
