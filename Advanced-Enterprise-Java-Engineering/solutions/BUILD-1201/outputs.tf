output "repository_url" {
  description = "ECR repository URL for payment-service."
  value       = aws_ecr_repository.payment.repository_url
}

output "repository_arn" {
  description = "ECR repository ARN."
  value       = aws_ecr_repository.payment.arn
}

output "region" {
  description = "Region this root targeted."
  value       = var.region
}
