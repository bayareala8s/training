variable "name_prefix" {
  description = "Prefix for resource names (e.g., baylearn-lab06)"
  type        = string
}

variable "student_id" {
  description = "Student identifier used in tags and naming"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "notification_email" {
  description = "Email for SNS lab notifications (confirm subscription)"
  type        = string
}

variable "tags" {
  description = "Additional tags"
  type        = map(string)
  default     = {}
}
