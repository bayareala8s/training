output "create_account_url" {
  value       = module.integration_platform.create_account_url
  description = "POST to create an account"
}

output "accounts_api_endpoint" {
  value = module.integration_platform.accounts_api_endpoint
}

output "event_bus_name" {
  value = module.integration_platform.event_bus_name
}

output "partner_bucket_name" {
  value = module.integration_platform.partner_bucket_name
}

output "payments_queue_url" {
  value = module.integration_platform.payments_queue_url
}

output "sns_topic_arn" {
  value = module.integration_platform.sns_topic_arn
}

output "accounts_table_name" {
  value = module.integration_platform.accounts_table_name
}

output "state_machine_arn" {
  value = module.integration_platform.state_machine_arn
}

output "payment_processor_lambda" {
  value = module.integration_platform.payment_processor_lambda
}

output "partner_file_lambda" {
  value = module.integration_platform.partner_file_lambda
}
