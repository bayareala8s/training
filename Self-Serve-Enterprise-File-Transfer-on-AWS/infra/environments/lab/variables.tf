variable "aws_region" {
  type        = string
  description = "AWS region for all lab resources."
  default     = "us-west-2"
}

variable "project" {
  type    = string
  default = "baylearn-mft"
}

variable "environment" {
  type    = string
  default = "lab"
}

variable "force_destroy" {
  type        = bool
  description = "Allow Terraform to delete non-empty S3 buckets (required for stop_stack destroy)."
  default     = true
}

variable "enable_transfer_family" {
  type        = bool
  description = "Provision Transfer Family SFTP server (primary ongoing cost while ONLINE)."
  default     = true
}

variable "enable_connector" {
  type        = bool
  description = "Self-demo connector to the same Transfer server (Lab 5)."
  default     = true
}

variable "partner_id" {
  type    = string
  default = "demo"
}

variable "inbound_username" {
  type    = string
  default = "partner-demo"
}

variable "admin_email" {
  type        = string
  description = "Cognito test user email (Lab 6)."
  default     = "lab-admin@example.com"
}

variable "admin_password" {
  type        = string
  description = "Cognito test user password (min 8 chars, upper/lower/number)."
  default     = "BayLearn1!"
  sensitive   = true
}

variable "enable_ecs_worker" {
  type        = bool
  description = "Lab 9: ECS Fargate worker for large file transfers (VPC + ECR; pay per task run)."
  default     = true
}

variable "ecs_task_cpu" {
  type    = string
  default = "1024"
}

variable "ecs_task_memory" {
  type    = string
  default = "2048"
}

variable "ecs_image_tag" {
  type        = string
  description = "Docker image tag pushed by scripts/build_ecs_worker.sh"
  default     = "latest"
}

variable "skip_ecs_image_build" {
  type        = bool
  description = "Set true if image already in ECR (CI); start_stack.sh skips docker build."
  default     = false
}
