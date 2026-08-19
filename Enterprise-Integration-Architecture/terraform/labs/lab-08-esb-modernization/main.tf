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
      Lab     = "lab-08-esb-modernization"
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
  name = "eia-lab08-${random_string.suffix.result}"
}

resource "aws_dynamodb_table" "t" {
  name         = "${local.name}-bal"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}

resource "aws_dynamodb_table_item" "demo" {
  table_name = aws_dynamodb_table.t.name
  hash_key   = "pk"
  item = jsonencode({
    pk         = { S = "BAL#demo" }
    customerId = { S = "demo" }
    balance    = { S = "100.00" }
    source     = { S = "new-api" }
  })
}

module "facade" {
  source      = "../../modules/lambda_from_dir"
  name        = "${local.name}-facade"
  source_dir  = "${path.module}/../../../lambda/lab08_facade"
  build_path  = "${path.module}/.build"
  environment = { TABLE_NAME = aws_dynamodb_table.t.name }
  policy_json = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["dynamodb:GetItem"], Resource = aws_dynamodb_table.t.arn }
    ]
  })
}

resource "aws_apigatewayv2_api" "http" {
  name          = "${local.name}-http"
  protocol_type = "HTTP"
}
resource "aws_apigatewayv2_integration" "fn" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = module.facade.invoke_arn
  payload_format_version = "2.0"
}
resource "aws_apigatewayv2_route" "get" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "GET /balances/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.fn.id}"
}
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
}
resource "aws_lambda_permission" "apigw" {
  action        = "lambda:InvokeFunction"
  function_name = module.facade.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}

output "api_endpoint" { value = aws_apigatewayv2_api.http.api_endpoint }
output "aws_region" { value = var.aws_region }
