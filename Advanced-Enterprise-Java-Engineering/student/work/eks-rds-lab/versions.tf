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
      Module      = "Capstone"
      Lab         = "EKS-RDS-DEMO"
      Environment = "student"
      Expiration  = var.expiration
    }
  }
}
