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
      Project     = "baylearn-eia"
      Lab         = "lab-02-api"
      Environment = "lab"
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
  name = "eia-lab02-${random_string.suffix.result}"
}

resource "aws_dynamodb_table" "orders" {
  name         = "${local.name}-orders"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
  attribute {
    name = "orderId"
    type = "S"
  }
  global_secondary_index {
    name            = "orderId-index"
    hash_key        = "orderId"
    projection_type = "ALL"
  }
}

data "archive_file" "fn" {
  type        = "zip"
  output_path = "${path.module}/.build/orders.zip"
  source_dir  = "${path.module}/../../../lambda/lab02_orders"
  excludes    = ["__pycache__", "*.pyc"]
}

data "archive_file" "shared" {
  type        = "zip"
  output_path = "${path.module}/.build/shared.zip"
  source {
    content  = file("${path.module}/../../../lambda/shared/eia_common.py")
    filename = "python/eia_common.py"
  }
}

resource "aws_iam_role" "fn" {
  name = "${local.name}-orders-role"
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
  name = "${local.name}-orders-policy"
  role = aws_iam_role.fn.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Query"
        ]
        Resource = [
          aws_dynamodb_table.orders.arn,
          "${aws_dynamodb_table.orders.arn}/index/*"
        ]
      }
    ]
  })
}

resource "aws_lambda_layer_version" "shared" {
  layer_name          = "${local.name}-shared"
  filename            = data.archive_file.shared.output_path
  source_code_hash    = data.archive_file.shared.output_base64sha256
  compatible_runtimes = ["python3.12"]
}

resource "aws_cloudwatch_log_group" "orders" {
  name              = "/aws/lambda/${local.name}-orders"
  retention_in_days = 7
}

resource "aws_lambda_function" "orders" {
  function_name    = "${local.name}-orders"
  role             = aws_iam_role.fn.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.fn.output_path
  source_code_hash = data.archive_file.fn.output_base64sha256
  timeout          = 10
  layers           = [aws_lambda_layer_version.shared.arn]
  depends_on       = [aws_cloudwatch_log_group.orders]
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.orders.name
    }
  }
}

resource "aws_apigatewayv2_api" "http" {
  name          = "${local.name}-http"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "fn" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.orders.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "post" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /orders"
  target    = "integrations/${aws_apigatewayv2_integration.fn.id}"
}

resource "aws_apigatewayv2_route" "get" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "GET /orders/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.fn.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.orders.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.http.api_endpoint
}

output "table_name" {
  value = aws_dynamodb_table.orders.name
}

output "function_name" {
  value = aws_lambda_function.orders.function_name
}

output "aws_region" {
  value = var.aws_region
}
