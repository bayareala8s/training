variable "name_prefix" {
  type = string
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

variable "enable_nat_gateway" {
  type    = bool
  default = false
}

variable "use_nat_instance" {
  type        = bool
  default     = true
  description = "Cheaper NAT via EC2 (tagged Role=nat-instance for start/stop scripts)"
}

variable "tags" {
  type    = map(string)
  default = {}
}
