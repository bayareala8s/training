variable "aws_region" {
  type    = string
  default = "us-west-2"
}

variable "owner" {
  type = string
}

variable "name_prefix" {
  type    = string
  default = "svc-demo"
}

variable "vpc_cidr" {
  type    = string
  default = "10.80.0.0/16"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}
