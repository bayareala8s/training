# Define variables for customization
variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table for customer registration"
  type        = string
  default     = "CustomerRegistration"
}

# DynamoDB table definition
resource "aws_dynamodb_table" "customer_registration" {
  name           = var.dynamodb_table_name
  billing_mode   = "PAY_PER_REQUEST" # On-demand pricing
  hash_key       = "CustomerID"      # Primary key
  range_key      = "Email"           # Sort key (optional for better query structure)

  # Define attributes
  attribute {
    name = "CustomerID"
    type = "S" # S = String
  }

  attribute {
    name = "Email"
    type = "S" # S = String
  }

  attribute {
    name = "SourceBucket"
    type = "S" # S = String
  }

  attribute {
    name = "DestinationBucket"
    type = "S" # S = String
  }

  attribute {
    name = "DateCreated"
    type = "S" # S = String (ISO8601 timestamp format)
  }

  # Global secondary index for email-based queries
  global_secondary_index {
    name            = "EmailIndex"
    hash_key        = "Email"
    projection_type = "ALL"
  }

  # Point-in-time recovery for data protection
  point_in_time_recovery {
    enabled = true
  }

  # Server-side encryption
  server_side_encryption {
    enabled = true
  }

  # Table tags
  tags = {
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# IAM Role for Lambda to access DynamoDB (optional, if integrating with a Lambda function)
resource "aws_iam_role" "dynamodb_lambda_role" {
  name = "dynamodb_lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# IAM Policy for Lambda to read/write to the DynamoDB table
resource "aws_iam_policy" "dynamodb_access_policy" {
  name        = "DynamoDBAccessPolicy"
  description = "Policy for Lambda to access DynamoDB table"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          "arn:aws:dynamodb:${var.region}:${var.account_id}:table/${aws_dynamodb_table.customer_registration.name}",
          "arn:aws:dynamodb:${var.region}:${var.account_id}:table/${aws_dynamodb_table.customer_registration.name}/index/*"
        ]
      }
    ]
  })
}

# Attach policy to IAM role
resource "aws_iam_role_policy_attachment" "attach_dynamodb_policy" {
  role       = aws_iam_role.dynamodb_lambda_role.name
  policy_arn = aws_iam_policy.dynamodb_access_policy.arn
}

# Output the table name for verification
output "dynamodb_table_name" {
  value       = aws_dynamodb_table.customer_registration.name
  description = "The name of the DynamoDB table for customer registration"
}

# Output the ARN of the table
output "dynamodb_table_arn" {
  value       = aws_dynamodb_table.customer_registration.arn
  description = "The ARN of the DynamoDB table for customer registration"
}
