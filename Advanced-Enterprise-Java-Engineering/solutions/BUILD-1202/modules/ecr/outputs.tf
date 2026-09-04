output "repository_url" {
  description = "ECR repository URL."
  value       = aws_ecr_repository.this.repository_url
}

output "repository_arn" {
  description = "ECR repository ARN."
  value       = aws_ecr_repository.this.arn
}

output "region" {
  description = "Region passed into this module."
  value       = var.region
}
