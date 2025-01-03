provider "aws" {
  region = var.aws_region
}

# Fetch the DynamoDB table
data "aws_dynamodb_table" "lambda_config_table" {
  name = var.dynamodb_table_name
}

# Fetch all items in the DynamoDB table
data "aws_dynamodb_table_items" "lambda_configs" {
  table_name = data.aws_dynamodb_table.lambda_config_table.name
}

# Create Lambda functions dynamically
resource "aws_lambda_function" "dynamic_lambdas" {
  for_each = { for item in data.aws_dynamodb_table_items.lambda_configs.items : item["FunctionName"] => item }

  function_name = each.value["FunctionName"]
  runtime       = each.value["Runtime"]
  role          = each.value["RoleArn"]
  handler       = each.value["Handler"]

  s3_bucket = each.value["CodeS3Bucket"]
  s3_key    = each.value["CodeS3Key"]

  # Environment variables (optional)
  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table_name
    }
  }
}
