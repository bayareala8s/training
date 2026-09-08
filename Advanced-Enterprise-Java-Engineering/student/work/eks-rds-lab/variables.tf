variable "region" {
  type        = string
  description = "BayPay teaching region. Must match the ECS lab."
  default     = "us-west-2"
}

variable "name_prefix" {
  type        = string
  description = "Short prefix for the EKS cluster and node group."
  default     = "baypay-eksrd"
}

variable "expiration" {
  type        = string
  description = "ISO date tag. Run ./stop.sh on or before this date."
  default     = "2026-09-08"
}

variable "kubernetes_version" {
  type        = string
  description = "EKS control plane version."
  default     = "1.31"
}

variable "node_instance_type" {
  type        = string
  description = "One public-subnet managed node. Not a fleet."
  default     = "t3.small"
}
