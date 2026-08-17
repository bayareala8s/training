variable "aws_region" {
  type        = string
  description = "AWS region for lab resources."
}

variable "environment" {
  type        = string
  description = "Environment name (dev, test, prod). Used in tags and resource naming."

  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "environment must be dev, test, or prod."
  }
}

variable "owner" {
  type        = string
  description = "Owner tag for cost allocation (required by course governance)."

  validation {
    condition     = length(var.owner) > 0
    error_message = "owner must be non-empty for cost allocation tags."
  }
}

variable "project_name" {
  type        = string
  description = "Short prefix for resource names (e.g. bal8s-tf)."
}

variable "vpc_cidr" {
  type        = string
  description = "VPC CIDR block. Must not overlap other environments in the same account."

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "vpc_cidr must be a valid IPv4 CIDR block."
  }
}

variable "availability_zones" {
  type        = list(string)
  description = "Availability zones for subnets (minimum 2)."

  validation {
    condition     = length(var.availability_zones) >= 2
    error_message = "At least two availability zones are required."
  }
}

variable "public_subnet_cidrs" {
  type        = list(string)
  description = "CIDR blocks for public subnets (one per AZ)."
}

variable "private_subnet_cidrs" {
  type        = list(string)
  description = "CIDR blocks for private subnets (one per AZ)."
}

variable "enable_nat_gateway" {
  type        = bool
  description = "Use managed NAT Gateway (higher cost; typical for prod)."
}

variable "use_nat_instance" {
  type        = bool
  description = "Use EC2 NAT instance (stoppable via make lab-pause; typical for dev/test)."
}

variable "enable_lab_compute" {
  type        = bool
  description = "Deploy optional lab EC2 instance in a private subnet."
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type for lab compute when enable_lab_compute is true."

  validation {
    condition     = can(regex("^t[0-9]", var.instance_type))
    error_message = "Course labs use burstable instance types (e.g. t3.micro) for cost control."
  }
}
