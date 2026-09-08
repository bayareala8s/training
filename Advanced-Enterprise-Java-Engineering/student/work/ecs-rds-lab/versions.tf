terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.6"
    }
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Course      = "AEJE"
      Module      = "Capstone"
      Lab         = "ECS-RDS-DEMO"
      Environment = "student"
      Expiration  = var.expiration
    }
  }
}
