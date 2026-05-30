terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# ------------------------------------------------------------------------------
# Variables
# ------------------------------------------------------------------------------

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

variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}

variable "bucket_name" {
  type        = string
  description = "S3 data lake bucket name"
}

variable "glue_job_name" {
  type        = string
  description = "Glue ETL job name to orchestrate (from glue-etl module)"
}

variable "validation_lambda_arn" {
  type        = string
  description = "ARN of quality validation Lambda (Lab 4.2 or placeholder)"
  default     = ""
}

variable "sns_topic_arn" {
  type        = string
  description = "SNS topic ARN for failure notifications (Lab 6.3)"
  default     = ""
}

variable "schedule_expression" {
  type        = string
  description = "EventBridge schedule for daily pipeline (UTC)"
  default     = "cron(0 6 * * ? *)"
}

variable "enable_schedule" {
  type        = bool
  description = "Enable EventBridge schedule (disable in dev to save costs)"
  default     = false
}

variable "state_machine_definition_path" {
  type        = string
  description = "Path to ASL JSON file relative to module root"
  default     = ""
}

# ------------------------------------------------------------------------------
# Locals
# ------------------------------------------------------------------------------

locals {
  state_machine_name = "${var.project}-${var.environment}-daily-etl"
  execution_role_name = "${var.project}-${var.environment}-sfn-etl-role"
  event_rule_name     = "${var.project}-${var.environment}-daily-etl-schedule"

  # Default ASL when external file not provided
  default_definition = templatefile("${path.module}/templates/daily_etl.asl.json.tpl", {
    glue_job_name           = var.glue_job_name
    validation_lambda_arn   = var.validation_lambda_arn != "" ? var.validation_lambda_arn : "arn:aws:lambda:${var.aws_region}:000000000000:function:placeholder-validation"
    sns_topic_arn           = var.sns_topic_arn != "" ? var.sns_topic_arn : "arn:aws:sns:${var.aws_region}:000000000000:placeholder-topic"
    pass_rate_threshold     = 99.9
  })

  state_machine_definition = var.state_machine_definition_path != "" ? file(var.state_machine_definition_path) : local.default_definition

  common_tags = {
    Project     = var.project
    Environment = var.environment
    Student     = var.student
    ManagedBy   = "terraform"
    Course      = "cloud-native-data-engineering"
    Module      = "module-06-orchestration"
  }
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# ------------------------------------------------------------------------------
# IAM — Step Functions execution role
# ------------------------------------------------------------------------------

data "aws_iam_policy_document" "sfn_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["states.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "sfn_execution" {
  name               = local.execution_role_name
  assume_role_policy = data.aws_iam_policy_document.sfn_assume_role.json
  tags               = local.common_tags
}

data "aws_iam_policy_document" "sfn_execution" {
  statement {
    sid    = "GlueJobRun"
    effect = "Allow"
    actions = [
      "glue:StartJobRun",
      "glue:GetJobRun",
      "glue:GetJobRuns",
      "glue:BatchStopJobRun",
    ]
    resources = ["*"]
  }

  statement {
    sid    = "LambdaInvoke"
    effect = "Allow"
    actions = [
      "lambda:InvokeFunction",
    ]
    resources = var.validation_lambda_arn != "" ? [var.validation_lambda_arn] : ["arn:aws:lambda:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:function:*"]
  }

  dynamic "statement" {
    for_each = var.sns_topic_arn != "" ? [1] : []
    content {
      sid    = "SNSPublish"
      effect = "Allow"
      actions = [
        "sns:Publish",
      ]
      resources = [var.sns_topic_arn]
    }
  }

  statement {
    sid    = "CloudWatchLogs"
    effect = "Allow"
    actions = [
      "logs:CreateLogDelivery",
      "logs:GetLogDelivery",
      "logs:UpdateLogDelivery",
      "logs:DeleteLogDelivery",
      "logs:ListLogDeliveries",
      "logs:PutResourcePolicy",
      "logs:DescribeResourcePolicies",
      "logs:DescribeLogGroups",
    ]
    resources = ["*"]
  }

  statement {
    sid    = "S3PipelineMetadata"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::${var.bucket_name}",
      "arn:aws:s3:::${var.bucket_name}/metadata/pipeline-runs/*",
    ]
  }

  statement {
    sid    = "EventBridgeManagedRule"
    effect = "Allow"
    actions = [
      "events:PutTargets",
      "events:PutRule",
      "events:DescribeRule",
    ]
    resources = ["arn:aws:events:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:rule/StepFunctionsGetEventsForStepFunctionsExecutionRule"]
  }
}

resource "aws_iam_role_policy" "sfn_execution" {
  name   = "${local.execution_role_name}-policy"
  role   = aws_iam_role.sfn_execution.id
  policy = data.aws_iam_policy_document.sfn_execution.json
}

# ------------------------------------------------------------------------------
# CloudWatch Log Group for Step Functions
# ------------------------------------------------------------------------------

resource "aws_cloudwatch_log_group" "sfn" {
  name              = "/aws/vendedlogs/states/${local.state_machine_name}"
  retention_in_days = 14
  tags              = local.common_tags
}

# ------------------------------------------------------------------------------
# Step Functions State Machine
# ------------------------------------------------------------------------------

resource "aws_sfn_state_machine" "daily_etl" {
  name     = local.state_machine_name
  role_arn = aws_iam_role.sfn_execution.arn
  type     = "STANDARD"

  definition = local.state_machine_definition

  logging_configuration {
    log_destination        = "${aws_cloudwatch_log_group.sfn.arn}:*"
    include_execution_data = true
    level                  = "ALL"
  }

  tags = local.common_tags

  depends_on = [aws_iam_role_policy.sfn_execution]
}

# ------------------------------------------------------------------------------
# EventBridge Schedule (optional)
# ------------------------------------------------------------------------------

resource "aws_cloudwatch_event_rule" "daily_etl" {
  count               = var.enable_schedule ? 1 : 0
  name                = local.event_rule_name
  description         = "Trigger daily ETL Step Functions workflow"
  schedule_expression = var.schedule_expression
  tags                = local.common_tags
}

# EventBridge target starts Step Functions executions
resource "aws_cloudwatch_event_target" "daily_etl" {
  count     = var.enable_schedule ? 1 : 0
  rule      = aws_cloudwatch_event_rule.daily_etl[0].name
  target_id = "StartDailyETL"
  arn       = aws_sfn_state_machine.daily_etl.arn
  role_arn  = aws_iam_role.eventbridge_sfn[0].arn

  # Use InputTransformer in production for dynamic dates; static default for course labs
  input = jsonencode({
    processing_date = "auto-yesterday"
    dataset         = "retail/orders"
    triggered_by    = "eventbridge-schedule"
  })
}

resource "aws_iam_role" "eventbridge_sfn" {
  count = var.enable_schedule ? 1 : 0
  name  = "${var.project}-${var.environment}-events-sfn-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "events.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
  tags = local.common_tags
}

resource "aws_iam_role_policy" "eventbridge_sfn" {
  count = var.enable_schedule ? 1 : 0
  name  = "start-sfn"
  role  = aws_iam_role.eventbridge_sfn[0].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "states:StartExecution"
      Resource = aws_sfn_state_machine.daily_etl.arn
    }]
  })
}

# ------------------------------------------------------------------------------
# Outputs
# ------------------------------------------------------------------------------

output "state_machine_arn" {
  description = "ARN of the daily ETL state machine"
  value       = aws_sfn_state_machine.daily_etl.arn
}

output "state_machine_name" {
  description = "Name of the daily ETL state machine"
  value       = aws_sfn_state_machine.daily_etl.name
}

output "execution_role_arn" {
  description = "IAM role ARN for Step Functions execution"
  value       = aws_iam_role.sfn_execution.arn
}

output "log_group_name" {
  description = "CloudWatch log group for state machine executions"
  value       = aws_cloudwatch_log_group.sfn.name
}
