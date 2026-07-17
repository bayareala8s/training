variable "name_prefix" {
  description = "Prefix for resource names (e.g., baylearn-lab05)"
  type        = string
}

variable "student_id" {
  description = "Student identifier used in tags and resource naming"
  type        = string
}

variable "aws_region" {
  description = "AWS region for lab resources"
  type        = string
  default     = "us-east-1"
}

variable "enable_cloudtrail" {
  description = "Create a simple single-region CloudTrail (low cost; disable to minimize further)"
  type        = bool
  default     = true
}

variable "enable_config" {
  description = "OPTIONAL: enable AWS Config recorder. Cost warning — leave false for typical lab."
  type        = bool
  default     = false
}

variable "budget_limit_usd" {
  description = "Monthly budget amount in USD for AWS Budgets alert"
  type        = number
  default     = 5
}

variable "budget_notification_email" {
  description = "Email for budget alerts (must confirm SNS subscription if required by account)"
  type        = string
}

variable "tags" {
  description = "Additional tags merged with required BayLearn tags"
  type        = map(string)
  default     = {}
}
