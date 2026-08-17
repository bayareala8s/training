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
    tags = {
      Course      = "terraform-enterprise"
      Project     = "bayareala8s-tf-course"
      ManagedBy   = "terraform"
      Environment = "prod"
      Owner       = var.owner
      Capstone    = "option-03"
      DRRole      = "primary"
    }
  }
}

module "vpc" {
  source = "../../../../../modules/vpc"

  name_prefix          = "${var.project_name}-primary"
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  enable_nat_gateway   = false
  use_nat_instance     = true
  tags = {
    Course   = "terraform-enterprise"
    Capstone = "option-03"
    DRRole   = "primary"
    Owner    = var.owner
  }
}

module "compute" {
  count  = var.enable_lab_compute ? 1 : 0
  source = "../../../../../modules/compute"

  name_prefix   = "${var.project_name}-primary"
  subnet_id     = module.vpc.private_subnet_ids[0]
  instance_type = var.instance_type
  tags = {
    Course   = "terraform-enterprise"
    Capstone = "option-03"
    DRRole   = "primary"
    Owner    = var.owner
  }
}

output "vpc_id" { value = module.vpc.vpc_id }
output "region" { value = var.aws_region }
output "dr_role" { value = "primary" }
