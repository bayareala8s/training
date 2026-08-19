#!/usr/bin/env python3
"""Emit remaining lab Terraform (valid HCL)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


HEADER = '''terraform {{
  required_version = ">= 1.5.0"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = ">= 5.50"
    }}
    archive = {{
      source  = "hashicorp/archive"
      version = ">= 2.4"
    }}
    random = {{
      source  = "hashicorp/random"
      version = ">= 3.5"
    }}
  }}
}}

provider "aws" {{
  region = var.aws_region
  default_tags {{
    tags = {{
      Project = "baylearn-eia"
      Lab     = "{lab}"
    }}
  }}
}}

variable "aws_region" {{
  type    = string
  default = "us-west-2"
}}

resource "random_string" "suffix" {{
  length  = 6
  special = false
  upper   = false
}}

locals {{
  name = "{prefix}-${{random_string.suffix.result}}"
}}
'''


def write(lab: str, body: str) -> None:
    p = ROOT / "terraform" / "labs" / lab / "main.tf"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    (p.parent / "terraform.tfvars.example").write_text('aws_region = "us-west-2"\n', encoding="utf-8")
    print(p)


def assume():
    return '''jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })'''


def lab04():
    write("lab-04-pubsub", HEADER.format(lab="lab-04-pubsub", prefix="eia-lab04") + f'''
resource "aws_sns_topic" "orders" {{
  name = "${{local.name}}-orders"
}}

resource "aws_sqs_queue" "inv" {{ name = "${{local.name}}-inv" }}
resource "aws_sqs_queue" "ntf" {{ name = "${{local.name}}-ntf" }}
resource "aws_sqs_queue" "an"  {{ name = "${{local.name}}-an" }}

resource "aws_sns_topic_subscription" "inv" {{
  topic_arn = aws_sns_topic.orders.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.inv.arn
}}
resource "aws_sns_topic_subscription" "ntf" {{
  topic_arn = aws_sns_topic.orders.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.ntf.arn
}}
resource "aws_sns_topic_subscription" "an" {{
  topic_arn = aws_sns_topic.orders.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.an.arn
}}

resource "aws_sqs_queue_policy" "allow_sns" {{
  for_each = {{
    inv = aws_sqs_queue.inv
    ntf = aws_sqs_queue.ntf
    an  = aws_sqs_queue.an
  }}
  queue_url = each.value.id
  policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [{{
      Effect    = "Allow"
      Principal = {{ Service = "sns.amazonaws.com" }}
      Action    = "sqs:SendMessage"
      Resource  = each.value.arn
      Condition = {{ ArnEquals = {{ "aws:SourceArn" = aws_sns_topic.orders.arn }} }}
    }}]
  }})
}}

resource "aws_dynamodb_table" "t" {{
  name         = "${{local.name}}-proj"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {{
    name = "pk"
    type = "S"
  }}
}}

{lambda_sqs("inv", "lab04_inventory", "aws_sqs_queue.inv")}
{lambda_sqs("ntf", "lab04_notify", "aws_sqs_queue.ntf")}
{lambda_sqs("an", "lab04_analytics", "aws_sqs_queue.an")}

output "topic_arn" {{ value = aws_sns_topic.orders.arn }}
output "table_name" {{ value = aws_dynamodb_table.t.name }}
''')


def lambda_sqs(id_, dir_, queue_ref):
    return f'''
data "archive_file" "{id_}" {{
  type        = "zip"
  output_path = "${{path.module}}/.build/{id_}.zip"
  source_dir  = "${{path.module}}/../../../lambda/{dir_}"
}}
resource "aws_iam_role" "{id_}" {{
  name               = "${{local.name}}-{id_}"
  assume_role_policy = {assume()}
}}
resource "aws_iam_role_policy" "{id_}" {{
  role = aws_iam_role.{id_}.id
  policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{ Effect = "Allow" Action = ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"] Resource = "*" }},
      {{ Effect = "Allow" Action = ["sqs:ReceiveMessage","sqs:DeleteMessage","sqs:GetQueueAttributes"] Resource = {queue_ref}.arn }},
      {{ Effect = "Allow" Action = ["dynamodb:PutItem"] Resource = aws_dynamodb_table.t.arn }}
    ]
  }})
}}
resource "aws_lambda_function" "{id_}" {{
  function_name    = "${{local.name}}-{id_}"
  role             = aws_iam_role.{id_}.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.{id_}.output_path
  source_code_hash = data.archive_file.{id_}.output_base64sha256
  timeout          = 15
  environment {{
    variables = {{ TABLE_NAME = aws_dynamodb_table.t.name }}
  }}
}}
resource "aws_lambda_event_source_mapping" "{id_}" {{
  event_source_arn = {queue_ref}.arn
  function_name    = aws_lambda_function.{id_}.arn
  batch_size       = 1
}}
'''


def lab05():
    write("lab-05-events", HEADER.format(lab="lab-05-events", prefix="eia-lab05") + f'''
resource "aws_cloudwatch_event_bus" "bus" {{
  name = "${{local.name}}-bus"
}}
resource "aws_dynamodb_table" "t" {{
  name         = "${{local.name}}-proj"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {{
    name = "pk"
    type = "S"
  }}
}}
{eb_lambda("pay", "lab05_payment", "OrderCreated")}
{eb_lambda("inv", "lab05_inventory", "PaymentAuthorized")}
{eb_lambda("done", "lab05_notify", "InventoryReserved")}
output "bus_name" {{ value = aws_cloudwatch_event_bus.bus.name }}
output "table_name" {{ value = aws_dynamodb_table.t.name }}
''')


def eb_lambda(id_, dir_, detail_type):
    return f'''
data "archive_file" "{id_}" {{
  type        = "zip"
  output_path = "${{path.module}}/.build/{id_}.zip"
  source_dir  = "${{path.module}}/../../../lambda/{dir_}"
}}
resource "aws_iam_role" "{id_}" {{
  name               = "${{local.name}}-{id_}"
  assume_role_policy = {assume()}
}}
resource "aws_iam_role_policy" "{id_}" {{
  role = aws_iam_role.{id_}.id
  policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{ Effect = "Allow" Action = ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"] Resource = "*" }},
      {{ Effect = "Allow" Action = ["events:PutEvents"] Resource = "*" }},
      {{ Effect = "Allow" Action = ["dynamodb:PutItem"] Resource = aws_dynamodb_table.t.arn }}
    ]
  }})
}}
resource "aws_lambda_function" "{id_}" {{
  function_name    = "${{local.name}}-{id_}"
  role             = aws_iam_role.{id_}.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.{id_}.output_path
  source_code_hash = data.archive_file.{id_}.output_base64sha256
  timeout          = 15
  environment {{
    variables = {{
      TABLE_NAME = aws_dynamodb_table.t.name
      BUS_NAME   = aws_cloudwatch_event_bus.bus.name
    }}
  }}
}}
resource "aws_cloudwatch_event_rule" "{id_}" {{
  name           = "${{local.name}}-{id_}"
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  event_pattern  = jsonencode({{ "detail-type" = ["{detail_type}"] }})
}}
resource "aws_cloudwatch_event_target" "{id_}" {{
  rule           = aws_cloudwatch_event_rule.{id_}.name
  event_bus_name = aws_cloudwatch_event_bus.bus.name
  arn            = aws_lambda_function.{id_}.arn
}}
resource "aws_lambda_permission" "{id_}" {{
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.{id_}.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.{id_}.arn
}}
'''


def lab06():
    write("lab-06-file-transfer", HEADER.format(lab="lab-06-file-transfer", prefix="eia-lab06") + f'''
variable "enable_transfer_family" {{
  type    = bool
  default = false
}}

resource "aws_s3_bucket" "land" {{
  bucket        = "${{local.name}}-land"
  force_destroy = true
}}
resource "aws_s3_bucket_public_access_block" "land" {{
  bucket                  = aws_s3_bucket.land.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}}
resource "aws_s3_bucket_versioning" "land" {{
  bucket = aws_s3_bucket.land.id
  versioning_configuration {{ status = "Enabled" }}
}}
resource "aws_sqs_queue" "q" {{ name = "${{local.name}}-val" }}
resource "aws_s3_bucket_notification" "n" {{
  bucket = aws_s3_bucket.land.id
  queue {{
    queue_arn     = aws_sqs_queue.q.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "inbound/"
  }}
  depends_on = [aws_sqs_queue_policy.s3]
}}
resource "aws_sqs_queue_policy" "s3" {{
  queue_url = aws_sqs_queue.q.id
  policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [{{
      Effect    = "Allow"
      Principal = {{ Service = "s3.amazonaws.com" }}
      Action    = "sqs:SendMessage"
      Resource  = aws_sqs_queue.q.arn
      Condition = {{ ArnEquals = {{ "aws:SourceArn" = aws_s3_bucket.land.arn }} }}
    }}]
  }})
}}
resource "aws_dynamodb_table" "cat" {{
  name         = "${{local.name}}-catalog"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {{
    name = "pk"
    type = "S"
  }}
}}
data "archive_file" "fn" {{
  type        = "zip"
  output_path = "${{path.module}}/.build/val.zip"
  source_dir  = "${{path.module}}/../../../lambda/lab06_validate"
}}
resource "aws_iam_role" "fn" {{
  name               = "${{local.name}}-val"
  assume_role_policy = {assume()}
}}
resource "aws_iam_role_policy" "fn" {{
  role = aws_iam_role.fn.id
  policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{ Effect = "Allow" Action = ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"] Resource = "*" }},
      {{ Effect = "Allow" Action = ["sqs:ReceiveMessage","sqs:DeleteMessage","sqs:GetQueueAttributes"] Resource = aws_sqs_queue.q.arn }},
      {{ Effect = "Allow" Action = ["s3:GetObject","s3:PutObject"] Resource = "${{aws_s3_bucket.land.arn}}/*" }},
      {{ Effect = "Allow" Action = ["dynamodb:PutItem"] Resource = aws_dynamodb_table.cat.arn }}
    ]
  }})
}}
resource "aws_lambda_function" "fn" {{
  function_name    = "${{local.name}}-val"
  role             = aws_iam_role.fn.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.fn.output_path
  source_code_hash = data.archive_file.fn.output_base64sha256
  timeout          = 30
  environment {{
    variables = {{ TABLE_NAME = aws_dynamodb_table.cat.name }}
  }}
}}
resource "aws_lambda_event_source_mapping" "m" {{
  event_source_arn = aws_sqs_queue.q.arn
  function_name    = aws_lambda_function.fn.arn
  batch_size       = 1
}}
output "bucket" {{ value = aws_s3_bucket.land.bucket }}
output "table_name" {{ value = aws_dynamodb_table.cat.name }}
output "enable_transfer_family" {{ value = var.enable_transfer_family }}
''')


def lab07():
    init_fn = gw_lambda("init", "lab07_init_upload", extra_env="BUCKET = aws_s3_bucket.b.bucket")
    status_fn = gw_lambda("status", "lab07_status")
    write("lab-07-large-files", HEADER.format(lab="lab-07-large-files", prefix="eia-lab07") + f'''
resource "aws_s3_bucket" "b" {{
  bucket        = "${{local.name}}-up"
  force_destroy = true
}}
resource "aws_s3_bucket_public_access_block" "b" {{
  bucket                  = aws_s3_bucket.b.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}}
resource "aws_s3_bucket_lifecycle_configuration" "abort" {{
  bucket = aws_s3_bucket.b.id
  rule {{
    id     = "abort-mpu"
    status = "Enabled"
    abort_incomplete_multipart_upload {{ days_after_initiation = 1 }}
    filter {{ prefix = "" }}
  }}
}}
resource "aws_dynamodb_table" "jobs" {{
  name         = "${{local.name}}-jobs"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {{
    name = "pk"
    type = "S"
  }}
}}
{init_fn}
{status_fn}
data "archive_file" "proc" {{
  type        = "zip"
  output_path = "${{path.module}}/.build/proc.zip"
  source_dir  = "${{path.module}}/../../../lambda/lab07_process"
}}
resource "aws_iam_role" "proc" {{
  name               = "${{local.name}}-proc"
  assume_role_policy = {assume()}
}}
resource "aws_iam_role_policy" "proc" {{
  role = aws_iam_role.proc.id
  policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{ Effect = "Allow" Action = ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"] Resource = "*" }},
      {{ Effect = "Allow" Action = ["s3:GetObject"] Resource = "${{aws_s3_bucket.b.arn}}/*" }},
      {{ Effect = "Allow" Action = ["dynamodb:UpdateItem"] Resource = aws_dynamodb_table.jobs.arn }}
    ]
  }})
}}
resource "aws_lambda_function" "proc" {{
  function_name    = "${{local.name}}-proc"
  role             = aws_iam_role.proc.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.proc.output_path
  source_code_hash = data.archive_file.proc.output_base64sha256
  timeout          = 60
  environment {{
    variables = {{ TABLE_NAME = aws_dynamodb_table.jobs.name }}
  }}
}}
resource "aws_s3_bucket_notification" "n" {{
  bucket = aws_s3_bucket.b.id
  lambda_function {{
    lambda_function_arn = aws_lambda_function.proc.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "inbound/"
  }}
  depends_on = [aws_lambda_permission.s3]
}}
resource "aws_lambda_permission" "s3" {{
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.proc.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.b.arn
}}
resource "aws_apigatewayv2_api" "http" {{
  name          = "${{local.name}}-http"
  protocol_type = "HTTP"
}}
resource "aws_apigatewayv2_integration" "init" {{
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.init.invoke_arn
  payload_format_version = "2.0"
}}
resource "aws_apigatewayv2_integration" "status" {{
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.status.invoke_arn
  payload_format_version = "2.0"
}}
resource "aws_apigatewayv2_route" "post" {{
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /uploads"
  target    = "integrations/${{aws_apigatewayv2_integration.init.id}}"
}}
resource "aws_apigatewayv2_route" "get" {{
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "GET /uploads/{{id}}"
  target    = "integrations/${{aws_apigatewayv2_integration.status.id}}"
}}
resource "aws_apigatewayv2_stage" "default" {{
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
}}
resource "aws_lambda_permission" "apigw_init" {{
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.init.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${{aws_apigatewayv2_api.http.execution_arn}}/*/*"
}}
resource "aws_lambda_permission" "apigw_status" {{
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.status.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${{aws_apigatewayv2_api.http.execution_arn}}/*/*"
}}
output "api_endpoint" {{ value = aws_apigatewayv2_api.http.api_endpoint }}
output "bucket" {{ value = aws_s3_bucket.b.bucket }}
''')


def gw_lambda(id_, dir_, extra_env="", extra_iam=""):
    env = "TABLE_NAME = aws_dynamodb_table.jobs.name"
    if extra_env:
        env = env + "\\n      " + extra_env
    extra = extra_iam + "," if extra_iam else ""
    return f'''
data "archive_file" "{id_}" {{
  type        = "zip"
  output_path = "${{path.module}}/.build/{id_}.zip"
  source_dir  = "${{path.module}}/../../../lambda/{dir_}"
}}
resource "aws_iam_role" "{id_}" {{
  name               = "${{local.name}}-{id_}"
  assume_role_policy = {assume()}
}}
resource "aws_iam_role_policy" "{id_}" {{
  role = aws_iam_role.{id_}.id
  policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {extra}
      {{ Effect = "Allow" Action = ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"] Resource = "*" }},
      {{ Effect = "Allow" Action = ["dynamodb:PutItem","dynamodb:GetItem","dynamodb:UpdateItem"] Resource = aws_dynamodb_table.jobs.arn }}
    ]
  }})
}}
resource "aws_lambda_function" "{id_}" {{
  function_name    = "${{local.name}}-{id_}"
  role             = aws_iam_role.{id_}.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.{id_}.output_path
  source_code_hash = data.archive_file.{id_}.output_base64sha256
  timeout          = 15
  environment {{
    variables = {{
      {env}
    }}
  }}
}}
'''


def lab12():
    write("lab-12-security", HEADER.format(lab="lab-12-security", prefix="eia-lab12") + f'''
variable "insecure" {{
  type    = bool
  default = true
}}
resource "aws_s3_bucket" "b" {{
  bucket        = "${{local.name}}-data"
  force_destroy = true
}}
resource "aws_s3_bucket_public_access_block" "b" {{
  bucket                  = aws_s3_bucket.b.id
  block_public_acls       = !var.insecure
  block_public_policy     = !var.insecure
  ignore_public_acls      = !var.insecure
  restrict_public_buckets = !var.insecure
}}
resource "aws_dynamodb_table" "t" {{
  name         = "${{local.name}}-t"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {{
    name = "pk"
    type = "S"
  }}
}}
data "archive_file" "fn" {{
  type        = "zip"
  output_path = "${{path.module}}/.build/fix.zip"
  source_dir  = "${{path.module}}/../../../lambda/lab12_fix"
}}
resource "aws_iam_role" "fn" {{
  name               = "${{local.name}}-fn"
  assume_role_policy = {assume()}
}}
resource "aws_iam_role_policy" "fn" {{
  role = aws_iam_role.fn.id
  policy = var.insecure ? jsonencode({{
    Version = "2012-10-17"
    Statement = [{{ Effect = "Allow" Action = ["dynamodb:*","s3:*","logs:*"] Resource = "*" }}]
  }}) : jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{ Effect = "Allow" Action = ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"] Resource = "*" }},
      {{ Effect = "Allow" Action = ["dynamodb:GetItem","dynamodb:PutItem"] Resource = aws_dynamodb_table.t.arn }},
      {{ Effect = "Allow" Action = ["s3:GetObject"] Resource = "${{aws_s3_bucket.b.arn}}/allowed/*" }}
    ]
  }})
}}
resource "aws_lambda_function" "fn" {{
  function_name    = "${{local.name}}-fn"
  role             = aws_iam_role.fn.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.fn.output_path
  source_code_hash = data.archive_file.fn.output_base64sha256
}}
output "insecure" {{ value = var.insecure }}
output "bucket" {{ value = aws_s3_bucket.b.bucket }}
output "function_name" {{ value = aws_lambda_function.fn.function_name }}
''')
    (ROOT / "terraform/labs/lab-12-security/terraform.tfvars.example").write_text(
        'aws_region = "us-west-2"\ninsecure   = true\n', encoding="utf-8"
    )


def lab13():
    write("lab-13-observability", HEADER.format(lab="lab-13-observability", prefix="eia-lab13") + f'''
data "archive_file" "fn" {{
  type        = "zip"
  output_path = "${{path.module}}/.build/met.zip"
  source_dir  = "${{path.module}}/../../../lambda/lab13_metrics"
}}
resource "aws_iam_role" "fn" {{
  name               = "${{local.name}}-met"
  assume_role_policy = {assume()}
}}
resource "aws_iam_role_policy" "fn" {{
  role = aws_iam_role.fn.id
  policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{ Effect = "Allow" Action = ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"] Resource = "*" }},
      {{ Effect = "Allow" Action = ["cloudwatch:PutMetricData"] Resource = "*" }}
    ]
  }})
}}
resource "aws_lambda_function" "fn" {{
  function_name    = "${{local.name}}-met"
  role             = aws_iam_role.fn.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.fn.output_path
  source_code_hash = data.archive_file.fn.output_base64sha256
  environment {{
    variables = {{ METRIC_NS = "EIA/Lab13" }}
  }}
}}
resource "aws_cloudwatch_dashboard" "d" {{
  dashboard_name = "${{local.name}}-ops"
  dashboard_body = jsonencode({{
    widgets = [
      {{ "type": "metric", "x": 0, "y": 0, "width": 8, "height": 6, "properties": {{ "title": "Transactions", "metrics": [["EIA/Lab13", "Transactions"]], "region": var.aws_region, "stat": "Sum", "period": 60 }} }},
      {{ "type": "metric", "x": 8, "y": 0, "width": 8, "height": 6, "properties": {{ "title": "Success vs Failure", "metrics": [["EIA/Lab13", "Success"], ["EIA/Lab13", "Failure"]], "region": var.aws_region, "stat": "Sum", "period": 60 }} }},
      {{ "type": "metric", "x": 16, "y": 0, "width": 8, "height": 6, "properties": {{ "title": "Latency (ms)", "metrics": [["EIA/Lab13", "LatencyMs"]], "region": var.aws_region, "stat": "Average", "period": 60 }} }},
      {{ "type": "metric", "x": 0, "y": 6, "width": 8, "height": 6, "properties": {{ "title": "Queue depth", "metrics": [["EIA/Lab13", "QueueDepth"]], "region": var.aws_region, "stat": "Maximum", "period": 60 }} }},
      {{ "type": "metric", "x": 8, "y": 6, "width": 8, "height": 6, "properties": {{ "title": "DLQ", "metrics": [["EIA/Lab13", "DLQVisible"]], "region": var.aws_region, "stat": "Maximum", "period": 60 }} }},
      {{ "type": "metric", "x": 16, "y": 6, "width": 8, "height": 6, "properties": {{ "title": "File counts", "metrics": [["EIA/Lab13", "FileCounts"]], "region": var.aws_region, "stat": "Sum", "period": 60 }} }},
      {{ "type": "metric", "x": 0, "y": 12, "width": 8, "height": 6, "properties": {{ "title": "Processing duration (ms)", "metrics": [["EIA/Lab13", "ProcessingDurationMs"]], "region": var.aws_region, "stat": "Average", "period": 60 }} }}
    ]
  }})
}}
output "function_name" {{ value = aws_lambda_function.fn.function_name }}
output "dashboard_name" {{ value = aws_cloudwatch_dashboard.d.dashboard_name }}
''')


def lab15():
    write("lab-15-ai-agent", HEADER.format(lab="lab-15-ai-agent", prefix="eia-lab15") + f'''
variable "enable_bedrock" {{
  type    = bool
  default = false
}}
resource "aws_dynamodb_table" "catalog" {{
  name         = "${{local.name}}-catalog"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {{
    name = "pk"
    type = "S"
  }}
}}
resource "aws_dynamodb_table" "appr" {{
  name         = "${{local.name}}-appr"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  attribute {{
    name = "pk"
    type = "S"
  }}
}}
resource "aws_dynamodb_table_item" "demo" {{
  table_name = aws_dynamodb_table.catalog.name
  hash_key   = "pk"
  item = jsonencode({{
    pk            = {{ S = "FILE#demo.csv" }}
    status        = {{ S = "QUARANTINED" }}
    correlationId = {{ S = "demo-corr" }}
  }})
}}
data "archive_file" "fn" {{
  type        = "zip"
  output_path = "${{path.module}}/.build/tools.zip"
  source_dir  = "${{path.module}}/../../../lambda/lab15_tools"
}}
resource "aws_iam_role" "fn" {{
  name               = "${{local.name}}-tools"
  assume_role_policy = {assume()}
}}
resource "aws_iam_role_policy" "fn" {{
  role = aws_iam_role.fn.id
  policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{ Effect = "Allow" Action = ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"] Resource = "*" }},
      {{ Effect = "Allow" Action = ["dynamodb:GetItem","dynamodb:PutItem","dynamodb:UpdateItem"] Resource = [aws_dynamodb_table.catalog.arn, aws_dynamodb_table.appr.arn] }}
    ]
  }})
}}
resource "aws_lambda_function" "fn" {{
  function_name    = "${{local.name}}-tools"
  role             = aws_iam_role.fn.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.fn.output_path
  source_code_hash = data.archive_file.fn.output_base64sha256
  timeout          = 15
  environment {{
    variables = {{
      CATALOG_TABLE  = aws_dynamodb_table.catalog.name
      APPROVAL_TABLE = aws_dynamodb_table.appr.name
    }}
  }}
}}
resource "aws_apigatewayv2_api" "http" {{
  name          = "${{local.name}}-tools"
  protocol_type = "HTTP"
}}
resource "aws_apigatewayv2_integration" "fn" {{
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.fn.invoke_arn
  payload_format_version = "2.0"
}}
resource "aws_apigatewayv2_route" "post" {{
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /tools"
  target    = "integrations/${{aws_apigatewayv2_integration.fn.id}}"
}}
resource "aws_apigatewayv2_route" "approve" {{
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /approve"
  target    = "integrations/${{aws_apigatewayv2_integration.fn.id}}"
}}
resource "aws_apigatewayv2_stage" "default" {{
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
}}
resource "aws_lambda_permission" "apigw" {{
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.fn.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${{aws_apigatewayv2_api.http.execution_arn}}/*/*"
}}
output "tools_url" {{ value = "${{aws_apigatewayv2_api.http.api_endpoint}}/tools" }}
output "approve_url" {{ value = "${{aws_apigatewayv2_api.http.api_endpoint}}/approve" }}
output "enable_bedrock" {{ value = var.enable_bedrock }}
''')


if __name__ == "__main__":
    lab04()
    lab05()
    lab06()
    lab07()
    lab12()
    lab13()
    lab15()
