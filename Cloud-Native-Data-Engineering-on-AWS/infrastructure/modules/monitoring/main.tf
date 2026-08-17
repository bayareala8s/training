terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

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
  type    = string
  default = "us-east-1"
}

variable "alert_email" {
  type        = string
  description = "Email address for SNS alert subscriptions"
}

variable "glue_job_names" {
  type        = list(string)
  description = "Glue job names to monitor"
  default     = []
}

variable "lambda_function_names" {
  type        = list(string)
  description = "Lambda function names to monitor"
  default     = []
}

variable "data_lake_bucket" {
  type        = string
  description = "S3 data lake bucket name for storage alarms"
  default     = ""
}

locals {
  name_prefix = "${var.project}-${var.environment}"
  common_tags = {
    Project     = var.project
    Environment = var.environment
    Student     = var.student
    ManagedBy   = "terraform"
    Course      = "cloud-native-data-engineering"
    Module      = "monitoring"
  }
}

# ---------------------------------------------------------------------------
# SNS Topics
# ---------------------------------------------------------------------------

resource "aws_sns_topic" "alerts_critical" {
  name = "${local.name_prefix}-alerts-critical"
  tags = merge(local.common_tags, { Severity = "critical" })
}

resource "aws_sns_topic" "alerts_warning" {
  name = "${local.name_prefix}-alerts-warning"
  tags = merge(local.common_tags, { Severity = "warning" })
}

resource "aws_sns_topic_subscription" "critical_email" {
  topic_arn = aws_sns_topic.alerts_critical.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

resource "aws_sns_topic_subscription" "warning_email" {
  topic_arn = aws_sns_topic.alerts_warning.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# ---------------------------------------------------------------------------
# CloudWatch Dashboard – ETL Pipeline Operations
# ---------------------------------------------------------------------------

resource "aws_cloudwatch_dashboard" "etl_pipeline" {
  dashboard_name = "${local.name_prefix}-etl-pipeline"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "text"
        x      = 0
        y      = 0
        width  = 24
        height = 1
        properties = {
          markdown = "# CNDE ETL Pipeline Operations\nEnvironment: **${var.environment}** | Project: **${var.project}**"
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 1
        width  = 12
        height = 6
        properties = {
          title  = "Glue Job Failures (24h)"
          region = var.aws_region
          metrics = [
            for job in var.glue_job_names : [
              "AWS/Glue", "glue.driver.aggregate.numFailedTasks",
              "JobName", job, "Type", "gauge", { "stat" = "Sum", "period" = 300 }
            ]
          ]
          view   = "timeSeries"
          period = 300
          stat   = "Sum"
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 1
        width  = 12
        height = 6
        properties = {
          title  = "Glue Job Duration (P95)"
          region = var.aws_region
          metrics = [
            for job in var.glue_job_names : [
              "AWS/Glue", "glue.driver.ExecutorRunTime",
              "JobName", job, "Type", "gauge", { "stat" = "p95", "period" = 300 }
            ]
          ]
          view   = "timeSeries"
          period = 300
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 7
        width  = 8
        height = 6
        properties = {
          title  = "Lambda Errors"
          region = var.aws_region
          metrics = [
            for fn in var.lambda_function_names : [
              "AWS/Lambda", "Errors", "FunctionName", fn, { "stat" = "Sum" }
            ]
          ]
          view   = "timeSeries"
          period = 300
        }
      },
      {
        type   = "metric"
        x      = 8
        y      = 7
        width  = 8
        height = 6
        properties = {
          title  = "Data Quality Pass Rate"
          region = var.aws_region
          metrics = [
            ["CNDE/DataQuality", "ValidationPassRate", "Dataset", "retail/orders", "Environment", var.environment, { "stat" = "Average" }]
          ]
          view   = "timeSeries"
          period = 300
          yAxis = {
            left = { min = 95, max = 100 }
          }
        }
      },
      {
        type   = "metric"
        x      = 16
        y      = 7
        width  = 8
        height = 6
        properties = {
          title  = "Records Quarantined"
          region = var.aws_region
          metrics = [
            ["CNDE/DataQuality", "QuarantinedRecords", "Dataset", "retail/orders", "Environment", var.environment, { "stat" = "Sum" }]
          ]
          view   = "timeSeries"
          period = 300
        }
      }
    ]
  })
}

# ---------------------------------------------------------------------------
# CloudWatch Alarms
# ---------------------------------------------------------------------------

resource "aws_cloudwatch_metric_alarm" "glue_job_failure" {
  for_each = toset(var.glue_job_names)

  alarm_name          = "${local.name_prefix}-glue-failure-${each.value}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "glue.driver.aggregate.numFailedTasks"
  namespace           = "AWS/Glue"
  period              = 300
  statistic           = "Sum"
  threshold           = 0
  treat_missing_data  = "notBreaching"
  alarm_description   = "Glue job ${each.value} reported failed tasks. See runbook: modules/module-08-monitoring-ops/assignments/assignment-08.md"
  alarm_actions       = [aws_sns_topic.alerts_critical.arn]
  ok_actions          = [aws_sns_topic.alerts_warning.arn]

  dimensions = {
    JobName = each.value
    Type    = "gauge"
  }

  tags = local.common_tags
}

resource "aws_cloudwatch_metric_alarm" "quality_pass_rate_low" {
  alarm_name          = "${local.name_prefix}-quality-pass-rate-low"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 2
  metric_name         = "ValidationPassRate"
  namespace           = "CNDE/DataQuality"
  period              = 300
  statistic           = "Average"
  threshold           = 99.0
  treat_missing_data  = "notBreaching"
  alarm_description   = "Data quality pass rate for retail/orders dropped below 99%. Review quarantine zone."
  alarm_actions       = [aws_sns_topic.alerts_warning.arn]

  dimensions = {
    Dataset     = "retail/orders"
    Environment = var.environment
  }

  tags = local.common_tags
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  for_each = toset(var.lambda_function_names)

  alarm_name          = "${local.name_prefix}-lambda-errors-${each.value}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 0
  treat_missing_data  = "notBreaching"
  alarm_description   = "Lambda ${each.value} reported errors. Check CloudWatch Logs."
  alarm_actions       = [aws_sns_topic.alerts_critical.arn]

  dimensions = {
    FunctionName = each.value
  }

  tags = local.common_tags
}

# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------

output "dashboard_name" {
  value = aws_cloudwatch_dashboard.etl_pipeline.dashboard_name
}

output "sns_critical_topic_arn" {
  value = aws_sns_topic.alerts_critical.arn
}

output "sns_warning_topic_arn" {
  value = aws_sns_topic.alerts_warning.arn
}

output "alarm_names" {
  value = concat(
    [for a in aws_cloudwatch_metric_alarm.glue_job_failure : a.alarm_name],
    [for a in aws_cloudwatch_metric_alarm.lambda_errors : a.alarm_name],
    [aws_cloudwatch_metric_alarm.quality_pass_rate_low.alarm_name]
  )
}
