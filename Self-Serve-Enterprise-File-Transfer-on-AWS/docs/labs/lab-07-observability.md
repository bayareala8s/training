# Lab 7 — Observability pack

**Week 7 · Estimated time: 3 hours**

> **Terraform:** Dashboard `baylearn-mft-lab-ops`, alarms for Lambda errors and Step Functions failures.

## Objectives

Dashboards, alarms, and operations runbook v0.1 for your sandbox platform.

## Steps

### 1. Open dashboard

```bash
open "https://$(terraform -chdir=infra/environments/lab output -raw aws_region).console.aws.amazon.com/cloudwatch/home?region=$(terraform -chdir=infra/environments/lab output -raw aws_region)#dashboards:name=$(terraform -chdir=infra/environments/lab output -raw cloudwatch_dashboard_name)"
```

### 2. List alarms

```bash
aws cloudwatch describe-alarms --alarm-name-prefix baylearn-mft-lab
```

### 3. Trigger test alarm (optional)

Upload invalid file to cause quarantine log activity; or invoke failed Step Functions input.

### 4. Runbook

Create `submissions/week-07/runbook.md` with sections:

1. **Service overview**  
2. **Dashboards & alarms**  
3. **Partner onboarding** (checklist)  
4. **Incident: transfer failed** (triage steps)  
5. **Rollback / disable partner**  
6. **Cost controls**  

## Rubric (10 pts)

| Criterion | Points |
|-----------|--------|
| Dashboard | 3 |
| Alarms | 3 |
| Runbook completeness | 4 |
