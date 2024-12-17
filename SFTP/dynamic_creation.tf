# AWS Provider Configuration
provider "aws" {
  region = "us-east-1"
}

# Fetch DynamoDB Table Data via Local Exec
resource "null_resource" "fetch_dynamodb_data" {
  provisioner "local-exec" {
    command = "aws dynamodb scan --table-name ResourceDefinitions --output json > data.json"
  }
}

# Read DynamoDB Data from File
locals {
  dynamodb_data = jsondecode(file("${path.module}/data.json"))
  s3_resources = [
    for item in local.dynamodb_data.Items :
    {
      resource_id  = item.ResourceID.S
      bucket_name  = jsondecode(item.Configuration.S).BucketName
    }
    if item.ResourceType.S == "S3" && item.Status.S == "Pending"
  ]
}

# Create S3 Buckets Dynamically
resource "aws_s3_bucket" "dynamic_s3_buckets" {
  for_each = { for s3 in local.s3_resources : s3.resource_id => s3 }

  bucket = each.value.bucket_name

  tags = {
    Name        = each.value.bucket_name
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# Outputs for Verification
output "created_s3_buckets" {
  value = [for bucket in aws_s3_bucket.dynamic_s3_buckets : bucket.bucket]
}


aws dynamodb scan --table-name ResourceDefinitions --output json > data.json
