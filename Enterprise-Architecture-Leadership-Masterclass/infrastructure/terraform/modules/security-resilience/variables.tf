variable "name_prefix" {
  description = "Prefix for resource names (e.g., baylearn-m07-jsmith)."
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9-]{3,40}$", var.name_prefix))
    error_message = "name_prefix must be 3-40 chars of lowercase letters, digits, and hyphens."
  }
}

variable "student_id" {
  description = "Student identifier for tagging."
  type        = string
}

variable "aws_region" {
  description = "Primary AWS region."
  type        = string
  default     = "us-east-1"
}

variable "replica_region" {
  description = "Replica region used when enable_replication is true."
  type        = string
  default     = "us-west-2"
}

variable "enable_replication" {
  description = "When true, create replica bucket and CRR. Increases cost—clean up same day."
  type        = bool
  default     = false
}

variable "alert_email" {
  description = "Optional email for SNS alarm subscriptions. Empty skips subscription."
  type        = string
  default     = ""
}

variable "expiration_date" {
  description = "Tag value YYYY-MM-DD for lab expiration."
  type        = string
}

variable "tags" {
  description = "Additional tags merged with required BayLearn tags."
  type        = map(string)
  default     = {}
}
