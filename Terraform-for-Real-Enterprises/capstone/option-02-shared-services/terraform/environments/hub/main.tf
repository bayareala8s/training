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
  default_tags { tags = local.tags }
}

locals {
  tags = {
    Course      = "terraform-enterprise"
    Project     = "bayareala8s-tf-course"
    ManagedBy   = "terraform"
    Environment = "shared"
    Owner       = var.owner
    Capstone    = "option-02"
    Role        = "shared-services-hub"
  }
}

module "hub_vpc" {
  source = "../../../../../modules/vpc"

  name_prefix          = "${var.project_name}-hub"
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  enable_nat_gateway   = false
  use_nat_instance     = true
  tags                 = local.tags
}

resource "aws_cloudwatch_log_group" "platform" {
  name              = "/capstone/option-02/hub/platform"
  retention_in_days = 30
  tags              = merge(local.tags, { Name = "${var.project_name}-hub-platform-logs" })
}

output "hub_vpc_id" {
  value = module.hub_vpc.vpc_id
}

output "hub_vpc_cidr" {
  value = module.hub_vpc.vpc_cidr
}

output "hub_private_subnet_ids" {
  value = module.hub_vpc.private_subnet_ids
}

output "hub_public_subnet_ids" {
  value = module.hub_vpc.public_subnet_ids
}

output "platform_log_group_name" {
  value = aws_cloudwatch_log_group.platform.name
}

output "tgw_attachment_pattern" {
  value = "Attach VPC ${module.hub_vpc.vpc_id} to TGW; associate private subnets; propagate spoke routes for ${module.hub_vpc.vpc_cidr}"
}
