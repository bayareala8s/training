terraform {
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
