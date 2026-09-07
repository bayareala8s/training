output "repository_url" {
  description = "Push baypay/payment-service:<tag> here. Never :latest."
  value       = aws_ecr_repository.payment.repository_url
}

output "repository_arn" {
  description = "ECR repository ARN in us-west-2."
  value       = aws_ecr_repository.payment.arn
}
