terraform {
  required_version = ">= 1.5.0"
}

variable "name_prefix" { type = string }
variable "subnet_id" { type = string }
variable "owner" { type = string }
variable "instance_type" {
  type    = string
  default = "t3.micro"
}

locals {
  tags = {
    Course    = "terraform-enterprise"
    Project   = "bayareala8s-tf-course"
    ManagedBy = "terraform"
    Owner     = var.owner
    Capstone  = "option-04"
    Platform  = "app-host"
  }
}

module "compute" {
  source = "../../../../modules/compute"

  name_prefix   = var.name_prefix
  subnet_id     = var.subnet_id
  instance_type = var.instance_type
  tags          = local.tags
}

output "instance_id" { value = module.compute.instance_id }
output "private_ip" { value = module.compute.private_ip }
