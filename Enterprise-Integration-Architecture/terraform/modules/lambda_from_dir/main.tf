terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
    archive = {
      source = "hashicorp/archive"
    }
  }
}

variable "name" { type = string }
variable "source_dir" { type = string }
variable "build_path" { type = string }
variable "timeout" {
  type    = number
  default = 15
}
variable "environment" {
  type    = map(string)
  default = {}
}
variable "policy_json" { type = string }

data "archive_file" "fn" {
  type        = "zip"
  output_path = "${var.build_path}/${var.name}.zip"
  source_dir  = var.source_dir
  excludes    = ["__pycache__", "*.pyc"]
}

resource "aws_iam_role" "fn" {
  name = "${var.name}-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "fn" {
  role   = aws_iam_role.fn.id
  policy = var.policy_json
}

resource "aws_cloudwatch_log_group" "fn" {
  name              = "/aws/lambda/${var.name}"
  retention_in_days = 7
}

resource "aws_lambda_function" "fn" {
  function_name    = var.name
  role             = aws_iam_role.fn.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.fn.output_path
  source_code_hash = data.archive_file.fn.output_base64sha256
  timeout          = var.timeout
  depends_on       = [aws_cloudwatch_log_group.fn]
  environment {
    variables = var.environment
  }
}

output "arn" { value = aws_lambda_function.fn.arn }
output "invoke_arn" { value = aws_lambda_function.fn.invoke_arn }
output "function_name" { value = aws_lambda_function.fn.function_name }
output "role_arn" { value = aws_iam_role.fn.arn }
