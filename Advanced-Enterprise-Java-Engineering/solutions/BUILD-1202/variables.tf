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

variable "service_name" {
  type        = string
  description = "Logical ECS service name."
  default     = "payment-service"
}

variable "container_port" {
  type        = number
  description = "Container listen port. BayPay payment-service is 8080."
  default     = 8080
}

variable "health_check_path" {
  type        = string
  description = "HTTP path ALB and task health must use."
  default     = "/actuator/health/liveness"
}
