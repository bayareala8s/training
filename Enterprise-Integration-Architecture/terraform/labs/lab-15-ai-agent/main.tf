terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.50"
    }
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.4"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project = "baylearn-eia"
      Lab     = "lab-15-ai-agent"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-west-2"
}

resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

locals {
  name = "eia-lab15-${random_string.suffix.result}"
}

variable "enable_bedrock" {
  type    = bool
  default = false
}
resource "aws_dynamodb_table" "catalog" {
  name         = "${local.name}-catalog"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}
resource "aws_dynamodb_table" "appr" {
  name         = "${local.name}-appr"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}
resource "aws_dynamodb_table_item" "demo" {
  table_name = aws_dynamodb_table.catalog.name
  hash_key   = "pk"
  item = jsonencode({
    pk            = { S = "FILE#demo.csv" }
    status        = { S = "QUARANTINED" }
    correlationId = { S = "demo-corr" }
    error         = { S = "SCHEMA" }
    errorMessage  = { S = "CSV header missing partner column" }
    partner       = { S = "ABC" }
  })
}
data "archive_file" "fn" {
  type        = "zip"
  output_path = "${path.module}/.build/tools.zip"
  source_dir  = "${path.module}/../../../lambda/lab15_tools"
}
resource "aws_iam_role" "fn" {
  name = "${local.name}-tools"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
resource "aws_sqs_queue" "ops" {
  name = "${local.name}-ops"
}

resource "aws_iam_role_policy" "fn" {
  role = aws_iam_role.fn.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:UpdateItem"], Resource = [aws_dynamodb_table.catalog.arn, aws_dynamodb_table.appr.arn] },
      { Effect = "Allow", Action = ["sqs:GetQueueAttributes"], Resource = aws_sqs_queue.ops.arn }
    ]
  })
}
resource "aws_lambda_function" "fn" {
  function_name    = "${local.name}-tools"
  role             = aws_iam_role.fn.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.fn.output_path
  source_code_hash = data.archive_file.fn.output_base64sha256
  timeout          = 15
  environment {
    variables = {
      CATALOG_TABLE  = aws_dynamodb_table.catalog.name
      APPROVAL_TABLE = aws_dynamodb_table.appr.name
      QUEUE_URL      = aws_sqs_queue.ops.url
    }
  }
}
resource "aws_apigatewayv2_api" "http" {
  name          = "${local.name}-tools"
  protocol_type = "HTTP"
}
resource "aws_apigatewayv2_integration" "fn" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.fn.invoke_arn
  payload_format_version = "2.0"
}
resource "aws_apigatewayv2_route" "post" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /tools"
  target    = "integrations/${aws_apigatewayv2_integration.fn.id}"
}
resource "aws_apigatewayv2_route" "approve" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /approve"
  target    = "integrations/${aws_apigatewayv2_integration.fn.id}"
}
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
}
resource "aws_lambda_permission" "apigw" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.fn.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}
output "tools_url" { value = "${aws_apigatewayv2_api.http.api_endpoint}/tools" }
output "approve_url" { value = "${aws_apigatewayv2_api.http.api_endpoint}/approve" }
output "catalog_table" { value = aws_dynamodb_table.catalog.name }
output "approval_table" { value = aws_dynamodb_table.appr.name }
output "enable_bedrock" { value = var.enable_bedrock }
output "aws_region" { value = var.aws_region }
