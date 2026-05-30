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
  description = "AWS region for Glue resources"
  default     = "us-east-1"
}

variable "bucket_name" {
  type        = string
  description = "S3 data lake bucket name (from s3-data-lake module)"
}

variable "glue_version" {
  type        = string
  description = "AWS Glue version for ETL jobs"
  default     = "4.0"
}

variable "worker_type" {
  type        = string
  description = "Glue worker type (G.1X, G.2X, G.025X)"
  default     = "G.1X"
}

variable "number_of_workers" {
  type        = number
  description = "Number of Glue workers for the ETL job"
  default     = 2
}

variable "dataset_path" {
  type        = string
  description = "Default dataset path under raw/cleaned zones"
  default     = "retail/orders"
}

variable "processing_date" {
  type        = string
  description = "Default processing date for lab runs (YYYY-MM-DD)"
  default     = "2024-01-15"
}

# ------------------------------------------------------------------------------
# Locals
# ------------------------------------------------------------------------------

locals {
  catalog_database_name = "${var.project}_${var.environment}_datalake"
  glue_job_name         = "${var.project}-${var.environment}-raw-to-cleaned-etl"
  glue_role_name        = "${var.project}-${var.environment}-glue-etl-role"
  cleaned_crawler_name  = "${local.catalog_database_name}-cleaned-crawler"
  scripts_prefix        = "glue/scripts"
  script_s3_key         = "${local.scripts_prefix}/glue_etl_job.py"

  common_tags = {
    Project     = var.project
    Environment = var.environment
    Student     = var.student
    ManagedBy   = "terraform"
    Course      = "cloud-native-data-engineering"
    Module      = "module-03-glue-etl"
  }
}

data "aws_caller_identity" "current" {}

# ------------------------------------------------------------------------------
# IAM Role for Glue
# ------------------------------------------------------------------------------

data "aws_iam_policy_document" "glue_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "glue_etl" {
  name               = local.glue_role_name
  assume_role_policy = data.aws_iam_policy_document.glue_assume_role.json
  tags               = local.common_tags
}

# AWS managed policy for Glue service operations
resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue_etl.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# Least-privilege S3 access scoped to data lake prefixes
data "aws_iam_policy_document" "glue_s3" {
  statement {
    sid    = "ListBucket"
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetBucketLocation",
    ]
    resources = ["arn:aws:s3:::${var.bucket_name}"]
  }

  statement {
    sid    = "ReadRaw"
    effect = "Allow"
    actions = [
      "s3:GetObject",
    ]
    resources = [
      "arn:aws:s3:::${var.bucket_name}/raw/*",
      "arn:aws:s3:::${var.bucket_name}/glue/*",
    ]
  }

  statement {
    sid    = "WriteCleaned"
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:DeleteObject",
    ]
    resources = [
      "arn:aws:s3:::${var.bucket_name}/cleaned/*",
      "arn:aws:s3:::${var.bucket_name}/glue/*",
    ]
  }
}

resource "aws_iam_role_policy" "glue_s3" {
  name   = "${local.glue_role_name}-s3"
  role   = aws_iam_role.glue_etl.id
  policy = data.aws_iam_policy_document.glue_s3.json
}

# CloudWatch Logs for job output
data "aws_iam_policy_document" "glue_logs" {
  statement {
    sid    = "GlueLogs"
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/aws-glue/*"]
  }
}

resource "aws_iam_role_policy" "glue_logs" {
  name   = "${local.glue_role_name}-logs"
  role   = aws_iam_role.glue_etl.id
  policy = data.aws_iam_policy_document.glue_logs.json
}

# ------------------------------------------------------------------------------
# Glue Data Catalog Database
# ------------------------------------------------------------------------------

resource "aws_glue_catalog_database" "datalake" {
  name        = local.catalog_database_name
  description = "Course data lake catalog — Module 3 Glue ETL"
  tags        = local.common_tags
}

# ------------------------------------------------------------------------------
# ETL Script in S3 (placeholder — labs upload full script via aws s3 cp)
# ------------------------------------------------------------------------------

resource "aws_s3_object" "glue_etl_script" {
  bucket = var.bucket_name
  key    = local.script_s3_key
  source = "${path.module}/../../../modules/module-03-glue-etl/labs/lab-3.1-etl-raw-to-cleaned/scripts/glue_etl_job.py"
  etag   = filemd5("${path.module}/../../../modules/module-03-glue-etl/labs/lab-3.1-etl-raw-to-cleaned/scripts/glue_etl_job.py")
  tags   = local.common_tags
}

# ------------------------------------------------------------------------------
# Glue ETL Job
# ------------------------------------------------------------------------------

resource "aws_glue_job" "raw_to_cleaned" {
  name     = local.glue_job_name
  role_arn = aws_iam_role.glue_etl.arn

  glue_version      = var.glue_version
  worker_type       = var.worker_type
  number_of_workers = var.number_of_workers
  timeout           = 60
  max_retries       = 0

  command {
    name            = "glueetl"
    script_location = "s3://${var.bucket_name}/${local.script_s3_key}"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"                     = "python"
    "--enable-metrics"                   = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-spark-ui"                  = "true"
    "--spark-event-logs-path"            = "s3://${var.bucket_name}/glue/spark-logs/"
    "--TempDir"                          = "s3://${var.bucket_name}/glue/temp/"
    "--raw_bucket"                       = var.bucket_name
    "--cleaned_bucket"                   = var.bucket_name
    "--dataset_path"                     = var.dataset_path
    "--processing_date"                  = var.processing_date
    "--conf"                             = "spark.sql.sources.partitionOverwriteMode=dynamic --conf spark.sql.adaptive.enabled=true"
  }

  execution_property {
    max_concurrent_runs = 2
  }

  tags = local.common_tags

  depends_on = [
    aws_s3_object.glue_etl_script,
    aws_iam_role_policy_attachment.glue_service,
    aws_iam_role_policy.glue_s3,
    aws_iam_role_policy.glue_logs,
  ]
}

# ------------------------------------------------------------------------------
# Glue Crawler — Cleaned Zone
# ------------------------------------------------------------------------------

resource "aws_glue_crawler" "cleaned" {
  name          = local.cleaned_crawler_name
  role          = aws_iam_role.glue_etl.arn
  database_name = aws_glue_catalog_database.datalake.name
  description   = "Crawl cleaned zone Parquet datasets for Athena"

  s3_target {
    path = "s3://${var.bucket_name}/cleaned/"
  }

  schema_change_policy {
    update_behavior = "LOG"
    delete_behavior = "LOG"
  }

  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }

  configuration = jsonencode({
    Version = 1
    CrawlerOutput = {
      Partitions = { AddOrUpdateBehavior = "InheritFromTable" }
    }
  })

  tags = local.common_tags

  depends_on = [
    aws_glue_catalog_database.datalake,
    aws_iam_role_policy_attachment.glue_service,
  ]
}

# ------------------------------------------------------------------------------
# Outputs
# ------------------------------------------------------------------------------

output "glue_job_name" {
  description = "Name of the Raw to Cleaned Glue ETL job"
  value       = aws_glue_job.raw_to_cleaned.name
}

output "glue_job_arn" {
  description = "ARN of the Glue ETL job"
  value       = aws_glue_job.raw_to_cleaned.arn
}

output "glue_catalog_database" {
  description = "Glue Data Catalog database name"
  value       = aws_glue_catalog_database.datalake.name
}

output "glue_role_arn" {
  description = "IAM role ARN assumed by Glue jobs and crawlers"
  value       = aws_iam_role.glue_etl.arn
}

output "cleaned_crawler_name" {
  description = "Glue crawler name for the cleaned zone"
  value       = aws_glue_crawler.cleaned.name
}

output "glue_script_s3_uri" {
  description = "S3 URI where the ETL script should be uploaded"
  value       = "s3://${var.bucket_name}/${local.script_s3_key}"
}
