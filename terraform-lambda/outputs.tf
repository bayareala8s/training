output "lambda_function_names" {
  value = aws_lambda_function.dynamic_lambdas[*].function_name
  description = "List of created Lambda functions"
}
