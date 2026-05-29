# Terraform — Course Platform

Deploys shared AWS infrastructure for Modules 4–9.

## Resources

- VPC with public/private subnets and single NAT gateway
- EventBridge custom event bus
- DynamoDB orders table (example)
- ECR repositories for all four services
- ECS cluster, security group, CloudWatch log group

## Usage

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

## Module 4 Lab Extension

Students create ECS task definitions and services referencing ECR images built in Module 3. See `labs/module-04/README.md`.

## Cost Control

```bash
terraform destroy
```

Run when labs end for the day.
