terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.90.0"
    }
  }
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = local.tags
  }
}

locals {
  tags = {
    Course      = "terraform-enterprise"
    Project     = "bayareala8s-tf-course"
    ManagedBy   = "terraform"
    Environment = "shared"
    Owner       = var.owner
    Capstone    = "option-01"
    Role        = "landing-zone-shared"
  }
}

module "vpc" {
  source = "../../../../../modules/vpc"

  name_prefix          = "${var.project_name}-shared"
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  enable_nat_gateway   = false
  use_nat_instance     = true
  tags                 = local.tags
}

# Security baseline: encrypted log group retention for org-wide patterns
resource "aws_cloudwatch_log_group" "security_baseline" {
  name              = "/capstone/option-01/shared/security-baseline"
  retention_in_days = 30

  tags = merge(local.tags, {
    Name = "${var.project_name}-shared-security-logs"
  })
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "private_subnet_ids" {
  value = module.vpc.private_subnet_ids
}

output "security_log_group" {
  value = aws_cloudwatch_log_group.security_baseline.name
}
