variable "region" {
  type        = string
  description = "AWS region for BayPay student labs."
  default     = "us-west-2"
}

variable "repository_name" {
  type        = string
  description = "ECR repository name for payment-service."
  default     = "baypay/payment-service"
}

variable "expiration" {
  type        = string
  description = "ISO date after which this student environment must be destroyed."
  default     = "2026-12-31"
}
