terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region
  default_tags { tags = local.lab_tags }
}

module "vpc" {
  source               = "../../../../modules/vpc"
  name_prefix          = "${var.project_name}-${var.environment}"
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  enable_nat_gateway   = var.enable_nat_gateway
  use_nat_instance     = var.use_nat_instance
  tags                 = local.lab_tags
}

module "compute" {
  count         = var.enable_lab_compute ? 1 : 0
  source        = "../../../../modules/compute"
  name_prefix   = "${var.project_name}-${var.environment}"
  subnet_id     = module.vpc.private_subnet_ids[0]
  instance_type = var.instance_type
  tags          = local.lab_tags
}
