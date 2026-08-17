provider "aws" {
  region = "us-east-1"
}

variable "config_file" {
  description = "Path to the JSON configuration file"
  default     = "config.json"
}

# Read JSON Configuration
data "local_file" "config" {
  filename = var.config_file
}

locals {
  config = jsondecode(data.local_file.config.content)
}

# Create Source Bucket
resource "aws_s3_bucket" "source" {
  bucket = local.config["source_bucket"]
}

# Create Target Bucket
resource "aws_s3_bucket" "target" {
  bucket = local.config["target_bucket"]
}

# Create IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda_s3_file_copy_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

# Create IAM Policy for Lambda
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

# Attach IAM Policy to Role
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# Create Lambda Function
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

# Create CloudWatch Log Group
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = local.config["cloudwatch_logs"]["log_group"]
  retention_in_days = local.config["cloudwatch_logs"]["retention_days"]
}

# Lambda Permission for S3 Trigger
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.file_copy_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.source.arn
}

# S3 Event Notification for Lambda Trigger
resource "aws_s3_bucket_notification" "s3_trigger" {
  bucket = aws_s3_bucket.source.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.file_copy_lambda.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3]
}
