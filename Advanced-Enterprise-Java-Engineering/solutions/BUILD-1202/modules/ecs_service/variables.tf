variable "name" {
  type        = string
  description = "ECS service / log group name (payment-service)."
}

variable "container_port" {
  type        = number
  description = "Container listen port. BayPay payment-service is 8080."
  default     = 8080
}

variable "health_check_path" {
  type        = string
  description = "HTTP path the load balancer and task health check must use."
  default     = "/actuator/health/liveness"
}

variable "image" {
  type        = string
  description = "Immutable image reference. Never :latest."

  validation {
    condition     = !endswith(var.image, ":latest")
    error_message = "Image must use an immutable tag, not :latest."
  }
}

variable "tags" {
  type        = map(string)
  default     = {}
}
