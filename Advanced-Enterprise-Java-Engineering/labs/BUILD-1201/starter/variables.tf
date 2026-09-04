# BUILD-1201 starter — add variable "region" { default = "us-west-2" }
# and an Expiration tag input. Do not invent AWS keys.

variable "repository_name" {
  type        = string
  description = "ECR repository name for payment-service."
  default     = "baypay/payment-service"
}
