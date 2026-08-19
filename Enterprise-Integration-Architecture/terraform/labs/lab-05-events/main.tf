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
      Lab     = "lab-05-events"
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
  name = "eia-lab05-${random_string.suffix.result}"
}

resource "aws_cloudwatch_event_bus" "bus" {
  name = "${local.name}-bus"
}
resource "aws_dynamodb_table" "t" {
  name         = "${local.name}-proj"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}

data "archive_file" "pay" {
  type        = "zip"
  output_path = "${path.module}/.build/pay.zip"
  source_dir  = "${path.module}/../../../lambda/lab05_payment"
  excludes    = ["__pycache__", "*.pyc"]
}
resource "aws_iam_role" "pay" {
  name = "${local.name}-pay"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
resource "aws_iam_role_policy" "pay" {
  role = aws_iam_role.pay.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["events:PutEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["dynamodb:PutItem"], Resource = aws_dynamodb_table.t.arn }
    ]
  })
}
resource "aws_lambda_function" "pay" {
  function_name    = "${local.name}-pay"
  role             = aws_iam_role.pay.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.pay.output_path
  source_code_hash = data.archive_file.pay.output_base64sha256
  timeout          = 15
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.t.name
      BUS_NAME   = aws_cloudwatch_event_bus.bus.name
    }
  }
}
resource "aws_cloudwatch_event_rule" "pay" {
  name           = "${local.name}-pay"
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  event_pattern  = jsonencode({ "detail-type" = ["OrderCreated"] })
}
resource "aws_cloudwatch_event_target" "pay" {
  rule           = aws_cloudwatch_event_rule.pay.name
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  arn            = aws_lambda_function.pay.arn
}
resource "aws_lambda_permission" "pay" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pay.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.pay.arn
}


data "archive_file" "inv" {
  type        = "zip"
  output_path = "${path.module}/.build/inv.zip"
  source_dir  = "${path.module}/../../../lambda/lab05_inventory"
  excludes    = ["__pycache__", "*.pyc"]
}
resource "aws_iam_role" "inv" {
  name = "${local.name}-inv"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
resource "aws_iam_role_policy" "inv" {
  role = aws_iam_role.inv.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["events:PutEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["dynamodb:PutItem"], Resource = aws_dynamodb_table.t.arn }
    ]
  })
}
resource "aws_lambda_function" "inv" {
  function_name    = "${local.name}-inv"
  role             = aws_iam_role.inv.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.inv.output_path
  source_code_hash = data.archive_file.inv.output_base64sha256
  timeout          = 15
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.t.name
      BUS_NAME   = aws_cloudwatch_event_bus.bus.name
    }
  }
}
resource "aws_cloudwatch_event_rule" "inv" {
  name           = "${local.name}-inv"
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  event_pattern  = jsonencode({ "detail-type" = ["PaymentAuthorized"] })
}
resource "aws_cloudwatch_event_target" "inv" {
  rule           = aws_cloudwatch_event_rule.inv.name
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  arn            = aws_lambda_function.inv.arn
}
resource "aws_lambda_permission" "inv" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.inv.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.inv.arn
}


data "archive_file" "done" {
  type        = "zip"
  output_path = "${path.module}/.build/done.zip"
  source_dir  = "${path.module}/../../../lambda/lab05_notify"
  excludes    = ["__pycache__", "*.pyc"]
}
resource "aws_iam_role" "done" {
  name = "${local.name}-done"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
resource "aws_iam_role_policy" "done" {
  role = aws_iam_role.done.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["events:PutEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["dynamodb:PutItem"], Resource = aws_dynamodb_table.t.arn }
    ]
  })
}
resource "aws_lambda_function" "done" {
  function_name    = "${local.name}-done"
  role             = aws_iam_role.done.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.done.output_path
  source_code_hash = data.archive_file.done.output_base64sha256
  timeout          = 15
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.t.name
      BUS_NAME   = aws_cloudwatch_event_bus.bus.name
    }
  }
}
resource "aws_cloudwatch_event_rule" "done" {
  name           = "${local.name}-done"
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  event_pattern  = jsonencode({ "detail-type" = ["InventoryReserved"] })
}
resource "aws_cloudwatch_event_target" "done" {
  rule           = aws_cloudwatch_event_rule.done.name
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  arn            = aws_lambda_function.done.arn
}
resource "aws_lambda_permission" "done" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.done.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.done.arn
}

data "archive_file" "order" {
  type        = "zip"
  output_path = "${path.module}/.build/order.zip"
  source_dir  = "${path.module}/../../../lambda/lab05_order"
  excludes    = ["__pycache__", "*.pyc"]
}
resource "aws_iam_role" "order" {
  name = "${local.name}-order"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
resource "aws_iam_role_policy" "order" {
  role = aws_iam_role.order.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["events:PutEvents"], Resource = "*" }
    ]
  })
}
resource "aws_lambda_function" "order" {
  function_name    = "${local.name}-order"
  role             = aws_iam_role.order.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.order.output_path
  source_code_hash = data.archive_file.order.output_base64sha256
  timeout          = 15
  environment {
    variables = { BUS_NAME = aws_cloudwatch_event_bus.bus.name }
  }
}
resource "aws_apigatewayv2_api" "http" {
  name          = "${local.name}-http"
  protocol_type = "HTTP"
}
resource "aws_apigatewayv2_integration" "order" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.order.invoke_arn
  payload_format_version = "2.0"
}
resource "aws_apigatewayv2_route" "post" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /orders"
  target    = "integrations/${aws_apigatewayv2_integration.order.id}"
}
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
}
resource "aws_lambda_permission" "apigw" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.order.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}

output "bus_name" { value = aws_cloudwatch_event_bus.bus.name }
output "table_name" { value = aws_dynamodb_table.t.name }
output "order_function" { value = aws_lambda_function.order.function_name }
output "api_endpoint" { value = aws_apigatewayv2_api.http.api_endpoint }
output "aws_region" { value = var.aws_region }
