module "integration_platform" {
  source = "../../modules/integration-platform"

  name_prefix        = var.name_prefix
  student_id         = var.student_id
  aws_region         = var.aws_region
  notification_email = var.notification_email

  tags = {
    ExpirationDate = var.expiration_date
    Lab            = "lab-06-integration-platform"
  }
}
