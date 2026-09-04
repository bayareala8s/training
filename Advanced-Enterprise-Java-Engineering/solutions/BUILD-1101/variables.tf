variable "region" {
  type        = string
  description = "BayPay teaching region. Do not switch to us-east-1."
  default     = "us-west-2"
}

variable "name_prefix" {
  type        = string
  description = "Short prefix for ALB, cluster, and IAM names (ALB name max 32 chars)."
  default     = "baypay-1101"
}

variable "expiration" {
  type        = string
  description = "ISO date tag. Destroy on or before this date."
  default     = "2026-09-04"
}

variable "container_image" {
  type        = string
  description = "ECR image URI with an immutable tag. Never :latest."
  default     = "123456789012.dkr.ecr.us-west-2.amazonaws.com/baypay/payment-service:3.9.2"
}
