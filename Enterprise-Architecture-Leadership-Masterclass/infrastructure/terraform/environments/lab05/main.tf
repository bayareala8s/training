module "platform_foundation" {
  source = "../../modules/platform-foundation"

  name_prefix               = var.name_prefix
  student_id                = var.student_id
  aws_region                = var.aws_region
  enable_cloudtrail         = var.enable_cloudtrail
  enable_config             = var.enable_config
  budget_limit_usd          = var.budget_limit_usd
  budget_notification_email = var.budget_notification_email

  tags = {
    ExpirationDate = var.expiration_date
    Lab            = "lab-05-cloud-platform-foundation"
  }
}
