output "accounts_api_endpoint" {
  description = "HTTP API base URL for accounts"
  value       = aws_apigatewayv2_api.accounts.api_endpoint
}

output "create_account_url" {
  description = "POST /accounts URL"
  value       = "${aws_apigatewayv2_api.accounts.api_endpoint}/accounts"
}

output "event_bus_name" {
  value = aws_cloudwatch_event_bus.northstar.name
}

output "partner_bucket_name" {
  value = aws_s3_bucket.partner.bucket
}

output "payments_queue_url" {
  value = aws_sqs_queue.payments.url
}

output "payments_dlq_url" {
  value = aws_sqs_queue.payments_dlq.url
}

output "sns_topic_arn" {
  value = aws_sns_topic.alerts.arn
}

output "accounts_table_name" {
  value = aws_dynamodb_table.accounts.name
}

output "state_machine_arn" {
  value = aws_sfn_state_machine.regulatory_batch.arn
}

output "account_api_lambda" {
  value = aws_lambda_function.account_api.function_name
}

output "payment_processor_lambda" {
  value = aws_lambda_function.payment_processor.function_name
}

output "partner_file_lambda" {
  value = aws_lambda_function.partner_file.function_name
}
