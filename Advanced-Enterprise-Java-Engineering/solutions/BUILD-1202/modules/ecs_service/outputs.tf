output "container_port" {
  description = "Listen port the task and ALB must agree on."
  value       = var.container_port
}

output "health_check_path" {
  description = "Health path the task and ALB must agree on."
  value       = var.health_check_path
}

output "log_group_name" {
  description = "CloudWatch log group for the service."
  value       = aws_cloudwatch_log_group.service.name
}

output "service_contract" {
  description = "Reusable name, port, health path, and image contract."
  value       = local.service_contract
}
