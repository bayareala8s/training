variable "primary_bucket_name" {
  description = "Name of the primary S3 bucket"
  default     = "primary-bucket-unique-name"
}

variable "replica_bucket_name" {
  description = "Name of the replica S3 bucket"
  default     = "replica-bucket-unique-name"
}
