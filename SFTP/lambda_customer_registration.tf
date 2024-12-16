# Provider Configuration
provider "aws" {
  region = var.region
}

# Variables
variable "region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "CustomerRegistrationFunction"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  type        = string
  default     = "CustomerRegistration"
}

variable "lambda_role_name" {
  description = "Name of the IAM role for the Lambda function"
  type        = string
  default     = "LambdaDynamoDBRole"
}

# S3 Bucket to Store Lambda Deployment Package
resource "aws_s3_bucket" "lambda_code_bucket" {
  bucket_prefix = "lambda-deployment-bucket"
  acl           = "private"
  tags = {
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# Upload Lambda Function Code to S3
resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.lambda_code_bucket.id
  key    = "lambda_function.zip"
  source = "lambda_function.zip" # Ensure this file exists in the local directory
}

# IAM Role for Lambda Function
resource "aws_iam_role" "lambda_role" {
  name = var.lambda_role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement: [
      {
        Effect    = "Allow",
        Principal = { Service = "lambda.amazonaws.com" },
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

# IAM Policy for Lambda to Access DynamoDB
resource "aws_iam_policy" "dynamodb_access_policy" {
  name        = "DynamoDBAccessPolicy"
  description = "Policy for Lambda to access DynamoDB table"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement: [
      {
        Effect   = "Allow",
        Action   : [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan",
          "dynamodb:Query"
        ],
        Resource : [
          "arn:aws:dynamodb:${var.region}:*:table/${var.dynamodb_table_name}",
          "arn:aws:dynamodb:${var.region}:*:table/${var.dynamodb_table_name}/index/*"
        ]
      }
    ]
  })
}

# Attach Policy to IAM Role
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.dynamodb_access_policy.arn
}

# Lambda Function
resource "aws_lambda_function" "customer_registration_function" {
  function_name = var.function_name
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.9"
  handler       = "lambda_function.lambda_handler"

  # Reference the uploaded code from S3
  s3_bucket        = aws_s3_bucket.lambda_code_bucket.id
  s3_key           = aws_s3_object.lambda_zip.id

  # Environment variables for the table name
  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table_name
    }
  }

  # Tags for organization
  tags = {
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# CloudWatch Log Group for Lambda (Optional)
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.customer_registration_function.function_name}"
  retention_in_days = 7
}

# Outputs
output "lambda_function_name" {
  value       = aws_lambda_function.customer_registration_function.function_name
  description = "The name of the Lambda function"
}

output "lambda_function_arn" {
  value       = aws_lambda_function.customer_registration_function.arn
  description = "The ARN of the Lambda function"
}

output "lambda_role_arn" {
  value       = aws_iam_role.lambda_role.arn
  description = "The ARN of the IAM role used by the Lambda function"
}

output "s3_bucket_name" {
  value       = aws_s3_bucket.lambda_code_bucket.id
  description = "The name of the S3 bucket storing the Lambda code"
}
