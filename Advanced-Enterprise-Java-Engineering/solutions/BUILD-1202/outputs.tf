output "repository_url" {
  description = "ECR repository URL from module.ecr."
  value       = module.ecr.repository_url
}

output "repository_arn" {
  description = "ECR repository ARN from module.ecr."
  value       = module.ecr.repository_arn
}

output "service_contract" {
  description = "Port, health path, and log group the next environment must honor."
  value       = module.ecs_service.service_contract
}

output "region" {
  description = "Region this root targeted."
  value       = var.region
}
