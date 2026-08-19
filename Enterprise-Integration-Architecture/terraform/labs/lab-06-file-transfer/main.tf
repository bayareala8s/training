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
      Lab     = "lab-06-file-transfer"
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
  name = "eia-lab06-${random_string.suffix.result}"
}

data "aws_caller_identity" "current" {}

variable "enable_transfer_family" {
  type    = bool
  default = false
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
resource "aws_s3_bucket_versioning" "land" {
  bucket = aws_s3_bucket.land.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_sqs_queue" "q" { name = "${local.name}-val" }
resource "aws_s3_bucket_notification" "n" {
  bucket = aws_s3_bucket.land.id
  queue {
    queue_arn     = aws_sqs_queue.q.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "inbound/"
  }
  depends_on = [aws_sqs_queue_policy.s3]
}
resource "aws_sqs_queue_policy" "s3" {
  queue_url = aws_sqs_queue.q.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "s3.amazonaws.com" }
      Action    = "sqs:SendMessage"
      Resource  = aws_sqs_queue.q.arn
      Condition = {
        ArnEquals    = { "aws:SourceArn" = aws_s3_bucket.land.arn }
        StringEquals = { "aws:SourceAccount" = data.aws_caller_identity.current.account_id }
      }
    }]
  })
}
resource "aws_dynamodb_table" "cat" {
  name         = "${local.name}-catalog"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}
data "archive_file" "fn" {
  type        = "zip"
  output_path = "${path.module}/.build/val.zip"
  source_dir  = "${path.module}/../../../lambda/lab06_validate"
  excludes    = ["__pycache__", "*.pyc"]
}
resource "aws_iam_role" "fn" {
  name = "${local.name}-val"
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
  role = aws_iam_role.fn.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"], Resource = aws_sqs_queue.q.arn },
      { Effect = "Allow", Action = ["s3:GetObject", "s3:PutObject"], Resource = "${aws_s3_bucket.land.arn}/*" },
      { Effect = "Allow", Action = ["dynamodb:PutItem", "dynamodb:GetItem"], Resource = aws_dynamodb_table.cat.arn }
    ]
  })
}
resource "aws_lambda_function" "fn" {
  function_name    = "${local.name}-val"
  role             = aws_iam_role.fn.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.fn.output_path
  source_code_hash = data.archive_file.fn.output_base64sha256
  timeout          = 30
  environment {
    variables = { TABLE_NAME = aws_dynamodb_table.cat.name }
  }
}
resource "aws_lambda_event_source_mapping" "m" {
  event_source_arn = aws_sqs_queue.q.arn
  function_name    = aws_lambda_function.fn.arn
  batch_size       = 1
}
output "bucket" { value = aws_s3_bucket.land.bucket }
output "table_name" { value = aws_dynamodb_table.cat.name }
output "queue_url" { value = aws_sqs_queue.q.url }
output "enable_transfer_family" { value = var.enable_transfer_family }
output "aws_region" { value = var.aws_region }
