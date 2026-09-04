variable "expiration" {
  type        = string
  description = "ISO date after which this student environment must be destroyed."
  default     = "2026-12-31"
}

variable "repository_name" {
  type        = string
  description = "ECR repository name for payment-service."
  default     = "baypay/payment-service"
}
