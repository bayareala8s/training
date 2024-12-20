# AWS Provider Configuration
provider "aws" {
  region = "us-east-1"
}

# Fetch DynamoDB Data via Local Exec
resource "null_resource" "fetch_dynamodb_data" {
  provisioner "local-exec" {
    command = <<EOT
      aws dynamodb scan \
      --table-name ResourceDefinitions \
      --projection-expression "ResourceID, ResourceType, Configuration, Status" \
      --output json > data.json
    EOT
  }

  triggers = {
    always_run = timestamp()
  }
}

# Parse DynamoDB Data
locals {
  dynamodb_data = fileexists("${path.module}/data.json") ? jsondecode(file("${path.module}/data.json")) : { Items = [] }

  # Filter S3 resources
  s3_resources = [
    for item in local.dynamodb_data.Items :
    {
      resource_id = item["ResourceID"]["S"]
      bucket_name = jsondecode(item["Configuration"]["S"]).BucketName
    }
    if item["ResourceType"]["S"] == "S3" && item["Status"]["S"] == "Pending"
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

# Debug Outputs
output "debug_s3_resources" {
  value = local.s3_resources
}

# Output Created Buckets
output "created_s3_buckets" {
  value = [for bucket in aws_s3_bucket.dynamic_s3_buckets : bucket.bucket]
}
