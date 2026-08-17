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
      Capstone    = "option-04"
      Environment = "dev"
      Owner       = var.owner
      ManagedBy   = "terraform"
    }
  }
}

module "network" {
  source = "../../modules/network-baseline"

  name_prefix = var.name_prefix
  vpc_cidr    = var.vpc_cidr
  owner       = var.owner
  aws_region  = var.aws_region
}

module "app" {
  source = "../../modules/app-host"

  name_prefix   = var.name_prefix
  subnet_id     = module.network.private_subnet_ids[0]
  owner         = var.owner
  instance_type = var.instance_type
}

output "vpc_id" { value = module.network.vpc_id }
output "instance_id" { value = module.app.instance_id }
