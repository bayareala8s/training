variable "aws_region" {
  type    = string
  default = "us-west-2"
}

variable "owner" {
  type = string
  validation {
    condition     = length(var.owner) > 0
    error_message = "owner is required for cost tags."
  }
}

variable "project_name" {
  type    = string
  default = "bal8s-lz"
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
