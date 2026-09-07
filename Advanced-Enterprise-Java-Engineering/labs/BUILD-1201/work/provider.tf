# BUILD-1201 work — env skeleton (ECR + tags). No ALB/ECS/NAT/RDS.
# Region contract: us-west-2. No access keys.

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Course      = "AEJE"
      Module      = "12"
      Lab         = "BUILD-1201"
      Environment = "student"
      Expiration  = var.expiration
    }
  }
}
