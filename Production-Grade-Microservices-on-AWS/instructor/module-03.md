# Instructor Notes — Module 3

## AWS prep

- Pre-create ECR repos via Terraform
- Students need `ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, `ecr:PutImage`

## Demo

`./scripts/demo-platform.sh` after compose up.

## Cost warning

Remind students to `docker system prune` and destroy unused ECR images.
