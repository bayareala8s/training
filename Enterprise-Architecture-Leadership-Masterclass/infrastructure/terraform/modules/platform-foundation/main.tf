locals {
  required_tags = {
    Project     = "BayLearn"
    Course      = "EnterpriseArchitectureLeadership"
    Module      = "05"
    Environment = "Lab"
    Student     = var.student_id
    ManagedBy   = "Terraform"
    CaseStudy   = "NorthStar-Fictional"
  }

  tags = merge(local.required_tags, var.tags)

  name = "${var.name_prefix}-${var.student_id}"
}

data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}
data "aws_region" "current" {}

resource "random_id" "suffix" {
  byte_length = 4
}

# -----------------------------------------------------------------------------
# S3 audit bucket (CloudTrail destination + platform audit artifacts)
# -----------------------------------------------------------------------------

resource "aws_s3_bucket" "audit" {
  bucket        = "${local.name}-audit-${random_id.suffix.hex}"
  force_destroy = true

  tags = merge(local.tags, { Name = "${local.name}-audit" })
}

resource "aws_s3_bucket_public_access_block" "audit" {
  bucket = aws_s3_bucket.audit.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "audit" {
  bucket = aws_s3_bucket.audit.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "audit" {
  bucket = aws_s3_bucket.audit.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "audit" {
  bucket = aws_s3_bucket.audit.id

  rule {
    id     = "expire-lab-objects"
    status = "Enabled"

    filter {}

    expiration {
      days = 7
    }

    noncurrent_version_expiration {
      noncurrent_days = 1
    }
  }
}

data "aws_iam_policy_document" "audit_bucket" {
  statement {
    sid    = "AWSCloudTrailAclCheck"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions   = ["s3:GetBucketAcl"]
    resources = [aws_s3_bucket.audit.arn]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [data.aws_caller_identity.current.account_id]
    }
  }

  statement {
    sid    = "AWSCloudTrailWrite"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.audit.arn}/AWSLogs/${data.aws_caller_identity.current.account_id}/*"]

    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [data.aws_caller_identity.current.account_id]
    }
  }
}

resource "aws_s3_bucket_policy" "audit" {
  bucket = aws_s3_bucket.audit.id
  policy = data.aws_iam_policy_document.audit_bucket.json
}

# -----------------------------------------------------------------------------
# CloudTrail (optional simple single-region trail)
# -----------------------------------------------------------------------------

resource "aws_cloudtrail" "lab" {
  count = var.enable_cloudtrail ? 1 : 0

  name                          = "${local.name}-trail"
  s3_bucket_name                = aws_s3_bucket.audit.id
  include_global_service_events = true
  is_multi_region_trail         = false
  enable_log_file_validation    = true

  event_selector {
    read_write_type           = "All"
    include_management_events = true
  }

  depends_on = [aws_s3_bucket_policy.audit]

  tags = merge(local.tags, { Name = "${local.name}-trail" })
}

# -----------------------------------------------------------------------------
# DynamoDB — platform registry / heartbeat
# -----------------------------------------------------------------------------

resource "aws_dynamodb_table" "platform_registry" {
  name         = "${local.name}-registry"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  range_key    = "sk"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = merge(local.tags, { Name = "${local.name}-registry" })
}

# -----------------------------------------------------------------------------
# SSM Parameter Store — platform config golden path
# -----------------------------------------------------------------------------

resource "aws_ssm_parameter" "environment" {
  name  = "/${var.name_prefix}/platform/environment"
  type  = "String"
  value = "Lab"
  tags  = local.tags
}

resource "aws_ssm_parameter" "owner" {
  name  = "/${var.name_prefix}/platform/owner"
  type  = "String"
  value = "platform-team"
  tags  = local.tags
}

resource "aws_ssm_parameter" "cost_center" {
  name  = "/${var.name_prefix}/platform/cost-center"
  type  = "String"
  value = "EA-Lab-05"
  tags  = local.tags
}

# -----------------------------------------------------------------------------
# IAM — Lambda execution role (least privilege for lab)
# -----------------------------------------------------------------------------

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda" {
  name               = "${local.name}-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
  tags               = local.tags
}

data "aws_iam_policy_document" "lambda" {
  statement {
    sid    = "Logs"
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:${data.aws_partition.current.partition}:logs:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:*"]
  }

  statement {
    sid       = "DynamoDB"
    effect    = "Allow"
    actions   = ["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:Query"]
    resources = [aws_dynamodb_table.platform_registry.arn]
  }

  statement {
    sid       = "SSMRead"
    effect    = "Allow"
    actions   = ["ssm:GetParameter", "ssm:GetParameters"]
    resources = ["arn:${data.aws_partition.current.partition}:ssm:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:parameter/${var.name_prefix}/platform/*"]
  }
}

resource "aws_iam_role_policy" "lambda" {
  name   = "${local.name}-lambda-policy"
  role   = aws_iam_role.lambda.id
  policy = data.aws_iam_policy_document.lambda.json
}

# -----------------------------------------------------------------------------
# CloudWatch Logs + Lambda + HTTP API
# -----------------------------------------------------------------------------

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${local.name}-health"
  retention_in_days = 7
  tags              = local.tags
}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "${path.module}/lambda/handler.py"
  output_path = "${path.module}/lambda/handler.zip"
}

resource "aws_lambda_function" "platform_health" {
  function_name = "${local.name}-health"
  role          = aws_iam_role.lambda.arn
  handler       = "handler.handler"
  runtime       = "python3.12"
  timeout       = 10
  memory_size   = 128

  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256

  environment {
    variables = {
      REGISTRY_TABLE = aws_dynamodb_table.platform_registry.name
      SSM_PREFIX     = "/${var.name_prefix}/platform"
    }
  }

  depends_on = [aws_cloudwatch_log_group.lambda, aws_iam_role_policy.lambda]

  tags = merge(local.tags, { Name = "${local.name}-health" })
}

resource "aws_apigatewayv2_api" "platform" {
  name          = "${local.name}-http-api"
  protocol_type = "HTTP"
  tags          = local.tags
}

resource "aws_apigatewayv2_integration" "health" {
  api_id                 = aws_apigatewayv2_api.platform.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.platform_health.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "health" {
  api_id    = aws_apigatewayv2_api.platform.id
  route_key = "GET /health"
  target    = "integrations/${aws_apigatewayv2_integration.health.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.platform.id
  name        = "$default"
  auto_deploy = true
  tags        = local.tags
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.platform_health.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.platform.execution_arn}/*/*"
}

# -----------------------------------------------------------------------------
# AWS Budgets — FinOps guardrail for the lab
# -----------------------------------------------------------------------------

resource "aws_budgets_budget" "lab" {
  name              = "${local.name}-budget"
  budget_type       = "COST"
  limit_amount      = tostring(var.budget_limit_usd)
  limit_unit        = "USD"
  time_unit         = "MONTHLY"
  time_period_start = "2026-01-01_00:00"

  cost_filter {
    name = "TagKeyValue"
    values = [
      "user:Project$BayLearn",
      "user:Module$05",
    ]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.budget_notification_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.budget_notification_email]
  }

  tags = local.tags
}

# -----------------------------------------------------------------------------
# OPTIONAL AWS Config (cost warning — off by default)
# -----------------------------------------------------------------------------

resource "aws_iam_role" "config" {
  count = var.enable_config ? 1 : 0

  name = "${local.name}-config-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "config.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = local.tags
}

resource "aws_iam_role_policy_attachment" "config" {
  count = var.enable_config ? 1 : 0

  role       = aws_iam_role.config[0].name
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/service-role/AWS_ConfigRole"
}

resource "aws_config_configuration_recorder" "lab" {
  count = var.enable_config ? 1 : 0

  name     = "${local.name}-recorder"
  role_arn = aws_iam_role.config[0].arn

  recording_group {
    all_supported                 = false
    include_global_resource_types = false
    resource_types                = ["AWS::S3::Bucket", "AWS::Lambda::Function"]
  }
}

resource "aws_config_delivery_channel" "lab" {
  count = var.enable_config ? 1 : 0

  name           = "${local.name}-delivery"
  s3_bucket_name = aws_s3_bucket.audit.bucket

  depends_on = [aws_config_configuration_recorder.lab]
}

resource "aws_config_configuration_recorder_status" "lab" {
  count = var.enable_config ? 1 : 0

  name       = aws_config_configuration_recorder.lab[0].name
  is_enabled = true

  depends_on = [aws_config_delivery_channel.lab]
}
