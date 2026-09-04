output "alb_dns_name" {
  description = "Apply uses this DNS name. Teaching hostname is pay-alb-student.baypay.example."
  value       = aws_lb.pay.dns_name
}

output "ecr_repository_url" {
  description = "Push baypay/payment-service:<tag> here. Never :latest."
  value       = aws_ecr_repository.payment.repository_url
}

output "cluster_name" {
  value = aws_ecs_cluster.lab.name
}

output "service_name" {
  value = aws_ecs_service.payment.name
}

output "health_check_path" {
  description = "Must match ACCOUNT.md liveness. Never /."
  value       = "/actuator/health/liveness"
}
