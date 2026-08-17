variable "aws_region" {
  type    = string
  default = "us-west-2"
}

variable "owner" {
  type = string
}

variable "project_name" {
  type    = string
  default = "bal8s-dr"
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

variable "enable_lab_compute" {
  type    = bool
  default = false
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}
