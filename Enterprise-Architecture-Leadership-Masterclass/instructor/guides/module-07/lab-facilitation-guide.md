# Lab Facilitation Guide — Module 07

## Pre-lab (instructor)

1. Verify your own `terraform apply` in a sandbox within the last week
2. Confirm cleanup script empties versioned buckets
3. Prepare a sample control-evidence row on a slide
4. Remind cohort: **no real PII**; budget alert; CRR off by default

## During lab

| Time | Action |
| ---- | ------ |
| T+0 | Restate deliverables and cleanup rule |
| T+10 | Check: terraform init/plan succeeded |
| T+20 | Check: object uploaded with SSE-KMS |
| T+30 | Mid-check: recovery drill started; STRIDE draft exists |
| T+40 | Stop-ship for debrief even if incomplete; assign homework finish + cleanup |

## Stuck students

- **KMS AccessDenied:** deploy role vs lab roles; use caller identity that has key permissions from account root path for initial upload if assume-role not set up; still require policy analysis in write-up
- **Bucket not empty on destroy:** run cleanup script, not raw destroy alone
- **Alarm INSUFFICIENT_DATA:** acceptable if configuration documented; invoke drill Lambda to emit metric

## Safety

If a student enables public access, stop and remediate immediately; treat as teaching moment on Block Public Access.
