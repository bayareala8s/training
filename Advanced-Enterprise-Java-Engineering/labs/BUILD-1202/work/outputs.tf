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
