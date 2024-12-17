# AWS Provider Configuration
provider "aws" {
  region = "us-east-1"
}

# Fetch DynamoDB Data using Local Exec
resource "null_resource" "fetch_dynamodb_data" {
  provisioner "local-exec" {
    command = "aws dynamodb scan --table-name ResourceDefinitions --output json > data.json"
  }

  triggers = {
    always_run = timestamp()
  }
}

# Use a default fallback if the file does not yet exist
locals {
  dynamodb_data = fileexists("${path.module}/data.json") ? jsondecode(file("${path.module}/data.json")) : { Items = [] }

  s3_resources = [
    for item in local.dynamodb_data.Items :
    {
      resource_id = item.ResourceID.S
      bucket_name = jsondecode(item.Configuration.S).BucketName
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

  depends_on = [null_resource.fetch_dynamodb_data]
}

# Outputs
output "created_s3_buckets" {
  description = "List of S3 buckets created dynamically"
  value       = [for bucket in aws_s3_bucket.dynamic_s3_buckets : bucket.bucket]
}
