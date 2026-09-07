variable "expiration" {
  type        = string
  description = "ISO date after which this student environment must be destroyed."
  default     = "2026-12-31"
}

variable "repository_name" {
  type        = string
  default     = "baypay/payment-service"
}

variable "service_name" {
  type        = string
  default     = "payment-service"
}

variable "container_image" {
  type        = string
  description = "Immutable tag. Never :latest."
  default     = "123456789012.dkr.ecr.us-west-2.amazonaws.com/baypay/payment-service:3.9.2"
}
