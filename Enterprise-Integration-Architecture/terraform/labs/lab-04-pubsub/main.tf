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
      Lab     = "lab-04-pubsub"
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
  name = "eia-lab04-${random_string.suffix.result}"
}

resource "aws_sns_topic" "orders" {
  name = "${local.name}-orders"
}

resource "aws_sqs_queue" "inv" { name = "${local.name}-inv" }
resource "aws_sqs_queue" "ntf" { name = "${local.name}-ntf" }
resource "aws_sqs_queue" "an" { name = "${local.name}-an" }

resource "aws_sns_topic_subscription" "inv" {
  topic_arn = aws_sns_topic.orders.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.inv.arn
}
resource "aws_sns_topic_subscription" "ntf" {
  topic_arn = aws_sns_topic.orders.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.ntf.arn
}
resource "aws_sns_topic_subscription" "an" {
  topic_arn = aws_sns_topic.orders.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.an.arn
}

resource "aws_sqs_queue_policy" "allow_sns" {
  for_each = {
    inv = aws_sqs_queue.inv
    ntf = aws_sqs_queue.ntf
    an  = aws_sqs_queue.an
  }
  queue_url = each.value.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "sns.amazonaws.com" }
      Action    = "sqs:SendMessage"
      Resource  = each.value.arn
      Condition = { ArnEquals = { "aws:SourceArn" = aws_sns_topic.orders.arn } }
    }]
  })
}

resource "aws_dynamodb_table" "t" {
  name         = "${local.name}-proj"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {
    name = "pk"
    type = "S"
  }
}


data "archive_file" "inv" {
  type        = "zip"
  output_path = "${path.module}/.build/inv.zip"
  source_dir  = "${path.module}/../../../lambda/lab04_inventory"
  excludes    = ["__pycache__", "*.pyc"]
}
resource "aws_iam_role" "inv" {
  name = "${local.name}-inv"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
resource "aws_iam_role_policy" "inv" {
  role = aws_iam_role.inv.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"], Resource = aws_sqs_queue.inv.arn },
      { Effect = "Allow", Action = ["dynamodb:PutItem"], Resource = aws_dynamodb_table.t.arn }
    ]
  })
}
resource "aws_lambda_function" "inv" {
  function_name    = "${local.name}-inv"
  role             = aws_iam_role.inv.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.inv.output_path
  source_code_hash = data.archive_file.inv.output_base64sha256
  timeout          = 15
  environment {
    variables = { TABLE_NAME = aws_dynamodb_table.t.name }
  }
}
resource "aws_lambda_event_source_mapping" "inv" {
  event_source_arn = aws_sqs_queue.inv.arn
  function_name    = aws_lambda_function.inv.arn
  batch_size       = 1
}


data "archive_file" "ntf" {
  type        = "zip"
  output_path = "${path.module}/.build/ntf.zip"
  source_dir  = "${path.module}/../../../lambda/lab04_notify"
  excludes    = ["__pycache__", "*.pyc"]
}
resource "aws_iam_role" "ntf" {
  name = "${local.name}-ntf"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
resource "aws_iam_role_policy" "ntf" {
  role = aws_iam_role.ntf.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"], Resource = aws_sqs_queue.ntf.arn },
      { Effect = "Allow", Action = ["dynamodb:PutItem"], Resource = aws_dynamodb_table.t.arn }
    ]
  })
}
resource "aws_lambda_function" "ntf" {
  function_name    = "${local.name}-ntf"
  role             = aws_iam_role.ntf.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.ntf.output_path
  source_code_hash = data.archive_file.ntf.output_base64sha256
  timeout          = 15
  environment {
    variables = { TABLE_NAME = aws_dynamodb_table.t.name }
  }
}
resource "aws_lambda_event_source_mapping" "ntf" {
  event_source_arn = aws_sqs_queue.ntf.arn
  function_name    = aws_lambda_function.ntf.arn
  batch_size       = 1
}


data "archive_file" "an" {
  type        = "zip"
  output_path = "${path.module}/.build/an.zip"
  source_dir  = "${path.module}/../../../lambda/lab04_analytics"
  excludes    = ["__pycache__", "*.pyc"]
}
resource "aws_iam_role" "an" {
  name = "${local.name}-an"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}
resource "aws_iam_role_policy" "an" {
  role = aws_iam_role.an.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], Resource = "*" },
      { Effect = "Allow", Action = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"], Resource = aws_sqs_queue.an.arn },
      { Effect = "Allow", Action = ["dynamodb:PutItem"], Resource = aws_dynamodb_table.t.arn }
    ]
  })
}
resource "aws_lambda_function" "an" {
  function_name    = "${local.name}-an"
  role             = aws_iam_role.an.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.an.output_path
  source_code_hash = data.archive_file.an.output_base64sha256
  timeout          = 15
  environment {
    variables = { TABLE_NAME = aws_dynamodb_table.t.name }
  }
}
resource "aws_lambda_event_source_mapping" "an" {
  event_source_arn = aws_sqs_queue.an.arn
  function_name    = aws_lambda_function.an.arn
  batch_size       = 1
}


output "topic_arn" { value = aws_sns_topic.orders.arn }
output "table_name" { value = aws_dynamodb_table.t.name }
output "inventory_queue_url" { value = aws_sqs_queue.inv.url }
output "notify_queue_url" { value = aws_sqs_queue.ntf.url }
output "analytics_queue_url" { value = aws_sqs_queue.an.url }
output "aws_region" { value = var.aws_region }
