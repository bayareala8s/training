terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.4"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5"
    }
  }
}

variable "name_prefix" {
  type = string
}

variable "student_id" {
  type = string
}

variable "expiration_date" {
  type = string
}

variable "use_mock_bedrock" {
  description = "When true, skip Bedrock and use deterministic mock classifier."
  type        = bool
  default     = true
}

variable "bedrock_model_id" {
  description = "Bedrock model ID used when use_mock_bedrock is false."
  type        = string
  default     = "amazon.nova-micro-v1:0"
}

variable "enable_guardrails" {
  description = "Optional Bedrock Guardrail (only meaningful in live mode)."
  type        = bool
  default     = false
}

variable "tags" {
  type    = map(string)
  default = {}
}

locals {
  required_tags = {
    Project        = "BayLearn"
    Course         = "EnterpriseArchitectureLeadership"
    Module         = "08"
    Student        = var.student_id
    Environment    = "Lab"
    ExpirationDate = var.expiration_date
  }
  tags = merge(local.required_tags, var.tags)
}

data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}
data "aws_region" "current" {}

resource "random_id" "suffix" {
  byte_length = 3
}

resource "random_password" "api_token" {
  length  = 32
  special = false
}

resource "aws_s3_bucket" "artifacts" {
  bucket = "${var.name_prefix}-ai-${random_id.suffix.hex}"
  tags   = local.tags
}

resource "aws_s3_bucket_public_access_block" "artifacts" {
  bucket                  = aws_s3_bucket.artifacts.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_object" "system_prompt" {
  bucket       = aws_s3_bucket.artifacts.id
  key          = "prompts/system-prompt.txt"
  content      = <<-EOT
    You are NorthStar Financial Services (fictional) incident triage assistant.
    Return ONLY valid JSON with keys: category, severity, business_impact, routing_team, next_actions, hitl_required, confidence, rationale.
  EOT
  content_type = "text/plain"
  tags         = local.tags
}

resource "aws_dynamodb_table" "decisions" {
  name         = "${var.name_prefix}-decisions"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "incident_id"

  attribute {
    name = "incident_id"
    type = "S"
  }

  tags = local.tags
}

# Optional Guardrail (live mode teaching aid)
resource "aws_bedrock_guardrail" "lab" {
  count                     = var.enable_guardrails ? 1 : 0
  name                      = "${var.name_prefix}-guardrail"
  blocked_input_messaging   = "Input blocked by BayLearn lab guardrail."
  blocked_outputs_messaging = "Output blocked by BayLearn lab guardrail."
  description               = "Optional instructional guardrail for Module 08"

  content_policy_config {
    filters_config {
      input_strength  = "MEDIUM"
      output_strength = "MEDIUM"
      type            = "HATE"
    }
    filters_config {
      input_strength  = "MEDIUM"
      output_strength = "MEDIUM"
      type            = "VIOLENCE"
    }
  }

  tags = local.tags
}

resource "aws_bedrock_guardrail_version" "lab" {
  count         = var.enable_guardrails ? 1 : 0
  guardrail_arn = aws_bedrock_guardrail.lab[0].guardrail_arn
  description   = "lab"
  skip_destroy  = false
}

data "archive_file" "infer" {
  type        = "zip"
  output_path = "${path.module}/lambda/infer.zip"
  source {
    content  = file("${path.module}/lambda/infer.py")
    filename = "infer.py"
  }
}

data "archive_file" "validate" {
  type        = "zip"
  output_path = "${path.module}/lambda/validate.zip"
  source {
    content  = file("${path.module}/lambda/validate.py")
    filename = "validate.py"
  }
}

data "archive_file" "api" {
  type        = "zip"
  output_path = "${path.module}/lambda/api.zip"
  source {
    content  = file("${path.module}/lambda/api.py")
    filename = "api.py"
  }
}

resource "aws_iam_role" "lambda" {
  name = "${var.name_prefix}-ai-lambda"
  tags = local.tags
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "lambda" {
  name = "ai-lab-permissions"
  role = aws_iam_role.lambda.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:${data.aws_partition.current.partition}:logs:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:*"
      },
      {
        Effect   = "Allow"
        Action   = ["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:UpdateItem", "dynamodb:Query"]
        Resource = [aws_dynamodb_table.decisions.arn]
      },
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject", "s3:GetObject"]
        Resource = ["${aws_s3_bucket.artifacts.arn}/*"]
      },
      {
        Effect   = "Allow"
        Action   = ["cloudwatch:PutMetricData"]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "states:StartExecution",
          "states:DescribeExecution",
          "states:GetExecutionHistory"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream",
          "bedrock:Converse",
          "bedrock:ConverseStream",
          "bedrock:ApplyGuardrail"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_lambda_function" "infer" {
  function_name    = "${var.name_prefix}-infer"
  role             = aws_iam_role.lambda.arn
  handler          = "infer.handler"
  runtime          = "python3.12"
  filename         = data.archive_file.infer.output_path
  source_code_hash = data.archive_file.infer.output_base64sha256
  timeout          = 60
  memory_size      = 256
  tags             = local.tags

  environment {
    variables = {
      USE_MOCK_BEDROCK  = var.use_mock_bedrock ? "true" : "false"
      BEDROCK_MODEL_ID  = var.bedrock_model_id
      METRIC_NAMESPACE  = "BayLearn/Lab08"
      PROMPT_BUCKET     = aws_s3_bucket.artifacts.bucket
      GUARDRAIL_ID      = var.enable_guardrails ? aws_bedrock_guardrail.lab[0].guardrail_id : ""
      GUARDRAIL_VERSION = var.enable_guardrails ? aws_bedrock_guardrail_version.lab[0].version : ""
    }
  }
}

resource "aws_lambda_function" "validate" {
  function_name    = "${var.name_prefix}-validate"
  role             = aws_iam_role.lambda.arn
  handler          = "validate.handler"
  runtime          = "python3.12"
  filename         = data.archive_file.validate.output_path
  source_code_hash = data.archive_file.validate.output_base64sha256
  timeout          = 30
  memory_size      = 256
  tags             = local.tags

  environment {
    variables = {
      DECISIONS_TABLE = aws_dynamodb_table.decisions.name
    }
  }
}

resource "aws_iam_role" "sfn" {
  name = "${var.name_prefix}-ai-sfn"
  tags = local.tags
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "states.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "sfn" {
  name = "invoke-lambdas"
  role = aws_iam_role.sfn.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["lambda:InvokeFunction"]
      Resource = [aws_lambda_function.infer.arn, aws_lambda_function.validate.arn]
    }]
  })
}

resource "aws_sfn_state_machine" "assistant" {
  name     = "${var.name_prefix}-ai-assistant"
  role_arn = aws_iam_role.sfn.arn
  tags     = local.tags

  definition = jsonencode({
    Comment = "BayLearn Module 08 AI decision assistant"
    StartAt = "Infer"
    States = {
      Infer = {
        Type     = "Task"
        Resource = "arn:aws:states:::lambda:invoke"
        Parameters = {
          FunctionName = aws_lambda_function.infer.arn
          "Payload.$"  = "$"
        }
        ResultSelector = {
          "incident_id.$"   = "$.Payload.incident_id"
          "incident_text.$" = "$.Payload.incident_text"
          "decision.$"      = "$.Payload.decision"
          "metrics.$"       = "$.Payload.metrics"
        }
        Next = "ValidateAndRoute"
      }
      ValidateAndRoute = {
        Type     = "Task"
        Resource = "arn:aws:states:::lambda:invoke"
        Parameters = {
          FunctionName = aws_lambda_function.validate.arn
          "Payload.$"  = "$"
        }
        OutputPath = "$.Payload"
        End        = true
      }
    }
  })
}

resource "aws_lambda_function" "api" {
  function_name    = "${var.name_prefix}-api"
  role             = aws_iam_role.lambda.arn
  handler          = "api.handler"
  runtime          = "python3.12"
  filename         = data.archive_file.api.output_path
  source_code_hash = data.archive_file.api.output_base64sha256
  timeout          = 60
  memory_size      = 256
  tags             = local.tags

  environment {
    variables = {
      STATE_MACHINE_ARN = aws_sfn_state_machine.assistant.arn
      LAB_API_TOKEN     = random_password.api_token.result
    }
  }
}

resource "aws_apigatewayv2_api" "http" {
  name          = "${var.name_prefix}-ai-api"
  protocol_type = "HTTP"
  tags          = local.tags
}

resource "aws_apigatewayv2_integration" "api" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.api.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "decisions" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /decisions"
  target    = "integrations/${aws_apigatewayv2_integration.api.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
  tags        = local.tags
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}

output "name_prefix" {
  value = var.name_prefix
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.http.api_endpoint
}

output "api_token" {
  value     = random_password.api_token.result
  sensitive = true
}

output "state_machine_arn" {
  value = aws_sfn_state_machine.assistant.arn
}

output "decisions_table_name" {
  value = aws_dynamodb_table.decisions.name
}

output "artifacts_bucket" {
  value = aws_s3_bucket.artifacts.bucket
}

output "infer_lambda_name" {
  value = aws_lambda_function.infer.function_name
}

output "validate_lambda_name" {
  value = aws_lambda_function.validate.function_name
}

output "use_mock_bedrock" {
  value = var.use_mock_bedrock
}

output "bedrock_model_id" {
  value = var.bedrock_model_id
}

output "bedrock_enablement_notes" {
  value = <<-EOT
    LIVE MODE: In Bedrock console (${data.aws_region.current.id}), enable model access for '${var.bedrock_model_id}', then set use_mock_bedrock=false and re-apply.
    MOCK MODE (default): Deterministic classifier — lab teaches architecture, validation, HITL, eval without model access.
    Optional Guardrails: enable_guardrails=true (may require additional account permissions).
  EOT
}
