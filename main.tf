provider "aws" {
  region = "us-east-1"
}

variable "config_file" {
  description = "Path to the JSON configuration file"
  default     = "config.json"
}

data "local_file" "config" {
  filename = var.config_file
}

locals {
  config = jsondecode(data.local_file.config.content)
}

resource "aws_s3_bucket" "source" {
  bucket = local.config["source_bucket"]
}

resource "aws_s3_bucket" "target" {
  bucket = local.config["target_bucket"]
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_s3_file_copy_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda_s3_file_copy_policy"
  description = "Policy for Lambda to access S3 buckets"
  policy      = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ],
        Resource = [
          "arn:aws:s3:::${local.config["source_bucket"]}/*",
          "arn:aws:s3:::${local.config["target_bucket"]}/*"
        ]
      },
      {
        Effect = "Allow",
        Action = "logs:CreateLogGroup",
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

resource "aws_lambda_function" "file_copy_lambda" {
  function_name = local.config["lambda_function"]["name"]
  runtime       = local.config["lambda_function"]["runtime"]
  handler       = "lambda_function.lambda_handler"
  role          = aws_iam_role.lambda_role.arn

  filename      = "lambda_function.zip"
  timeout       = local.config["lambda_function"]["timeout"]
  memory_size   = local.config["lambda_function"]["memory_size"]

  environment {
    variables = {
      CONFIG = jsonencode(local.config)
    }
  }
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = local.config["cloudwatch_logs"]["log_group"]
  retention_in_days = local.config["cloudwatch_logs"]["retention_days"]
}
