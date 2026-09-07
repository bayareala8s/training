variable "region" {
  type        = string
  description = "BayPay teaching region. Do not switch to us-east-1."
  default     = "us-west-2"
}

variable "repository_name" {
  type        = string
  description = "ECR repository name for payment-service."
  default     = "baypay/payment-service"
}

variable "expiration" {
  type        = string
  description = "ISO date tag. Destroy on or before this date."
  default     = "2026-09-06"
}
