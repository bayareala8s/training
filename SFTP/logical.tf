provider "aws" {
  region = "us-east-1" # Replace with your preferred region
}

# DynamoDB table metadata
data "aws_dynamodb_table" "example_table" {
  name = "YourDynamoDBTableName" # Replace with your DynamoDB table name
}

# Define the key(s) to retrieve specific items
locals {
  keys = [
    {
      primary_key = "PrimaryKey1" # Replace with your table's primary key value
      sort_key    = "SortKey1"    # Replace with your table's sort key value (if applicable)
    },
    {
      primary_key = "PrimaryKey2" # Another example key
      sort_key    = "SortKey2"
    }
  ]
}

# Fetch specific attributes using AWS CLI and process output with PowerShell
resource "null_resource" "fetch_dynamodb_attributes" {
  for_each = tomap({
    for i, key in local.keys : "${i}" => key
  })

  provisioner "local-exec" {
    command = <<EOT
      aws dynamodb get-item `
        --table-name ${data.aws_dynamodb_table.example_table.name} `
        --key "{\\"PrimaryKey\\": {\\"S\\": \\"${each.value.primary_key}\\"}, \\"SortKey\\": {\\"S\\": \\"${each.value.sort_key}\\"}}" `
        --projection-expression "Attribute1, Attribute2" `
        --region us-east-1 `
        --output json | PowerShell -Command "Get-Content - | ConvertFrom-Json | Select-Object -ExpandProperty Item"
    EOT
  }
}

# Output the table's basic metadata for debugging
output "table_info" {
  value = {
    table_name = data.aws_dynamodb_table.example_table.name
    arn        = data.aws_dynamodb_table.example_table.arn
  }
}
