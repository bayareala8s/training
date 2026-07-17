variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region"
}

variable "student_id" {
  type        = string
  description = "Unique student id"
}

variable "name_prefix" {
  type        = string
  default     = "baylearn-lab06"
  description = "Resource name prefix"
}

variable "notification_email" {
  type        = string
  description = "Email for SNS notifications (confirm subscription)"
}

variable "expiration_date" {
  type        = string
  description = "ISO date when lab should be destroyed"
}
