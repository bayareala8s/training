terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.50"
    }
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.4"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project = "baylearn-eia"
      Lab     = "lab-13-observability"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-west-2"
}

resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

locals {
  name = "eia-lab13-${random_string.suffix.result}"
}

data "archive_file" "fn" {
  type        = "zip"
  output_path = "${path.module}/.build/met.zip"
  source_dir  = "${path.module}/../../../lambda/lab13_metrics"
}
resource "aws_iam_role" "fn" {
  name = "${local.name}-met"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
resource "aws_iam_role_policy" "fn" {
  role = aws_iam_role.fn.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["cloudwatch:PutMetricData"], Resource = "*" }
    ]
  })
}
resource "aws_lambda_function" "fn" {
  function_name    = "${local.name}-met"
  role             = aws_iam_role.fn.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.fn.output_path
  source_code_hash = data.archive_file.fn.output_base64sha256
  environment {
    variables = { METRIC_NS = "EIA/Lab13" }
  }
}
resource "aws_cloudwatch_dashboard" "d" {
  dashboard_name = "${local.name}-ops"
  dashboard_body = jsonencode({
    widgets = [
      { "type" : "metric", "x" : 0, "y" : 0, "width" : 8, "height" : 6, "properties" : { "title" : "Transactions", "metrics" : [["EIA/Lab13", "Transactions"]], "region" : var.aws_region, "stat" : "Sum", "period" : 60 } },
      { "type" : "metric", "x" : 8, "y" : 0, "width" : 8, "height" : 6, "properties" : { "title" : "Success vs Failure", "metrics" : [["EIA/Lab13", "Success"], ["EIA/Lab13", "Failure"]], "region" : var.aws_region, "stat" : "Sum", "period" : 60 } },
      { "type" : "metric", "x" : 16, "y" : 0, "width" : 8, "height" : 6, "properties" : { "title" : "Latency (ms)", "metrics" : [["EIA/Lab13", "LatencyMs"]], "region" : var.aws_region, "stat" : "Average", "period" : 60 } },
      { "type" : "metric", "x" : 0, "y" : 6, "width" : 8, "height" : 6, "properties" : { "title" : "Queue depth", "metrics" : [["EIA/Lab13", "QueueDepth"]], "region" : var.aws_region, "stat" : "Maximum", "period" : 60 } },
      { "type" : "metric", "x" : 8, "y" : 6, "width" : 8, "height" : 6, "properties" : { "title" : "DLQ", "metrics" : [["EIA/Lab13", "DLQVisible"]], "region" : var.aws_region, "stat" : "Maximum", "period" : 60 } },
      { "type" : "metric", "x" : 16, "y" : 6, "width" : 8, "height" : 6, "properties" : { "title" : "File counts", "metrics" : [["EIA/Lab13", "FileCounts"]], "region" : var.aws_region, "stat" : "Sum", "period" : 60 } },
      { "type" : "metric", "x" : 0, "y" : 12, "width" : 8, "height" : 6, "properties" : { "title" : "Processing duration (ms)", "metrics" : [["EIA/Lab13", "ProcessingDurationMs"]], "region" : var.aws_region, "stat" : "Average", "period" : 60 } }
    ]
  })
}
output "function_name" { value = aws_lambda_function.fn.function_name }
output "dashboard_name" { value = aws_cloudwatch_dashboard.d.dashboard_name }
output "aws_region" { value = var.aws_region }
