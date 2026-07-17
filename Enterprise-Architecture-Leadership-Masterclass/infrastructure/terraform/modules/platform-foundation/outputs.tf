output "audit_bucket_name" {
  description = "S3 audit / CloudTrail bucket name"
  value       = aws_s3_bucket.audit.id
}

output "audit_bucket_arn" {
  description = "S3 audit bucket ARN"
  value       = aws_s3_bucket.audit.arn
}

output "cloudtrail_name" {
  description = "CloudTrail name if enabled"
  value       = var.enable_cloudtrail ? aws_cloudtrail.lab[0].name : null
}

output "dynamodb_table_name" {
  description = "Platform registry DynamoDB table"
  value       = aws_dynamodb_table.platform_registry.name
}

output "dynamodb_table_arn" {
  description = "Platform registry DynamoDB table ARN"
  value       = aws_dynamodb_table.platform_registry.arn
}

output "lambda_function_name" {
  description = "Platform health Lambda name"
  value       = aws_lambda_function.platform_health.function_name
}

output "lambda_function_arn" {
  description = "Platform health Lambda ARN"
  value       = aws_lambda_function.platform_health.arn
}

output "api_endpoint" {
  description = "HTTP API Gateway invoke URL"
  value       = aws_apigatewayv2_api.platform.api_endpoint
}

output "api_health_url" {
  description = "Health check URL"
  value       = "${aws_apigatewayv2_api.platform.api_endpoint}/health"
}

output "ssm_parameter_prefix" {
  description = "SSM Parameter Store prefix for platform config"
  value       = "/${var.name_prefix}/platform"
}

output "lambda_role_arn" {
  description = "IAM role ARN for Lambda"
  value       = aws_iam_role.lambda.arn
}

output "budget_name" {
  description = "AWS Budgets name"
  value       = aws_budgets_budget.lab.name
}

output "cloudwatch_log_group" {
  description = "Lambda CloudWatch log group name"
  value       = aws_cloudwatch_log_group.lambda.name
}

output "config_enabled" {
  description = "Whether AWS Config was enabled (optional)"
  value       = var.enable_config
}
