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
      Capstone = "manufacturing"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-west-2"
}

data "aws_caller_identity" "current" {}

resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

locals {
  name = "eia-mfg-${random_string.suffix.result}"
}

resource "aws_dynamodb_table" "suppliers" {
  name         = "${local.name}-sup"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}
resource "aws_dynamodb_table" "catalog" {
  name         = "${local.name}-cat"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}
resource "aws_dynamodb_table" "approvals" {
  name         = "${local.name}-appr"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}

resource "aws_dynamodb_table_item" "ship" {
  table_name = aws_dynamodb_table.suppliers.name
  hash_key   = "pk"
  item = jsonencode({
    pk         = { S = "SHIP#92841" }
    shipmentId = { S = "92841" }
    status     = { S = "DELAYED" }
    reason     = { S = "supplier-file-missing" }
    supplier   = { S = "BOLTCO" }
  })
}

resource "aws_s3_bucket" "land" {
  bucket        = "${local.name}-land"
  force_destroy = true
}
resource "aws_s3_bucket_public_access_block" "land" {
  bucket                  = aws_s3_bucket.land.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
resource "aws_sqs_queue" "files" { name = "${local.name}-files" }
resource "aws_sqs_queue_policy" "files" {
  queue_url = aws_sqs_queue.files.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "s3.amazonaws.com" }
      Action    = "sqs:SendMessage"
      Resource  = aws_sqs_queue.files.arn
      Condition = {
        ArnEquals    = { "aws:SourceArn" = aws_s3_bucket.land.arn }
        StringEquals = { "aws:SourceAccount" = data.aws_caller_identity.current.account_id }
      }
    }]
  })
}
resource "aws_s3_bucket_notification" "n" {
  bucket = aws_s3_bucket.land.id
  queue {
    queue_arn     = aws_sqs_queue.files.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "inbound/"
  }
  depends_on = [aws_sqs_queue_policy.files]
}

module "api" {
  source     = "../../modules/lambda_from_dir"
  name       = "${local.name}-api"
  source_dir = "${path.module}/../../../lambda/cap_mfg_api"
  build_path = "${path.module}/.build"
  environment = {
    SUPPLIERS_TABLE    = aws_dynamodb_table.suppliers.name
    CATALOG_TABLE      = aws_dynamodb_table.catalog.name
    APPROVAL_TABLE     = aws_dynamodb_table.approvals.name
    EXPECTED_SUPPLIERS = "ACME,BOLTCO,YIELD"
  }
  policy_json = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:UpdateItem"], Resource = [aws_dynamodb_table.suppliers.arn, aws_dynamodb_table.catalog.arn, aws_dynamodb_table.approvals.arn] }
    ]
  })
}

module "files" {
  source      = "../../modules/lambda_from_dir"
  name        = "${local.name}-files"
  source_dir  = "${path.module}/../../../lambda/cap_mfg_files"
  build_path  = "${path.module}/.build"
  timeout     = 30
  environment = { CATALOG_TABLE = aws_dynamodb_table.catalog.name }
  policy_json = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"], Resource = aws_sqs_queue.files.arn },
      { Effect = "Allow", Action = ["s3:GetObject"], Resource = "${aws_s3_bucket.land.arn}/*" },
      { Effect = "Allow", Action = ["dynamodb:PutItem"], Resource = aws_dynamodb_table.catalog.arn }
    ]
  })
}
resource "aws_lambda_event_source_mapping" "files" {
  event_source_arn = aws_sqs_queue.files.arn
  function_name    = module.files.arn
  batch_size       = 1
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
resource "aws_apigatewayv2_route" "missing" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "GET /suppliers/missing"
  target    = "integrations/${aws_apigatewayv2_integration.api.id}"
}
resource "aws_apigatewayv2_route" "ship" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "GET /shipments/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.api.id}"
}
resource "aws_apigatewayv2_route" "tools" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /tools"
  target    = "integrations/${aws_apigatewayv2_integration.api.id}"
}
resource "aws_apigatewayv2_route" "approve" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /approve"
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
output "bucket" { value = aws_s3_bucket.land.bucket }
output "catalog_table" { value = aws_dynamodb_table.catalog.name }
output "aws_region" { value = var.aws_region }
