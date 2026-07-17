# AWS Lab {{LAB_NUMBER}} — {{LAB_TITLE}}

**Module:** {{MODULE_NUMBER}} — {{MODULE_TITLE}}  
**Estimated duration:** {{DURATION}}  
**Estimated cost:** {{COST_USD}} (when cleaned up promptly)  
**Region recommendation:** {{AWS_REGION}}  
**Case study:** NorthStar Financial Services (fictional)

---

## Cost and safety rules

- Prefer serverless; avoid NAT Gateway, always-on EC2, EKS, OpenSearch
- Avoid continuously running Transfer Family endpoints unless marked optional
- Tag all resources
- Create/verify a budget alert before deploying
- Run cleanup at the end of the session

### Required tags

```text
Project=BayLearn
Course=EnterpriseArchitectureLeadership
Module={{MODULE_NUMBER}}
Student=<student-id>
Environment=Lab
ExpirationDate=<YYYY-MM-DD>
```

---

## 1. Lab title

{{LAB_TITLE}}

## 2. Business context

{{BUSINESS_CONTEXT}}

## 3. Learning objectives

1. {{LO_1}}
2. {{LO_2}}
3. {{LO_3}}

## 4. Architecture diagram

```mermaid
{{MERMAID}}
```

## 5. AWS services

| Service | Purpose | Required? |
| ------- | ------- | --------- |
| {{SVC_1}} | {{PURPOSE_1}} | Yes |
| {{SVC_2}} | {{PURPOSE_2}} | Optional — cost warning: {{WARN}} |

## 6. Estimated duration

{{DURATION}}

## 7. Estimated cost

{{COST_DETAIL}}

## 8. Prerequisites

- AWS account with permissions documented in lab README
- Terraform {{TF_VERSION}}+
- AWS CLI configured
- Budget alarm capability

## 9. Security warnings

- {{SEC_1}}
- Do not use production data
- Do not expose public write access without explicit lab steps
- Rotate/destroy lab credentials after cleanup

## 10. Step-by-step implementation

### 10.1 Prepare

```bash
{{PREP_COMMANDS}}
```

### 10.2 Deploy

```bash
{{DEPLOY_COMMANDS}}
```

### 10.3 Configure / exercise

{{EXERCISE_STEPS}}

## 11. Validation steps

- [ ] {{V1}}
- [ ] {{V2}}
- [ ] {{V3}}

## 12. Failure scenarios

| Scenario | What to observe | Learning point |
| -------- | --------------- | -------------- |
| {{F1}} | {{O1}} | {{L1}} |

## 13. Troubleshooting

| Issue | Check | Fix |
| ----- | ----- | --- |
| {{I1}} | {{CHK1}} | {{FIX1}} |

## 14. Submission requirements

- Architecture write-up / ADRs as specified
- Screenshot or CLI evidence of validation
- Cost note and cleanup confirmation

## 15. Stretch objectives

- {{STRETCH_1}}

## 16. Cleanup steps

```bash
{{CLEANUP_COMMANDS}}
```

Confirm in console: no residual lab-tagged resources.

## 17. Reference solution

Instructor-only under `instructor/reference-solutions/module-{{MODULE_NUMBER}}/` and matching Terraform under `infrastructure/terraform/`.
