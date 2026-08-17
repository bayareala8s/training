data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  name_prefix    = "${var.project}-${var.environment}"
  partner_prefix = "partners/${var.partner_id}"
  inbound_prefix = "${local.partner_prefix}/inbound/"
  tags = {
    Project     = var.project
    Environment = var.environment
    Course      = "BayLearn-MFT"
  }
}

module "kms" {
  source      = "../../modules/kms"
  name_prefix = local.name_prefix
  tags        = local.tags
}

module "logs_bucket" {
  source        = "../../modules/s3_bucket"
  bucket_name   = "${local.name_prefix}-logs-${data.aws_caller_identity.current.account_id}"
  kms_key_arn   = module.kms.key_arn
  force_destroy = var.force_destroy
  versioning    = true
  tags          = local.tags
}

module "landing_bucket" {
  source                = "../../modules/s3_bucket"
  bucket_name           = "${local.name_prefix}-landing-${data.aws_caller_identity.current.account_id}"
  kms_key_arn           = module.kms.key_arn
  force_destroy         = var.force_destroy
  versioning            = true
  enable_access_logging = true
  logging_target_bucket = module.logs_bucket.bucket_id
  logging_target_prefix = "landing-access/"
  tags                  = local.tags

  depends_on = [module.logs_bucket]
}

resource "aws_s3_object" "prefix_placeholders" {
  for_each = toset([
    "${local.partner_prefix}/inbound/.keep",
    "${local.partner_prefix}/processing/.keep",
    "${local.partner_prefix}/quarantine/.keep",
    "${local.partner_prefix}/outbound/.keep",
    "${local.partner_prefix}/connector/.keep",
    "${local.partner_prefix}/large/inbound/.keep",
    "${local.partner_prefix}/large/processed/.keep",
  ])
  bucket  = module.landing_bucket.bucket_id
  key     = each.value
  content = ""
}

module "transfer" {
  count  = var.enable_transfer_family ? 1 : 0
  source = "../../modules/transfer_family"

  name_prefix          = local.name_prefix
  account_id           = data.aws_caller_identity.current.account_id
  region               = data.aws_region.current.id
  bucket_id            = module.landing_bucket.bucket_id
  bucket_arn           = module.landing_bucket.bucket_arn
  kms_key_arn          = module.kms.key_arn
  enable_server        = true
  enable_connector     = var.enable_connector
  inbound_username     = var.inbound_username
  inbound_prefix       = local.inbound_prefix
  connector_prefix     = "${local.partner_prefix}/connector/"
  staging_prefix       = "${local.partner_prefix}/outbound/"
  secret_recovery_days = 0
  tags                 = local.tags

  depends_on = [module.landing_bucket, aws_s3_object.prefix_placeholders]
}

resource "aws_dynamodb_table" "idempotency" {
  name         = "${local.name_prefix}-idempotency"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "event_key"

  attribute {
    name = "event_key"
    type = "S"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = local.tags
}

resource "aws_dynamodb_table" "connections" {
  name         = "${local.name_prefix}-connections"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "connection_id"

  attribute {
    name = "connection_id"
    type = "S"
  }

  tags = local.tags
}

resource "aws_dynamodb_table" "jobs" {
  name         = "${local.name_prefix}-jobs"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "job_id"

  attribute {
    name = "job_id"
    type = "S"
  }

  tags = local.tags
}

resource "aws_sns_topic" "workflow_success" {
  name = "${local.name_prefix}-workflow-success"
  tags = local.tags
}

resource "aws_sns_topic" "workflow_failure" {
  name = "${local.name_prefix}-workflow-failure"
  tags = local.tags
}

resource "aws_sns_topic_subscription" "workflow_success_email" {
  count     = var.admin_email != "" ? 1 : 0
  topic_arn = aws_sns_topic.workflow_success.arn
  protocol  = "email"
  endpoint  = var.admin_email
}

resource "aws_sns_topic_subscription" "workflow_failure_email" {
  count     = var.admin_email != "" ? 1 : 0
  topic_arn = aws_sns_topic.workflow_failure.arn
  protocol  = "email"
  endpoint  = var.admin_email
}
