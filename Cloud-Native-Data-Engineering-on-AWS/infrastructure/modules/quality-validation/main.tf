terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

variable "project" {
  type = string
}

variable "environment" {
  type = string
}

variable "student" {
  type    = string
  default = "student"
}

variable "data_lake_bucket" {
  type = string
}

locals {
  name_prefix = "${var.project}-${var.environment}"
  common_tags = {
    Project     = var.project
    Environment = var.environment
    Student     = var.student
    ManagedBy   = "terraform"
    Course      = "cloud-native-data-engineering"
    Module      = "quality-validation"
  }
}

data "archive_file" "validation_lambda" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/build/validation.zip"
  excludes    = ["__pycache__", "*.pyc"]
}

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "validation" {
  name               = "${local.name_prefix}-quality-validation"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
  tags               = local.common_tags
}

resource "aws_iam_role_policy_attachment" "basic" {
  role       = aws_iam_role.validation.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "validation" {
  function_name = "${local.name_prefix}-quality-validation"
  role          = aws_iam_role.validation.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 256

  filename         = data.archive_file.validation_lambda.output_path
  source_code_hash = data.archive_file.validation_lambda.output_base64sha256

  environment {
    variables = {
      DATA_LAKE_BUCKET = var.data_lake_bucket
      PASS_RATE        = "100"
      PASS_RATE_SLO    = "0"
    }
  }

  tags = local.common_tags
}

output "validation_lambda_arn" {
  value = aws_lambda_function.validation.arn
}

output "validation_lambda_name" {
  value = aws_lambda_function.validation.function_name
}
