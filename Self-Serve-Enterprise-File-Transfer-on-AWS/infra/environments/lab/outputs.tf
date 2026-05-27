output "aws_region" {
  value = data.aws_region.current.id
}

output "landing_bucket" {
  value = module.landing_bucket.bucket_id
}

output "logs_bucket" {
  value = module.logs_bucket.bucket_id
}

output "kms_key_arn" {
  value = module.kms.key_arn
}

output "inbound_s3_prefix" {
  value = local.inbound_prefix
}

output "partner_prefix" {
  value = local.partner_prefix
}

output "transfer_server_endpoint" {
  value       = var.enable_transfer_family ? module.transfer[0].server_endpoint : null
  description = "SFTP hostname (no protocol prefix)."
}

output "transfer_server_id" {
  value = var.enable_transfer_family ? module.transfer[0].server_id : null
}

output "sftp_username" {
  value = var.inbound_username
}

output "sftp_private_key_secret_arn" {
  value       = var.enable_transfer_family ? module.transfer[0].inbound_private_key_secret_arn : null
  sensitive   = true
  description = "Secrets Manager ARN for partner-demo private key (PEM)."
}

output "transfer_connector_id" {
  value = var.enable_transfer_family && var.enable_connector ? module.transfer[0].connector_id : null
}

output "idempotency_table" {
  value = aws_dynamodb_table.idempotency.name
}

output "connections_table" {
  value = aws_dynamodb_table.connections.name
}

output "jobs_table" {
  value = aws_dynamodb_table.jobs.name
}

output "state_machine_arn" {
  value = aws_sfn_state_machine.transfer.arn
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.http.api_endpoint
}

output "cognito_user_pool_id" {
  value = aws_cognito_user_pool.lab.id
}

output "cognito_client_id" {
  value = aws_cognito_user_pool_client.api.id
}

output "cognito_test_username" {
  value = var.admin_email
}

output "cloudwatch_dashboard_name" {
  value = aws_cloudwatch_dashboard.lab.dashboard_name
}

output "ecs_cluster_name" {
  value       = var.enable_ecs_worker ? module.ecs_worker[0].cluster_name : null
  description = "Lab 9 ECS cluster"
}

output "ecs_task_definition" {
  value       = var.enable_ecs_worker ? module.ecs_worker[0].task_definition_family : null
  description = "Lab 9 Fargate task family"
}

output "ecr_repository_url" {
  value       = var.enable_ecs_worker ? module.ecs_worker[0].ecr_repository_url : null
  description = "Push worker image via scripts/build_ecs_worker.sh"
}

output "ecs_worker_log_group" {
  value = var.enable_ecs_worker ? module.ecs_worker[0].log_group_name : null
}

output "large_file_inbound_prefix" {
  value = "partners/${var.partner_id}/large/inbound/"
}

output "large_file_processed_prefix" {
  value = "partners/${var.partner_id}/large/processed/"
}

output "ecs_subnet_ids" {
  value       = var.enable_ecs_worker ? module.networking[0].public_subnet_ids : []
  description = "Public subnets for Fargate tasks (Lab 9)"
}

output "ecs_security_group_id" {
  value = var.enable_ecs_worker ? module.networking[0].ecs_security_group_id : null
}

output "lab_stack_summary" {
  value = <<-EOT
    BayLearn MFT lab stack (${local.name_prefix})
    Region: ${data.aws_region.current.id}
    Landing bucket: ${module.landing_bucket.bucket_id}
    SFTP: ${var.enable_transfer_family ? "${var.inbound_username}@${module.transfer[0].server_endpoint}" : "disabled"}
    API: ${aws_apigatewayv2_api.http.api_endpoint}
    Cognito user: ${var.admin_email}
    ECS Fargate (Lab 9): ${var.enable_ecs_worker ? "enabled — run tasks on demand only" : "disabled"}
    Stop costs: ./scripts/stop_stack.sh --yes
  EOT
}
