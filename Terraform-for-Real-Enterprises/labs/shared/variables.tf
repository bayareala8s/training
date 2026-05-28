variable "aws_region" {
  type        = string
  description = "AWS region for lab resources"
  default     = "us-west-2"
}

variable "environment" {
  type        = string
  description = "Environment name: dev, test, prod"
}

variable "owner" {
  type        = string
  description = "Student or team email prefix"
  default     = "student"
}

variable "project_name" {
  type        = string
  description = "Prefix for resource names"
  default     = "bal8s-tf"
}

variable "vpc_cidr" {
  type        = string
  description = "VPC CIDR block"
}

variable "availability_zones" {
  type        = list(string)
  description = "AZs to use (min 2)"
}

variable "enable_nat_gateway" {
  type        = bool
  description = "Use NAT Gateway (costly). Set false for NAT instance or no NAT in dev."
  default     = false
}

variable "enable_lab_compute" {
  type        = bool
  description = "Deploy optional EC2 lab instance for start/stop exercises"
  default     = true
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}
