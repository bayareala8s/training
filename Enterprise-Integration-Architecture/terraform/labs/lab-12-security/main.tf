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
      Lab     = "lab-12-security"
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
  name = "eia-lab12-${random_string.suffix.result}"
}

variable "insecure" {
  type    = bool
  default = true
}
resource "aws_s3_bucket" "b" {
  bucket        = "${local.name}-data"
  force_destroy = true
}
resource "aws_s3_bucket_public_access_block" "b" {
  bucket                  = aws_s3_bucket.b.id
  block_public_acls       = !var.insecure
  block_public_policy     = !var.insecure
  ignore_public_acls      = !var.insecure
  restrict_public_buckets = !var.insecure
}
resource "aws_dynamodb_table" "t" {
  name         = "${local.name}-t"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}
data "archive_file" "fn" {
  type        = "zip"
  output_path = "${path.module}/.build/fix.zip"
  source_dir  = "${path.module}/../../../lambda/lab12_fix"
}
resource "aws_iam_role" "fn" {
  name = "${local.name}-fn"
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
  policy = var.insecure ? jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = ["dynamodb:*", "s3:*", "logs:*"], Resource = "*" }]
    }) : jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["dynamodb:GetItem", "dynamodb:PutItem"], Resource = aws_dynamodb_table.t.arn },
      { Effect = "Allow", Action = ["s3:GetObject"], Resource = "${aws_s3_bucket.b.arn}/allowed/*" }
    ]
  })
}
resource "aws_lambda_function" "fn" {
  function_name    = "${local.name}-fn"
  role             = aws_iam_role.fn.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.fn.output_path
  source_code_hash = data.archive_file.fn.output_base64sha256
}
output "insecure" { value = var.insecure }
output "bucket" { value = aws_s3_bucket.b.bucket }
output "function_name" { value = aws_lambda_function.fn.function_name }
output "function_role_name" { value = aws_iam_role.fn.name }
output "table_name" { value = aws_dynamodb_table.t.name }
output "aws_region" { value = var.aws_region }
