locals {
  lab_tags = {
    Course      = "terraform-enterprise"
    Project     = "bayareala8s-tf-course"
    ManagedBy   = "terraform"
    Environment = var.environment
    Owner       = var.owner
  }
}
