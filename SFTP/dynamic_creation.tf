# AWS Provider Configuration
provider "aws" {
  region = "us-east-1" # Replace with your desired region
}

# Variables for DynamoDB Table Name
variable "dynamodb_table_name" {
  description = "The name of the DynamoDB table storing resource definitions"
  type        = string
  default     = "ResourceDefinitions"
}

# Fetch Items from DynamoDB Table
data "aws_dynamodb_table_items" "resource_definitions" {
  table_name = var.dynamodb_table_name
}

# Parse DynamoDB Items for S3 Resources
locals {
  s3_resources = [
    for item in data.aws_dynamodb_table_items.resource_definitions.items :
    {
      resource_id = item["ResourceID"]
      configuration = jsondecode(item["Configuration"])
    }
    if item["ResourceType"] == "S3" && item["Status"] == "Pending"
  ]
}

# Dynamically Create S3 Buckets
resource "aws_s3_bucket" "dynamic_s3_buckets" {
  for_each = { for s3 in local.s3_resources : s3.resource_id => s3 }

  bucket = each.value.configuration.BucketName

  # Example: Enable versioning
  versioning {
    enabled = true
  }

  tags = {
    Name        = each.value.configuration.BucketName
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# Outputs for Verification
output "s3_bucket_names" {
  value       = [for bucket in aws_s3_bucket.dynamic_s3_buckets : bucket.bucket]
  description = "List of S3 buckets created dynamically from DynamoDB"
}
