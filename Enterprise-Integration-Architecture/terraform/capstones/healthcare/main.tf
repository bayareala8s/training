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
      Project  = "baylearn-eia"
      Capstone = "healthcare"
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
  name = "eia-hlth-${random_string.suffix.result}"
}

resource "aws_dynamodb_table" "patients" {
  name         = "${local.name}-pt"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}

resource "aws_dynamodb_table_item" "pt1" {
  table_name = aws_dynamodb_table.patients.name
  hash_key   = "pk"
  item = jsonencode({
    pk            = { S = "PT#pt-1" }
    patientId     = { S = "pt-1" }
    name          = { S = "Alex Rivera" }
    status        = { S = "active" }
    accountStatus = { S = "current" }
  })
}
resource "aws_dynamodb_table_item" "pt2" {
  table_name = aws_dynamodb_table.patients.name
  hash_key   = "pk"
  item = jsonencode({
    pk            = { S = "PT#pt-2" }
    patientId     = { S = "pt-2" }
    name          = { S = "Jordan Lee" }
    status        = { S = "active" }
    accountStatus = { S = "current" }
  })
}

resource "aws_apigatewayv2_api" "http" {
  name          = "${local.name}-http"
  protocol_type = "HTTP"
}

module "patients" {
  source      = "../../modules/lambda_from_dir"
  name        = "${local.name}-pt"
  source_dir  = "${path.module}/../../../lambda/cap_health_patients"
  build_path  = "${path.module}/.build"
  environment = { TABLE_NAME = aws_dynamodb_table.patients.name }
  policy_json = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["dynamodb:GetItem"], Resource = aws_dynamodb_table.patients.arn }
    ]
  })
}

module "tools" {
  source      = "../../modules/lambda_from_dir"
  name        = "${local.name}-tools"
  source_dir  = "${path.module}/../../../lambda/cap_health_tools"
  build_path  = "${path.module}/.build"
  environment = { PATIENTS_API_URL = aws_apigatewayv2_api.http.api_endpoint }
  policy_json = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" }
    ]
  })
}

resource "aws_apigatewayv2_integration" "pt" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = module.patients.invoke_arn
  payload_format_version = "2.0"
}
resource "aws_apigatewayv2_integration" "tools" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = module.tools.invoke_arn
  payload_format_version = "2.0"
}
resource "aws_apigatewayv2_route" "get" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "GET /patients/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.pt.id}"
}
resource "aws_apigatewayv2_route" "tools" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /tools"
  target    = "integrations/${aws_apigatewayv2_integration.tools.id}"
}
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
}
resource "aws_lambda_permission" "pt" {
  action        = "lambda:InvokeFunction"
  function_name = module.patients.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}
resource "aws_lambda_permission" "tools" {
  action        = "lambda:InvokeFunction"
  function_name = module.tools.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}

output "api_endpoint" { value = aws_apigatewayv2_api.http.api_endpoint }
output "table_name" { value = aws_dynamodb_table.patients.name }
output "aws_region" { value = var.aws_region }
