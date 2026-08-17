# Lab 4 — Step Functions transfer workflow

**Week 4 · Estimated time: 4 hours**

> **Terraform:** State machine `baylearn-mft-lab-transfer-workflow`, SNS topics, workflow Lambdas. ASL: `infra/environments/lab/workflows/transfer-workflow.asl.json`.

## Objectives

Build a Standard workflow: **Start → Copy/Validate (Lambda) → Choice → Notify (SNS) → Success/Fail**.

## Steps

### 1. Export ASL for deliverable

```bash
cp infra/environments/lab/workflows/transfer-workflow.asl.json submissions/week-04/state-machine.asl.json
# Or pull live definition from console / AWS CLI describe-state-machine
```

### 2. Start execution

```bash
BUCKET=$(terraform -chdir=infra/environments/lab output -raw landing_bucket)
SFN=$(terraform -chdir=infra/environments/lab output -raw state_machine_arn)
aws stepfunctions start-execution \
  --state-machine-arn "$SFN" \
  --name "lab04-$(date +%s)" \
  --input "{\"bucket\":\"$BUCKET\",\"key\":\"partners/demo/inbound/sample.csv\",\"correlation_id\":\"$(uuidgen)\"}"
```

### 3. Confirm SNS

Check email for `you@example.com` (from `terraform.tfvars`) — **confirm SNS subscriptions** in inbox after first apply.

### 4. Execution history

Open Step Functions console → execution → verify Validate → Choice → Copy → Notify path.

## Deliverables

- ASL file + execution ARN in README  
- Screenshot of successful graph in console  

## Rubric (10 pts)

| Criterion | Points |
|-----------|--------|
| End-to-end success path | 4 |
| Failure path + SNS | 3 |
| Retries configured | 2 |
| correlation_id in logs | 1 |
