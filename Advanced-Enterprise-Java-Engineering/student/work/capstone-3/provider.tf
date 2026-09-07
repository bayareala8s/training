# CAPSTONE-3 — AEJE-D-072 student apply default (ECS/Fargate contract).
# validate only. Do not apply NAT, EKS, or RDS.

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

variable "region" {
  type        = string
  description = "AWS region for BayPay student labs."
  default     = "us-west-2"
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Course      = "AEJE"
      Module      = "Capstone"
      Lab         = "CAPSTONE-3"
      Environment = "student"
      Expiration  = var.expiration
    }
  }
}
