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
    Environment = "dev"
    Owner       = var.owner
    Capstone    = "option-02"
    Role        = "spoke-workload"
  }
}

# Remote state contract — hub must be applied first
data "terraform_remote_state" "hub" {
  backend = "s3"
  config = {
    bucket = var.hub_state_bucket
    key    = var.hub_state_key
    region = var.aws_region
  }
}

module "spoke_vpc" {
  source = "../../../../../modules/vpc"

  name_prefix          = "${var.project_name}-spoke-dev"
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  enable_nat_gateway   = false
  use_nat_instance     = true
  tags                 = local.tags
}

output "spoke_vpc_id" {
  value = module.spoke_vpc.vpc_id
}

output "hub_vpc_id_from_remote_state" {
  value = try(data.terraform_remote_state.hub.outputs.hub_vpc_id, "apply-hub-first")
}

output "hub_cidr_for_routes" {
  value = try(data.terraform_remote_state.hub.outputs.hub_vpc_cidr, null)
}

output "platform_log_group" {
  value = try(data.terraform_remote_state.hub.outputs.platform_log_group_name, null)
}
