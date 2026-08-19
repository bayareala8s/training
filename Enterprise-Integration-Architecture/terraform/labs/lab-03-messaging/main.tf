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
      Lab     = "lab-03-messaging"
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
  name = "eia-lab03-${random_string.suffix.result}"
}

resource "aws_sqs_queue" "dlq" {
  name                      = "${local.name}-dlq"
  message_retention_seconds = 86400
}

resource "aws_sqs_queue" "work" {
  name                       = "${local.name}-work"
  visibility_timeout_seconds = 10
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 2
  })
}

resource "aws_dynamodb_table" "t" {
  name         = "${local.name}-posted"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}

data "archive_file" "fn" {
  type        = "zip"
  output_path = "${path.module}/.build/consumer.zip"
  source_dir  = "${path.module}/../../../lambda/lab03_consumer"
  excludes    = ["__pycache__", "*.pyc"]
}

resource "aws_iam_role" "fn" {
  name = "${local.name}-role"
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
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"]
        Resource = aws_sqs_queue.work.arn
      },
      {
        Effect   = "Allow"
        Action   = ["dynamodb:PutItem"]
        Resource = aws_dynamodb_table.t.arn
      }
    ]
  })
}

resource "aws_lambda_function" "c" {
  function_name    = "${local.name}-consumer"
  role             = aws_iam_role.fn.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.fn.output_path
  source_code_hash = data.archive_file.fn.output_base64sha256
  timeout          = 8
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.t.name
    }
  }
}

resource "aws_lambda_event_source_mapping" "m" {
  event_source_arn = aws_sqs_queue.work.arn
  function_name    = aws_lambda_function.c.arn
  batch_size       = 1
}

output "queue_url" { value = aws_sqs_queue.work.url }
output "dlq_url" { value = aws_sqs_queue.dlq.url }
output "table_name" { value = aws_dynamodb_table.t.name }
output "function_name" { value = aws_lambda_function.c.function_name }
output "aws_region" { value = var.aws_region }
