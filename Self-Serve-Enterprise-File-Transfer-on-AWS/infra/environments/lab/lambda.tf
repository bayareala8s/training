data "archive_file" "s3_processor_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../../app/lambdas/s3_processor"
  output_path = "${path.module}/.build/s3_processor.zip"
}

data "archive_file" "workflow_validate_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../../app/lambdas/workflow_validate"
  output_path = "${path.module}/.build/workflow_validate.zip"
}

data "archive_file" "workflow_copy_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../../app/lambdas/workflow_copy"
  output_path = "${path.module}/.build/workflow_copy.zip"
}

data "archive_file" "workflow_notify_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../../app/lambdas/workflow_notify"
  output_path = "${path.module}/.build/workflow_notify.zip"
}

data "archive_file" "api_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../../app/lambdas/api"
  output_path = "${path.module}/.build/api.zip"
}

resource "aws_iam_role" "lambda" {
  name = "${local.name_prefix}-lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = local.tags
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_data" {
  name = "${local.name_prefix}-lambda-data"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:ListBucket",
          "s3:GetObjectVersion", "s3:CopyObject"
        ]
        Resource = [
          module.landing_bucket.bucket_arn,
          "${module.landing_bucket.bucket_arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:UpdateItem",
          "dynamodb:Scan", "dynamodb:Query"
        ]
        Resource = [
          aws_dynamodb_table.idempotency.arn,
          aws_dynamodb_table.connections.arn,
          aws_dynamodb_table.jobs.arn
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:Encrypt", "kms:GenerateDataKey", "kms:DescribeKey"]
        Resource = module.kms.key_arn
      },
      {
        Effect   = "Allow"
        Action   = ["states:StartExecution"]
        Resource = aws_sfn_state_machine.transfer.arn
      },
      {
        Effect   = "Allow"
        Action   = ["sns:Publish"]
        Resource = [aws_sns_topic.workflow_success.arn, aws_sns_topic.workflow_failure.arn]
      }
    ]
  })
}

resource "aws_lambda_function" "s3_processor" {
  function_name    = "${local.name_prefix}-s3-processor"
  role             = aws_iam_role.lambda.arn
  handler          = "handler.handler"
  runtime          = "python3.11"
  timeout          = 60
  filename         = data.archive_file.s3_processor_zip.output_path
  source_code_hash = data.archive_file.s3_processor_zip.output_base64sha256

  environment {
    variables = {
      IDEMPOTENCY_TABLE = aws_dynamodb_table.idempotency.name
      INBOUND_PREFIX    = local.inbound_prefix
    }
  }

  tags = local.tags
}

resource "aws_lambda_permission" "s3_invoke" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = module.landing_bucket.bucket_arn
}

resource "aws_s3_bucket_notification" "landing" {
  bucket = module.landing_bucket.bucket_id

  lambda_function {
    lambda_function_arn = aws_lambda_function.s3_processor.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = local.inbound_prefix
  }

  dynamic "lambda_function" {
    for_each = var.enable_ecs_worker ? [1] : []
    content {
      lambda_function_arn = aws_lambda_function.ecs_dispatcher[0].arn
      events              = ["s3:ObjectCreated:*"]
      filter_prefix       = local.large_inbound_prefix
    }
  }

  depends_on = [aws_lambda_permission.s3_invoke]
}

resource "aws_lambda_function" "workflow_validate" {
  function_name    = "${local.name_prefix}-workflow-validate"
  role             = aws_iam_role.lambda.arn
  handler          = "handler.handler"
  runtime          = "python3.11"
  timeout          = 30
  filename         = data.archive_file.workflow_validate_zip.output_path
  source_code_hash = data.archive_file.workflow_validate_zip.output_base64sha256

  environment {
    variables = {
      LANDING_BUCKET = module.landing_bucket.bucket_id
      INBOUND_PREFIX = local.inbound_prefix
    }
  }

  tags = local.tags
}

resource "aws_lambda_function" "workflow_copy" {
  function_name    = "${local.name_prefix}-workflow-copy"
  role             = aws_iam_role.lambda.arn
  handler          = "handler.handler"
  runtime          = "python3.11"
  timeout          = 30
  filename         = data.archive_file.workflow_copy_zip.output_path
  source_code_hash = data.archive_file.workflow_copy_zip.output_base64sha256

  environment {
    variables = {
      INBOUND_PREFIX = local.inbound_prefix
    }
  }

  tags = local.tags
}

resource "aws_lambda_function" "workflow_notify_success" {
  function_name    = "${local.name_prefix}-workflow-notify-success"
  role             = aws_iam_role.lambda.arn
  handler          = "handler.handler"
  runtime          = "python3.11"
  timeout          = 15
  filename         = data.archive_file.workflow_notify_zip.output_path
  source_code_hash = data.archive_file.workflow_notify_zip.output_base64sha256

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.workflow_success.arn
    }
  }

  tags = local.tags
}

resource "aws_lambda_function" "workflow_notify_failure" {
  function_name    = "${local.name_prefix}-workflow-notify-failure"
  role             = aws_iam_role.lambda.arn
  handler          = "handler.handler"
  runtime          = "python3.11"
  timeout          = 15
  filename         = data.archive_file.workflow_notify_zip.output_path
  source_code_hash = data.archive_file.workflow_notify_zip.output_base64sha256

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.workflow_failure.arn
    }
  }

  tags = local.tags
}

resource "aws_lambda_function" "api" {
  function_name    = "${local.name_prefix}-api"
  role             = aws_iam_role.lambda.arn
  handler          = "handler.handler"
  runtime          = "python3.11"
  timeout          = 30
  filename         = data.archive_file.api_zip.output_path
  source_code_hash = data.archive_file.api_zip.output_base64sha256

  environment {
    variables = {
      CONNECTIONS_TABLE = aws_dynamodb_table.connections.name
      JOBS_TABLE        = aws_dynamodb_table.jobs.name
      IDEMPOTENCY_TABLE = aws_dynamodb_table.idempotency.name
      STATE_MACHINE_ARN = aws_sfn_state_machine.transfer.arn
      LANDING_BUCKET    = module.landing_bucket.bucket_id
      ALLOWED_PREFIX    = "${local.partner_prefix}/"
    }
  }

  tags = local.tags
}
