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

locals {
  bucket_name = "${var.project}-${var.environment}-datalake-${data.aws_caller_identity.current.account_id}"
  common_tags = {
    Project     = var.project
    Environment = var.environment
    Student     = var.student
    ManagedBy   = "terraform"
    Course      = "cloud-native-data-engineering"
  }
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "datalake" {
  bucket = local.bucket_name
  tags   = local.common_tags
}

resource "aws_s3_bucket_versioning" "datalake" {
  bucket = aws_s3_bucket.datalake.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "datalake" {
  bucket = aws_s3_bucket.datalake.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "datalake" {
  bucket                  = aws_s3_bucket.datalake.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "datalake" {
  bucket = aws_s3_bucket.datalake.id

  rule {
    id     = "transition-raw-to-ia"
    status = "Enabled"
    filter { prefix = "raw/" }

    transition {
      days          = 90
      storage_class = "STANDARD_IA"
    }
  }

  rule {
    id     = "transition-curated-to-glacier"
    status = "Enabled"
    filter { prefix = "curated/" }

    transition {
      days          = 180
      storage_class = "GLACIER"
    }
  }
}

resource "aws_s3_object" "zones" {
  for_each = toset(["raw/", "cleaned/", "curated/", "quarantine/", "metadata/"])
  bucket   = aws_s3_bucket.datalake.id
  key      = each.value
  content  = ""
}

output "bucket_name" {
  value = aws_s3_bucket.datalake.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.datalake.arn
}

output "zone_prefixes" {
  value = ["raw/", "cleaned/", "curated/", "quarantine/", "metadata/"]
}
