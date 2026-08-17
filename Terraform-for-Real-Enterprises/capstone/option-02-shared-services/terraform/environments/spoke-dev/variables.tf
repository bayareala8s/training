variable "aws_region" {
  type    = string
  default = "us-west-2"
}

variable "owner" {
  type = string
}

variable "project_name" {
  type    = string
  default = "bal8s-ss"
}

variable "vpc_cidr" {
  type = string
}

variable "availability_zones" {
  type = list(string)
}

variable "public_subnet_cidrs" {
  type = list(string)
}

variable "private_subnet_cidrs" {
  type = list(string)
}

variable "hub_state_bucket" {
  type    = string
  default = "bayareala8s-terraform-state"
}

variable "hub_state_key" {
  type    = string
  default = "capstone/option-02/hub/terraform.tfstate"
}
