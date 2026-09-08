output "alb_dns_name" {
  description = "Public ALB DNS. Demo URL is http://<this>/api/v1/payments"
  value       = aws_lb.pay.dns_name
}

output "demo_base_url" {
  value = "http://${aws_lb.pay.dns_name}"
}

output "ecr_repository_url" {
  description = "Push baypay/payment-service-ecs-demo:<immutable-tag> here. Never :latest."
  value       = aws_ecr_repository.payment.repository_url
}

output "cluster_name" {
  value = aws_ecs_cluster.lab.name
}

output "service_name" {
  value = local.deploy ? aws_ecs_service.payment[0].name : null
}

output "db_endpoint" {
  description = "Private RDS hostname. Not reachable from your laptop."
  value       = aws_db_instance.baypay.address
}

output "secret_arn" {
  value = aws_secretsmanager_secret.db.arn
}

output "target_group_arn" {
  value = aws_lb_target_group.pay.arn
}
