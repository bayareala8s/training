# AWS Provider Configuration
provider "aws" {
  region = "us-east-1" # Replace with your AWS region
}

# Variables for Table Name and Region
variable "table_name" {
  description = "The name of the DynamoDB table"
  type        = string
  default     = "ResourceDefinitions"
}

# DynamoDB Table Creation
resource "aws_dynamodb_table" "resource_definitions" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST" # On-demand billing mode
  hash_key     = "ResourceID"      # Partition key

  # Define Attributes
  attribute {
    name = "ResourceID"
    type = "S" # String type
  }

  attribute {
    name = "ResourceType"
    type = "S" # String type
  }

  attribute {
    name = "Status"
    type = "S" # String type
  }

  attribute {
    name = "Configuration"
    type = "S" # String type for storing JSON or other structured data
  }

  # Optional: Add a Global Secondary Index (GSI) for ResourceType
  global_secondary_index {
    name               = "ResourceTypeIndex"
    hash_key           = "ResourceType"
    projection_type    = "ALL"
  }

  # Optional: Add a GSI for querying by Status
  global_secondary_index {
    name               = "StatusIndex"
    hash_key           = "Status"
    projection_type    = "ALL"
  }

  # Enable Point-in-Time Recovery for data protection
  point_in_time_recovery {
    enabled = true
  }

  # Table Tags for Organization
  tags = {
    Name        = var.table_name
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# Outputs for Verification
output "dynamodb_table_name" {
  value       = aws_dynamodb_table.resource_definitions.name
  description = "The name of the created DynamoDB table"
}

output "dynamodb_table_arn" {
  value       = aws_dynamodb_table.resource_definitions.arn
  description = "The ARN of the DynamoDB table"
}

output "global_secondary_indexes" {
  value       = aws_dynamodb_table.resource_definitions.global_secondary_indexes[*].name
  description = "The names of the GSIs for querying the table"
}
