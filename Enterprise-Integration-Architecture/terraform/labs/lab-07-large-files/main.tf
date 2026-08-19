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
      Lab     = "lab-07-large-files"
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
  name = "eia-lab07-${random_string.suffix.result}"
}

resource "aws_s3_bucket" "b" {
  bucket        = "${local.name}-up"
  force_destroy = true
}
resource "aws_s3_bucket_public_access_block" "b" {
  bucket                  = aws_s3_bucket.b.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_lifecycle_configuration" "abort" {
  bucket = aws_s3_bucket.b.id
  rule {
    id     = "abort-mpu"
    status = "Enabled"
    abort_incomplete_multipart_upload { days_after_initiation = 1 }
    filter { prefix = "" }
  }
}
resource "aws_dynamodb_table" "jobs" {
  name         = "${local.name}-jobs"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}

data "archive_file" "init" {
  type        = "zip"
  output_path = "${path.module}/.build/init.zip"
  source_dir  = "${path.module}/../../../lambda/lab07_init_upload"
}
resource "aws_iam_role" "init" {
  name = "${local.name}-init"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
resource "aws_iam_role_policy" "init" {
  role = aws_iam_role.init.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:UpdateItem"], Resource = aws_dynamodb_table.jobs.arn },
      { Effect = "Allow", Action = ["s3:PutObject"], Resource = "${aws_s3_bucket.b.arn}/*" }
    ]
  })
}
resource "aws_lambda_function" "init" {
  function_name    = "${local.name}-init"
  role             = aws_iam_role.init.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.init.output_path
  source_code_hash = data.archive_file.init.output_base64sha256
  timeout          = 15
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.jobs.name
      BUCKET     = aws_s3_bucket.b.bucket
    }
  }
}


data "archive_file" "status" {
  type        = "zip"
  output_path = "${path.module}/.build/status.zip"
  source_dir  = "${path.module}/../../../lambda/lab07_status"
}
resource "aws_iam_role" "status" {
  name = "${local.name}-status"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
resource "aws_iam_role_policy" "status" {
  role = aws_iam_role.status.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [

      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:UpdateItem"], Resource = aws_dynamodb_table.jobs.arn }
    ]
  })
}
resource "aws_lambda_function" "status" {
  function_name    = "${local.name}-status"
  role             = aws_iam_role.status.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.status.output_path
  source_code_hash = data.archive_file.status.output_base64sha256
  timeout          = 15
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.jobs.name
    }
  }
}

data "archive_file" "proc" {
  type        = "zip"
  output_path = "${path.module}/.build/proc.zip"
  source_dir  = "${path.module}/../../../lambda/lab07_process"
}
resource "aws_iam_role" "proc" {
  name = "${local.name}-proc"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
resource "aws_iam_role_policy" "proc" {
  role = aws_iam_role.proc.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["s3:GetObject"], Resource = "${aws_s3_bucket.b.arn}/*" },
      { Effect = "Allow", Action = ["dynamodb:UpdateItem", "dynamodb:PutItem"], Resource = aws_dynamodb_table.jobs.arn }
    ]
  })
}
resource "aws_lambda_function" "proc" {
  function_name    = "${local.name}-proc"
  role             = aws_iam_role.proc.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.proc.output_path
  source_code_hash = data.archive_file.proc.output_base64sha256
  timeout          = 60
  environment {
    variables = { TABLE_NAME = aws_dynamodb_table.jobs.name }
  }
}
resource "aws_s3_bucket_notification" "n" {
  bucket = aws_s3_bucket.b.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.proc.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "inbound/"
  }
  depends_on = [aws_lambda_permission.s3]
}
resource "aws_lambda_permission" "s3" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.proc.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.b.arn
}
resource "aws_apigatewayv2_api" "http" {
  name          = "${local.name}-http"
  protocol_type = "HTTP"
}
resource "aws_apigatewayv2_integration" "init" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.init.invoke_arn
  payload_format_version = "2.0"
}
resource "aws_apigatewayv2_integration" "status" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.status.invoke_arn
  payload_format_version = "2.0"
}
resource "aws_apigatewayv2_route" "post" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /uploads"
  target    = "integrations/${aws_apigatewayv2_integration.init.id}"
}
resource "aws_apigatewayv2_route" "get" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "GET /uploads/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.status.id}"
}
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
}
resource "aws_lambda_permission" "apigw_init" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.init.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}
resource "aws_lambda_permission" "apigw_status" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.status.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}
output "api_endpoint" { value = aws_apigatewayv2_api.http.api_endpoint }
output "bucket" { value = aws_s3_bucket.b.bucket }
output "table_name" { value = aws_dynamodb_table.jobs.name }
output "aws_region" { value = var.aws_region }
