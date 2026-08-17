# Lab 012 — minimal Terraform stub (plan-only by default)
terraform {
  required_version = ">= 1.5.0"
}

variable "primary_region" {
  type    = string
  default = "us-east-1"
}

variable "dr_region" {
  type    = string
  default = "us-west-2"
}

variable "lab_tag" {
  type    = string
  default = "lab-012"
}

# Stub: replace with real modules during implementation
output "lab_info" {
  value = {
    primary_region = var.primary_region
    dr_region      = var.dr_region
    lab_tag        = var.lab_tag
    note           = "Implement VPC, ALB, RDS modules — plan before apply"
  }
}
