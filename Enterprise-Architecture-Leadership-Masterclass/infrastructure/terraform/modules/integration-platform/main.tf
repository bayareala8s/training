locals {
  required_tags = {
    Project     = "BayLearn"
    Course      = "EnterpriseArchitectureLeadership"
    Module      = "06"
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
# S3 — partner file landing (SFTP simulation) + analytics landing
# -----------------------------------------------------------------------------

resource "aws_s3_bucket" "partner" {
  bucket        = "${local.name}-partner-${random_id.suffix.hex}"
  force_destroy = true
  tags          = merge(local.tags, { Name = "${local.name}-partner", Purpose = "SFTP-simulation" })
}

resource "aws_s3_bucket_public_access_block" "partner" {
  bucket                  = aws_s3_bucket.partner.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "partner" {
  bucket = aws_s3_bucket.partner.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "partner" {
  bucket = aws_s3_bucket.partner.id
  rule {
    id     = "expire-lab"
    status = "Enabled"
    filter {}
    expiration { days = 3 }
  }
}

resource "aws_s3_bucket_notification" "partner" {
  bucket = aws_s3_bucket.partner.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.partner_file.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "incoming/"
  }

  depends_on = [aws_lambda_permission.s3_partner]
}

# -----------------------------------------------------------------------------
# DynamoDB — accounts + payment processing records
# -----------------------------------------------------------------------------

resource "aws_dynamodb_table" "accounts" {
  name         = "${local.name}-accounts"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "account_id"

  attribute {
    name = "account_id"
    type = "S"
  }

  tags = merge(local.tags, { Name = "${local.name}-accounts" })
}

# -----------------------------------------------------------------------------
# EventBridge custom bus + rules
# -----------------------------------------------------------------------------

resource "aws_cloudwatch_event_bus" "northstar" {
  name = "${local.name}-bus"
  tags = local.tags
}

resource "aws_cloudwatch_event_rule" "payments" {
  name           = "${local.name}-payments"
  event_bus_name = aws_cloudwatch_event_bus.northstar.name
  description    = "Route payment events to SQS"

  event_pattern = jsonencode({
    source      = ["northstar.payments"]
    detail-type = ["PaymentSubmitted"]
  })

  tags = local.tags
}

resource "aws_cloudwatch_event_target" "payments_sqs" {
  rule           = aws_cloudwatch_event_rule.payments.name
  event_bus_name = aws_cloudwatch_event_bus.northstar.name
  arn            = aws_sqs_queue.payments.arn
}

resource "aws_cloudwatch_event_rule" "partner_files" {
  name           = "${local.name}-partner-files"
  event_bus_name = aws_cloudwatch_event_bus.northstar.name
  description    = "Partner file received → start regulatory batch (optional hook)"

  event_pattern = jsonencode({
    source      = ["northstar.partners"]
    detail-type = ["PartnerFileReceived"]
  })

  tags = local.tags
}

resource "aws_cloudwatch_event_target" "partner_sns" {
  rule           = aws_cloudwatch_event_rule.partner_files.name
  event_bus_name = aws_cloudwatch_event_bus.northstar.name
  arn            = aws_sns_topic.alerts.arn
}

# -----------------------------------------------------------------------------
# SQS — payment processing queue + DLQ
# -----------------------------------------------------------------------------

resource "aws_sqs_queue" "payments_dlq" {
  name                      = "${local.name}-payments-dlq"
  message_retention_seconds = 1209600
  tags                      = local.tags
}

resource "aws_sqs_queue" "payments" {
  name                       = "${local.name}-payments"
  visibility_timeout_seconds = 60
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.payments_dlq.arn
    maxReceiveCount     = 3
  })
  tags = local.tags
}

data "aws_iam_policy_document" "payments_queue" {
  statement {
    sid    = "AllowEventBridge"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.payments.arn]
    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_cloudwatch_event_rule.payments.arn]
    }
  }
}

resource "aws_sqs_queue_policy" "payments" {
  queue_url = aws_sqs_queue.payments.id
  policy    = data.aws_iam_policy_document.payments_queue.json
}

# -----------------------------------------------------------------------------
# SNS — notifications
# -----------------------------------------------------------------------------

resource "aws_sns_topic" "alerts" {
  name = "${local.name}-alerts"
  tags = local.tags
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.notification_email
}

data "aws_iam_policy_document" "sns_events" {
  statement {
    sid    = "AllowEventBridge"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
    actions   = ["sns:Publish"]
    resources = [aws_sns_topic.alerts.arn]
  }
}

resource "aws_sns_topic_policy" "alerts" {
  arn    = aws_sns_topic.alerts.arn
  policy = data.aws_iam_policy_document.sns_events.json
}

# -----------------------------------------------------------------------------
# IAM + Lambdas
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
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:${data.aws_partition.current.partition}:logs:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "dynamodb:PutItem",
      "dynamodb:GetItem",
      "dynamodb:Query",
      "dynamodb:UpdateItem",
    ]
    resources = [aws_dynamodb_table.accounts.arn]
  }

  statement {
    effect    = "Allow"
    actions   = ["events:PutEvents"]
    resources = [aws_cloudwatch_event_bus.northstar.arn]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]
    resources = [
      aws_s3_bucket.partner.arn,
      "${aws_s3_bucket.partner.arn}/*",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
    ]
    resources = [aws_sqs_queue.payments.arn]
  }

  statement {
    effect    = "Allow"
    actions   = ["sns:Publish"]
    resources = [aws_sns_topic.alerts.arn]
  }
}

resource "aws_iam_role_policy" "lambda" {
  name   = "${local.name}-lambda-policy"
  role   = aws_iam_role.lambda.id
  policy = data.aws_iam_policy_document.lambda.json
}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "${path.module}/lambda/handlers.py"
  output_path = "${path.module}/lambda/handlers.zip"
}

resource "aws_cloudwatch_log_group" "account_api" {
  name              = "/aws/lambda/${local.name}-account-api"
  retention_in_days = 7
  tags              = local.tags
}

resource "aws_cloudwatch_log_group" "payment_processor" {
  name              = "/aws/lambda/${local.name}-payment-processor"
  retention_in_days = 7
  tags              = local.tags
}

resource "aws_cloudwatch_log_group" "partner_file" {
  name              = "/aws/lambda/${local.name}-partner-file"
  retention_in_days = 7
  tags              = local.tags
}

resource "aws_cloudwatch_log_group" "analytics" {
  name              = "/aws/lambda/${local.name}-analytics"
  retention_in_days = 7
  tags              = local.tags
}

resource "aws_cloudwatch_log_group" "notification_prep" {
  name              = "/aws/lambda/${local.name}-notification-prep"
  retention_in_days = 7
  tags              = local.tags
}

locals {
  lambda_env = {
    ACCOUNTS_TABLE    = aws_dynamodb_table.accounts.name
    EVENT_BUS_NAME    = aws_cloudwatch_event_bus.northstar.name
    PARTNER_BUCKET    = aws_s3_bucket.partner.bucket
    PAYMENT_QUEUE_URL = aws_sqs_queue.payments.url
  }
}

resource "aws_lambda_function" "account_api" {
  function_name    = "${local.name}-account-api"
  role             = aws_iam_role.lambda.arn
  handler          = "handlers.account_api_handler"
  runtime          = "python3.12"
  timeout          = 15
  memory_size      = 128
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256
  environment { variables = local.lambda_env }
  depends_on = [aws_cloudwatch_log_group.account_api, aws_iam_role_policy.lambda]
  tags       = merge(local.tags, { Name = "${local.name}-account-api" })
}

resource "aws_lambda_function" "payment_processor" {
  function_name    = "${local.name}-payment-processor"
  role             = aws_iam_role.lambda.arn
  handler          = "handlers.payment_processor_handler"
  runtime          = "python3.12"
  timeout          = 30
  memory_size      = 128
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256
  environment { variables = local.lambda_env }
  depends_on = [aws_cloudwatch_log_group.payment_processor, aws_iam_role_policy.lambda]
  tags       = merge(local.tags, { Name = "${local.name}-payment-processor" })
}

resource "aws_lambda_event_source_mapping" "payments" {
  event_source_arn = aws_sqs_queue.payments.arn
  function_name    = aws_lambda_function.payment_processor.arn
  batch_size       = 5
  enabled          = true
}

resource "aws_lambda_function" "partner_file" {
  function_name    = "${local.name}-partner-file"
  role             = aws_iam_role.lambda.arn
  handler          = "handlers.partner_file_handler"
  runtime          = "python3.12"
  timeout          = 30
  memory_size      = 128
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256
  environment { variables = local.lambda_env }
  depends_on = [aws_cloudwatch_log_group.partner_file, aws_iam_role_policy.lambda]
  tags       = merge(local.tags, { Name = "${local.name}-partner-file" })
}

resource "aws_lambda_permission" "s3_partner" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.partner_file.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.partner.arn
}

resource "aws_lambda_function" "analytics" {
  function_name    = "${local.name}-analytics"
  role             = aws_iam_role.lambda.arn
  handler          = "handlers.analytics_handler"
  runtime          = "python3.12"
  timeout          = 15
  memory_size      = 128
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256
  environment { variables = local.lambda_env }
  depends_on = [aws_cloudwatch_log_group.analytics, aws_iam_role_policy.lambda]
  tags       = merge(local.tags, { Name = "${local.name}-analytics" })
}

resource "aws_lambda_function" "notification_prep" {
  function_name    = "${local.name}-notification-prep"
  role             = aws_iam_role.lambda.arn
  handler          = "handlers.notification_prep_handler"
  runtime          = "python3.12"
  timeout          = 10
  memory_size      = 128
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256
  environment { variables = local.lambda_env }
  depends_on = [aws_cloudwatch_log_group.notification_prep, aws_iam_role_policy.lambda]
  tags       = merge(local.tags, { Name = "${local.name}-notification-prep" })
}

# -----------------------------------------------------------------------------
# API Gateway HTTP API — account APIs
# -----------------------------------------------------------------------------

resource "aws_apigatewayv2_api" "accounts" {
  name          = "${local.name}-accounts-api"
  protocol_type = "HTTP"
  tags          = local.tags
}

resource "aws_apigatewayv2_integration" "accounts" {
  api_id                 = aws_apigatewayv2_api.accounts.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.account_api.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "get_account" {
  api_id    = aws_apigatewayv2_api.accounts.id
  route_key = "GET /accounts/{accountId}"
  target    = "integrations/${aws_apigatewayv2_integration.accounts.id}"
}

resource "aws_apigatewayv2_route" "create_account" {
  api_id    = aws_apigatewayv2_api.accounts.id
  route_key = "POST /accounts"
  target    = "integrations/${aws_apigatewayv2_integration.accounts.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.accounts.id
  name        = "$default"
  auto_deploy = true
  tags        = local.tags
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.account_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.accounts.execution_arn}/*/*"
}

# -----------------------------------------------------------------------------
# Step Functions — regulatory batch orchestration
# -----------------------------------------------------------------------------

data "aws_iam_policy_document" "sfn_assume" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["states.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "sfn" {
  name               = "${local.name}-sfn-role"
  assume_role_policy = data.aws_iam_policy_document.sfn_assume.json
  tags               = local.tags
}

data "aws_iam_policy_document" "sfn" {
  statement {
    effect  = "Allow"
    actions = ["lambda:InvokeFunction"]
    resources = [
      aws_lambda_function.analytics.arn,
      aws_lambda_function.notification_prep.arn,
    ]
  }

  statement {
    effect    = "Allow"
    actions   = ["sns:Publish"]
    resources = [aws_sns_topic.alerts.arn]
  }
}

resource "aws_iam_role_policy" "sfn" {
  name   = "${local.name}-sfn-policy"
  role   = aws_iam_role.sfn.id
  policy = data.aws_iam_policy_document.sfn.json
}

resource "aws_sfn_state_machine" "regulatory_batch" {
  name     = "${local.name}-regulatory-batch"
  role_arn = aws_iam_role.sfn.arn

  definition = templatefile("${path.module}/stepfunctions/regulatory_batch.asl.json", {
    analytics_lambda_arn    = aws_lambda_function.analytics.arn
    notification_lambda_arn = aws_lambda_function.notification_prep.arn
    sns_topic_arn           = aws_sns_topic.alerts.arn
  })

  tags = local.tags

  depends_on = [aws_iam_role_policy.sfn]
}
