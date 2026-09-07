variable "name" {
  type        = string
  description = "Service name (payment-service)."
}

variable "container_port" {
  type        = number
  description = "Process listen port from ACCOUNT.md."
  default     = 8080
}

variable "health_check_path" {
  type        = string
  description = "ALB / Actuator liveness path from ACCOUNT.md."
  default     = "/actuator/health/liveness"
}

variable "image" {
  type        = string
  description = "ECR image URI with an immutable tag. Never :latest."
}

variable "tags" {
  type        = map(string)
  default     = {}
}
