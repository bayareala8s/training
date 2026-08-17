variable "region" {
  description = "The AWS region to create resources in."
  default     = "us-west-2"
}

variable "bucket_name" {
  description = "The name of the S3 bucket."
  default     = "bayareala8s-static-website-bucket"
}
