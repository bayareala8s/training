# BUILD-1202 starter — root pin is present; finish the child modules.

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
      Module      = "12"
      Lab         = "BUILD-1202"
      Environment = "student"
      Expiration  = var.expiration
    }
  }
}
