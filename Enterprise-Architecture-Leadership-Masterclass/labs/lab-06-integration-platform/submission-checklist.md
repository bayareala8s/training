# Submission Checklist — Lab 06

**Lab:** Build NorthStar’s Integration Reference Architecture  
**Submit via:** BayLearn assignment drop for Module 06 (lab portion)

---

## Infrastructure and evidence

- [ ] `terraform apply` succeeded (or instructor-approved architecture-only path documented)
- [ ] Outputs captured (API URL, event bus, bucket, state machine ARN, queue URLs)
- [ ] Required tags present on resources
- [ ] SNS email subscription **Confirmed**
- [ ] Account API evidence (POST create + GET/lookup)
- [ ] Payment event path evidence (EventBridge → SQS → Lambda)
- [ ] Partner file evidence (S3 `incoming/` → Lambda)
- [ ] Step Functions execution evidence (or blocker note + design narrative)
- [ ] Cleanup confirmed (`cleanup-lab06.sh` or `terraform destroy` log)
- [ ] Cost note (estimated spend; budget alert mentioned)

## Architecture artifacts

- [ ] Integration pattern matrix with criteria scores (template 16)
- [ ] Reference architecture diagram (Mermaid or exported image)
- [ ] Data-flow diagram for payments + partner files (template 22)
- [ ] ADR-M06-01 (sync vs events for account create side effects)
- [ ] ADR-M06-02 (Transfer Family/MFT vs S3 landing) with cost trade-off
- [ ] Ownership notes: domain vs platform for at least payments + accounts

## Quality gates

- [ ] No Transfer Family / NAT / EKS / always-on EC2 proposed as lab deploy
- [ ] DLQ called out for payment path
- [ ] Fiction/assumptions stated for NorthStar context
- [ ] Filenames: `M06_<Artifact>_<LastName>.<ext>`
