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
      Capstone = "ecommerce"
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
  name = "eia-ecom-${random_string.suffix.result}"
}

resource "aws_dynamodb_table" "orders" {
  name         = "${local.name}-orders"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}

resource "aws_cloudwatch_event_bus" "bus" {
  name = "${local.name}-bus"
}

locals {
  lambda_env = {
    TABLE_NAME = aws_dynamodb_table.orders.name
    BUS_NAME   = aws_cloudwatch_event_bus.bus.name
  }
  lambda_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["events:PutEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:UpdateItem"], Resource = aws_dynamodb_table.orders.arn }
    ]
  })
}

module "api" {
  source      = "../../modules/lambda_from_dir"
  name        = "${local.name}-api"
  source_dir  = "${path.module}/../../../lambda/cap_ecom_api"
  build_path  = "${path.module}/.build"
  environment = local.lambda_env
  policy_json = local.lambda_policy
}
module "pay" {
  source      = "../../modules/lambda_from_dir"
  name        = "${local.name}-pay"
  source_dir  = "${path.module}/../../../lambda/cap_ecom_payment"
  build_path  = "${path.module}/.build"
  environment = local.lambda_env
  policy_json = local.lambda_policy
}
module "inv" {
  source      = "../../modules/lambda_from_dir"
  name        = "${local.name}-inv"
  source_dir  = "${path.module}/../../../lambda/cap_ecom_inventory"
  build_path  = "${path.module}/.build"
  environment = local.lambda_env
  policy_json = local.lambda_policy
}
module "saga" {
  source      = "../../modules/lambda_from_dir"
  name        = "${local.name}-saga"
  source_dir  = "${path.module}/../../../lambda/cap_ecom_saga"
  build_path  = "${path.module}/.build"
  environment = local.lambda_env
  policy_json = local.lambda_policy
}

resource "aws_cloudwatch_event_rule" "pay" {
  name           = "${local.name}-pay"
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  event_pattern  = jsonencode({ "detail-type" = ["OrderCreated"] })
}
resource "aws_cloudwatch_event_target" "pay" {
  rule           = aws_cloudwatch_event_rule.pay.name
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  arn            = module.pay.arn
}
resource "aws_lambda_permission" "pay" {
  action        = "lambda:InvokeFunction"
  function_name = module.pay.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.pay.arn
}

resource "aws_cloudwatch_event_rule" "inv" {
  name           = "${local.name}-inv"
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  event_pattern  = jsonencode({ "detail-type" = ["PaymentAuthorized"] })
}
resource "aws_cloudwatch_event_target" "inv" {
  rule           = aws_cloudwatch_event_rule.inv.name
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  arn            = module.inv.arn
}
resource "aws_lambda_permission" "inv" {
  action        = "lambda:InvokeFunction"
  function_name = module.inv.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.inv.arn
}

resource "aws_cloudwatch_event_rule" "saga" {
  name           = "${local.name}-saga"
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  event_pattern  = jsonencode({ "detail-type" = ["InventoryReserved", "InventoryFailed"] })
}
resource "aws_cloudwatch_event_target" "saga" {
  rule           = aws_cloudwatch_event_rule.saga.name
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  arn            = module.saga.arn
}
resource "aws_lambda_permission" "saga" {
  action        = "lambda:InvokeFunction"
  function_name = module.saga.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.saga.arn
}

resource "aws_apigatewayv2_api" "http" {
  name          = "${local.name}-http"
  protocol_type = "HTTP"
}
resource "aws_apigatewayv2_integration" "api" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = module.api.invoke_arn
  payload_format_version = "2.0"
}
resource "aws_apigatewayv2_route" "post" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /orders"
  target    = "integrations/${aws_apigatewayv2_integration.api.id}"
}
resource "aws_apigatewayv2_route" "get" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "GET /orders/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.api.id}"
}
resource "aws_apigatewayv2_route" "tools" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /tools"
  target    = "integrations/${aws_apigatewayv2_integration.api.id}"
}
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
}
resource "aws_lambda_permission" "apigw" {
  action        = "lambda:InvokeFunction"
  function_name = module.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}

output "api_endpoint" { value = aws_apigatewayv2_api.http.api_endpoint }
output "table_name" { value = aws_dynamodb_table.orders.name }
output "bus_name" { value = aws_cloudwatch_event_bus.bus.name }
output "aws_region" { value = var.aws_region }
