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
    Environment = "dev"
    Owner       = var.owner
    Capstone    = "option-01"
    Role        = "landing-zone-workload"
  }
}

module "vpc" {
  source = "../../../../../modules/vpc"

  name_prefix          = "${var.project_name}-wl-dev"
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  enable_nat_gateway   = false
  use_nat_instance     = true
  tags                 = local.tags
}

module "compute" {
  count  = var.enable_lab_compute ? 1 : 0
  source = "../../../../../modules/compute"

  name_prefix   = "${var.project_name}-wl-dev"
  subnet_id     = module.vpc.private_subnet_ids[0]
  instance_type = var.instance_type
  tags          = local.tags
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "lab_instance_id" {
  value = try(module.compute[0].instance_id, null)
}
