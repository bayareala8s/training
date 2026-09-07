output "repository_url" {
  value = module.ecr.repository_url
}

output "repository_arn" {
  value = module.ecr.repository_arn
}

output "container_port" {
  value = module.ecs_service.container_port
}

output "health_check_path" {
  value = module.ecs_service.health_check_path
}

output "service_contract" {
  value = module.ecs_service.service_contract
}

output "alb_contract" {
  description = "ACCOUNT.md ALB / Fargate shape. Not a live aws_lb (COST-1105)."
  value       = local.alb_contract
}
