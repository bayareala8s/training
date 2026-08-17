# Runbook — Failover & Failback (Option 3)

## Pre-checks

- [ ] Primary healthy (`terraform plan` clean)
- [ ] Secondary stack applied in `us-east-1`
- [ ] Stakeholders notified (tabletop) or change ticket open (live)

## Failover (primary → secondary)

1. Declare incident / start tabletop clock.
2. Confirm secondary VPC outputs:
   ```bash
   cd terraform/environments/secondary
   terraform output vpc_id
   terraform output region
   ```
3. If compute enabled on secondary: start instances (`AWS_REGION=us-east-1 ./scripts/aws/start-lab.sh`).
4. Update application traffic (DNS / load balancer) to secondary endpoints (**manual** in this lab).
5. Freeze primary applies (protect state; communicate “no terraform apply on primary”).
6. Record decision log: time, actor, evidence.

## Failback (secondary → primary)

1. Confirm primary restored and plan is clean.
2. Drain secondary traffic.
3. Re-point DNS to primary.
4. Stop secondary lab compute to save cost.
5. Post-incident review within 5 business days.

## Rollback of Terraform mistakes

Use Week 6 patterns: Git revert + plan; S3 state versioning for state recovery.

## Contacts

| Role | Responsibility |
|------|----------------|
| Capstone owner | Execute runbook |
| Instructor | Approve live DNS changes (if any) |
