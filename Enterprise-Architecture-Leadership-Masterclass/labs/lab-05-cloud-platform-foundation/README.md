# Lab 05 — Design and Deploy a Low-Cost Enterprise Platform Foundation

**Module:** 05 — Cloud and Platform Strategy  
**Estimated duration:** 90–120 minutes (including artifacts)  
**Estimated cost:** ~<$5 when cleaned up promptly  
**Region:** us-east-1 recommended  
**Case study:** NorthStar Financial Services (fictional)

## Files

| File | Audience |
| ---- | -------- |
| `student-instructions.md` | Students |
| `submission-checklist.md` | Students |
| `stretch-objectives.md` | Students |
| Terraform | `infrastructure/terraform/environments/lab05/` |
| Cost estimate | `infrastructure/cost-estimates/lab-05.md` |
| Cleanup | `infrastructure/terraform/scripts/cleanup-lab05.sh` |

## Quick start

```bash
cd infrastructure/terraform/environments/lab05
cp terraform.tfvars.example terraform.tfvars
# edit values
terraform init && terraform apply
curl "$(terraform output -raw api_health_url)"
../../../scripts/cleanup-lab05.sh
```
