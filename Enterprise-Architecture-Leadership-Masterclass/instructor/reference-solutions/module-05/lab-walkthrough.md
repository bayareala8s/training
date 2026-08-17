# Lab Walkthrough — Module 05

1. `cp terraform.tfvars.example terraform.tfvars` and set student_id + email
2. `terraform init && terraform apply`
3. `curl $(terraform output -raw api_health_url)` → status ok
4. Scan DynamoDB for HEARTBEAT
5. Confirm budget name output
6. `../../../scripts/cleanup-lab05.sh`

Expected teaching moment: map each resource to a strategy control.
