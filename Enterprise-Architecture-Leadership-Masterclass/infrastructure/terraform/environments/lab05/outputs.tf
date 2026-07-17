output "api_health_url" {
  value       = module.platform_foundation.api_health_url
  description = "Invoke this URL to validate the platform foundation"
}

output "api_endpoint" {
  value = module.platform_foundation.api_endpoint
}

output "audit_bucket_name" {
  value = module.platform_foundation.audit_bucket_name
}

output "dynamodb_table_name" {
  value = module.platform_foundation.dynamodb_table_name
}

output "lambda_function_name" {
  value = module.platform_foundation.lambda_function_name
}

output "cloudtrail_name" {
  value = module.platform_foundation.cloudtrail_name
}

output "ssm_parameter_prefix" {
  value = module.platform_foundation.ssm_parameter_prefix
}

output "budget_name" {
  value = module.platform_foundation.budget_name
}

output "cloudwatch_log_group" {
  value = module.platform_foundation.cloudwatch_log_group
}
