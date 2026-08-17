# Week 1 Lab 1.3 — Bootstrap remote state (run once locally)
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.90.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "us-west-2"
}

variable "student_id" {
  type        = string
  description = "Short unique id (e.g. jdoe) for bucket name"
}

variable "state_bucket_name" {
  type        = string
  description = "Globally unique S3 bucket name"
}

locals {
  project = "bayareala8s-tf-course"
  tags = {
    Course    = "terraform-enterprise"
    Project   = local.project
    ManagedBy = "terraform"
    Purpose   = "remote-state"
  }
}

resource "aws_s3_bucket" "state" {
  bucket = var.state_bucket_name
  tags   = local.tags
}

resource "aws_s3_bucket_versioning" "state" {
  bucket = aws_s3_bucket.state.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "state" {
  bucket = aws_s3_bucket.state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "state" {
  bucket                  = aws_s3_bucket.state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "locks" {
  name         = "${local.project}-${var.student_id}-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = local.tags
}

output "backend_config" {
  value = <<-EOT
    bucket         = "${aws_s3_bucket.state.id}"
    region         = "${var.aws_region}"
    dynamodb_table = "${aws_dynamodb_table.locks.name}"
    encrypt        = true
  EOT
}
