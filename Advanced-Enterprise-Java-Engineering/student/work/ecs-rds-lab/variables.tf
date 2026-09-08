variable "region" {
  type        = string
  description = "BayPay teaching region."
  default     = "us-west-2"
}

variable "name_prefix" {
  type        = string
  description = "Short prefix (ALB name max 32 characters)."
  default     = "baypay-ecsrd"
}

variable "expiration" {
  type        = string
  description = "ISO date tag. Run ./stop.sh on or before this date."
  default     = "2026-09-08"
}

variable "container_image" {
  type        = string
  description = "ECR image URI with an immutable tag. Set by start.sh after push. Never :latest."
  default     = ""
}

variable "deploy_service" {
  type        = bool
  description = "False until the image exists in ECR. start.sh flips this after push."
  default     = false
}

variable "db_instance_class" {
  type        = string
  description = "Single-AZ demo class. Not Multi-AZ."
  default     = "db.t3.micro"
}
