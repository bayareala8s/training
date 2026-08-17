variable "name_prefix" {
  type        = string
  description = "Prefix for security group and EC2 instance names."
}

variable "subnet_id" {
  type        = string
  description = "Subnet ID for the lab instance (typically first private subnet)."
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type for the lab host."
  default     = "t3.micro"
}

variable "tags" {
  type        = map(string)
  description = "Tags applied to compute resources (must include Course=terraform-enterprise for cost scripts)."
}
