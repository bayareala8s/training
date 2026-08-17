output "platform_active" {
  value = var.platform_active
}

output "aws_region" {
  value = var.aws_region
}

output "aws_account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "alb_dns_name" {
  value       = local.enable_alb ? aws_lb.main[0].dns_name : "ALB stopped (platform_active=false)"
  description = "Public URL for all services"
}

output "platform_url" {
  value = local.enable_alb ? "http://${aws_lb.main[0].dns_name}" : ""
}

output "event_bus_name" {
  value = aws_cloudwatch_event_bus.platform.name
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "ecr_repository_urls" {
  value = { for k, r in aws_ecr_repository.services : k => r.repository_url }
}

output "dynamodb_orders_table" {
  value = aws_dynamodb_table.orders.name
}

output "service_discovery_namespace" {
  value = local.service_discovery_namespace
}

output "ecs_service_names" {
  value = keys(local.services)
}

output "health_check_urls" {
  value = local.enable_alb ? {
    user         = "http://${aws_lb.main[0].dns_name}/health"
    product      = "http://${aws_lb.main[0].dns_name}/health"
    notification = "http://${aws_lb.main[0].dns_name}/health"
  } : {}
}
