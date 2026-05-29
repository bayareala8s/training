variable "project_name" {
  type    = string
  default = "ms-course"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

# When false: ECS scaled to 0, NAT and ALB destroyed (saves ~$45+/month idle)
variable "platform_active" {
  type        = bool
  default     = true
  description = "Set false via aws-stop.sh to minimize cost while keeping ECR/VPC"
}

variable "ecs_desired_count" {
  type    = number
  default = 1
}

variable "jwt_secret" {
  type      = string
  sensitive = true
  default   = "change-me-use-secrets-manager-in-production"
}

variable "container_image_tag" {
  type    = string
  default = "latest"
}
