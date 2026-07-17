variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}

variable "student_id" {
  type        = string
  description = "Unique student id (lowercase alphanumeric/hyphen)"
}

variable "name_prefix" {
  type        = string
  description = "Resource name prefix"
  default     = "baylearn-lab05"
}

variable "budget_notification_email" {
  type        = string
  description = "Email for AWS Budgets notifications"
}

variable "budget_limit_usd" {
  type        = number
  description = "Monthly budget limit USD"
  default     = 5
}

variable "enable_cloudtrail" {
  type        = bool
  description = "Enable simple CloudTrail"
  default     = true
}

variable "enable_config" {
  type        = bool
  description = "OPTIONAL AWS Config — cost warning; leave false unless stretch objective"
  default     = false
}

variable "expiration_date" {
  type        = string
  description = "ISO date when lab should be destroyed (tag)"
}
