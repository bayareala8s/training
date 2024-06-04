variable "region" {
  description = "The AWS region to create resources in."
  default     = "us-west-2"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function."
  default     = "MobileAppBackendFunction"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table."
  default     = "MobileAppBackendTable"
}

variable "api_gateway_name" {
  description = "Name of the API Gateway."
  default     = "MobileAppBackendAPI"
}
