terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

variable "project" {
  type        = string
  description = "Project name for resource naming"
}

variable "environment" {
  type        = string
  description = "Environment (dev, staging, prod)"
}

variable "student" {
  type        = string
  description = "Student identifier for tagging"
  default     = "student"
}

variable "data_lake_bucket" {
  type        = string
  description = "S3 data lake bucket name from s3-data-lake module"
}

variable "enable_schedule" {
  type        = bool
  description = "Enable EventBridge schedule (disable to avoid recurring Lambda invocations)"
  default     = false
}

variable "schedule_expression" {
  type        = string
  description = "EventBridge schedule for API ingestion Lambda"
  default     = "rate(15 minutes)"
}

variable "lambda_runtime" {
  type    = string
  default = "python3.11"
}

variable "lambda_memory_mb" {
  type    = number
  default = 512
}

variable "incoming_prefix" {
  type    = string
  default = "incoming/"
}

locals {
  name_prefix = "${var.project}-${var.environment}"
  common_tags = {
    Project     = var.project
    Environment = var.environment
    Student     = var.student
    ManagedBy   = "terraform"
    Course      = "cloud-native-data-engineering"
    Module      = "module-02-ingestion"
  }
  bucket_arn = "arn:aws:s3:::${var.data_lake_bucket}"
  lab_src_root = "${path.module}/../../../modules/module-02-ingestion/labs"
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# -----------------------------------------------------------------------------
# Lambda deployment packages (course lab source)
# -----------------------------------------------------------------------------

data "archive_file" "file_ingest" {
  type        = "zip"
  source_dir  = "${local.lab_src_root}/lab-2.1-lambda-ingestion/src"
  output_path = "${path.module}/build/file_ingest.zip"
}

data "archive_file" "scheduled_ingest" {
  type        = "zip"
  source_dir  = "${local.lab_src_root}/lab-2.2-eventbridge-automation/src"
  output_path = "${path.module}/build/scheduled_ingest.zip"
}

data "archive_file" "s3_event_ingest" {
  type        = "zip"
  source_dir  = "${local.lab_src_root}/lab-2.3-s3-event-processing/src"
  output_path = "${path.module}/build/s3_event_ingest.zip"
}

# -----------------------------------------------------------------------------
# IAM — shared Lambda execution role (least privilege per prefix)
# -----------------------------------------------------------------------------

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ingestion_lambda" {
  name               = "${local.name_prefix}-ingestion-lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
  tags               = local.common_tags
}

data "aws_iam_policy_document" "ingestion_s3" {
  statement {
    sid    = "WriteRawZone"
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:PutObjectTagging",
    ]
    resources = ["${local.bucket_arn}/raw/*"]
  }

  statement {
    sid    = "ReadWriteMetadata"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = ["${local.bucket_arn}/metadata/*"]
  }

  statement {
    sid    = "CopyIncomingToRaw"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = [
      "${local.bucket_arn}/${var.incoming_prefix}*",
      "${local.bucket_arn}/raw/*",
    ]
  }

  statement {
    sid       = "Quarantine"
    effect    = "Allow"
    actions   = ["s3:PutObject"]
    resources = ["${local.bucket_arn}/quarantine/*"]
  }
}

resource "aws_iam_role_policy" "ingestion_s3" {
  name   = "s3-ingestion-paths"
  role   = aws_iam_role.ingestion_lambda.id
  policy = data.aws_iam_policy_document.ingestion_s3.json
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.ingestion_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# -----------------------------------------------------------------------------
# Lab 2.1 — File / record ingestion Lambda
# -----------------------------------------------------------------------------

resource "aws_lambda_function" "file_ingest" {
  function_name = "${local.name_prefix}-file-ingest"
  role          = aws_iam_role.ingestion_lambda.arn
  handler       = "handler.lambda_handler"
  runtime       = var.lambda_runtime
  timeout       = 60
  memory_size   = var.lambda_memory_mb

  filename         = data.archive_file.file_ingest.output_path
  source_code_hash = data.archive_file.file_ingest.output_base64sha256

  environment {
    variables = {
      DATA_LAKE_BUCKET = var.data_lake_bucket
      RAW_PREFIX       = "raw/"
      SOURCE_SYSTEM    = "lambda-ingest"
      DATASET          = "transactions"
    }
  }

  tags = local.common_tags
}

# -----------------------------------------------------------------------------
# Lab 2.2 — EventBridge scheduled API ingestion
# -----------------------------------------------------------------------------

resource "aws_lambda_function" "scheduled_ingest" {
  function_name = "${local.name_prefix}-scheduled-ingest"
  role          = aws_iam_role.ingestion_lambda.arn
  handler       = "scheduled_ingestion.lambda_handler"
  runtime       = var.lambda_runtime
  timeout       = 120
  memory_size   = var.lambda_memory_mb

  filename         = data.archive_file.scheduled_ingest.output_path
  source_code_hash = data.archive_file.scheduled_ingest.output_base64sha256

  environment {
    variables = {
      DATA_LAKE_BUCKET = var.data_lake_bucket
      RAW_PREFIX       = "raw/"
      SOURCE_SYSTEM    = "api-ingest"
      DATASET          = "posts"
      API_URL          = "https://jsonplaceholder.typicode.com/posts"
      WATERMARK_KEY    = "metadata/watermarks/api-ingest/posts.json"
    }
  }

  tags = local.common_tags
}

resource "aws_cloudwatch_event_rule" "scheduled_ingest" {
  count               = var.enable_schedule ? 1 : 0
  name                = "${local.name_prefix}-scheduled-ingest"
  description         = "Module 2 Lab 2.2 — scheduled API ingestion"
  schedule_expression = var.schedule_expression
  tags                = local.common_tags
}

resource "aws_cloudwatch_event_target" "scheduled_ingest" {
  count     = var.enable_schedule ? 1 : 0
  rule      = aws_cloudwatch_event_rule.scheduled_ingest[0].name
  target_id = "ScheduledIngestLambda"
  arn       = aws_lambda_function.scheduled_ingest.arn
}

resource "aws_lambda_permission" "allow_eventbridge_scheduled" {
  count         = var.enable_schedule ? 1 : 0
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.scheduled_ingest.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.scheduled_ingest[0].arn
}

# -----------------------------------------------------------------------------
# Lab 2.3 — S3 event file promotion Lambda
# -----------------------------------------------------------------------------

resource "aws_lambda_function" "s3_event_ingest" {
  function_name = "${local.name_prefix}-s3-event-ingest"
  role          = aws_iam_role.ingestion_lambda.arn
  handler       = "s3_event_handler.lambda_handler"
  runtime       = var.lambda_runtime
  timeout       = 60
  memory_size   = var.lambda_memory_mb

  filename         = data.archive_file.s3_event_ingest.output_path
  source_code_hash = data.archive_file.s3_event_ingest.output_base64sha256

  environment {
    variables = {
      DATA_LAKE_BUCKET  = var.data_lake_bucket
      INCOMING_PREFIX   = var.incoming_prefix
      RAW_PREFIX        = "raw/"
      QUARANTINE_PREFIX = "quarantine/"
      SOURCE_SYSTEM     = "file-upload"
      DATASET           = "transactions"
      MAX_FILE_BYTES    = "10485760"
      ALLOWED_SUFFIXES  = ".csv,.json,.jsonl"
    }
  }

  tags = local.common_tags
}

resource "aws_lambda_permission" "allow_s3_invoke" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_event_ingest.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = local.bucket_arn
  source_account = data.aws_caller_identity.current.account_id
}

resource "aws_s3_bucket_notification" "incoming_lambda" {
  bucket = var.data_lake_bucket

  lambda_function {
    lambda_function_arn = aws_lambda_function.s3_event_ingest.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = var.incoming_prefix
  }

  depends_on = [aws_lambda_permission.allow_s3_invoke]
}

# Ensure incoming/ prefix exists for lab uploads
resource "aws_s3_object" "incoming_prefix" {
  bucket  = var.data_lake_bucket
  key     = var.incoming_prefix
  content = ""
}

# -----------------------------------------------------------------------------
# Outputs
# -----------------------------------------------------------------------------

output "file_ingest_function_name" {
  value = aws_lambda_function.file_ingest.function_name
}

output "scheduled_ingest_function_name" {
  value = aws_lambda_function.scheduled_ingest.function_name
}

output "s3_event_ingest_function_name" {
  value = aws_lambda_function.s3_event_ingest.function_name
}

output "ingestion_lambda_role_arn" {
  value = aws_iam_role.ingestion_lambda.arn
}

output "eventbridge_rule_name" {
  value = var.enable_schedule ? aws_cloudwatch_event_rule.scheduled_ingest[0].name : null
}

output "lambda_function_names" {
  value = [
    aws_lambda_function.file_ingest.function_name,
    aws_lambda_function.scheduled_ingest.function_name,
    aws_lambda_function.s3_event_ingest.function_name,
  ]
}
