terraform {
  required_version = ">= 1.5.0"
}

variable "name_prefix" { type = string }
variable "vpc_cidr" { type = string }
variable "owner" { type = string }
variable "aws_region" {
  type    = string
  default = "us-west-2"
}
variable "availability_zones" {
  type    = list(string)
  default = ["us-west-2a", "us-west-2b"]
}
variable "public_subnet_cidrs" {
  type    = list(string)
  default = null
}
variable "private_subnet_cidrs" {
  type    = list(string)
  default = null
}

locals {
  public_cidrs = coalesce(var.public_subnet_cidrs, [
    cidrsubnet(var.vpc_cidr, 8, 1),
    cidrsubnet(var.vpc_cidr, 8, 2),
  ])
  private_cidrs = coalesce(var.private_subnet_cidrs, [
    cidrsubnet(var.vpc_cidr, 8, 11),
    cidrsubnet(var.vpc_cidr, 8, 12),
  ])
  tags = {
    Course    = "terraform-enterprise"
    Project   = "bayareala8s-tf-course"
    ManagedBy = "terraform"
    Owner     = var.owner
    Capstone  = "option-04"
    Platform  = "network-baseline"
  }
}

module "vpc" {
  source = "../../../../modules/vpc"

  name_prefix          = var.name_prefix
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = local.public_cidrs
  private_subnet_cidrs = local.private_cidrs
  enable_nat_gateway   = false
  use_nat_instance     = true
  tags                 = local.tags
}

output "vpc_id" { value = module.vpc.vpc_id }
output "private_subnet_ids" { value = module.vpc.private_subnet_ids }
output "public_subnet_ids" { value = module.vpc.public_subnet_ids }
output "vpc_cidr" { value = module.vpc.vpc_cidr }
