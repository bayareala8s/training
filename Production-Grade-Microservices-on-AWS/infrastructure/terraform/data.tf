resource "aws_cloudwatch_event_bus" "platform" {
  name = "${local.name_prefix}-bus"
  tags = local.common_tags
}

resource "aws_cloudwatch_event_rule" "order_placed" {
  name           = "${local.name_prefix}-order-placed"
  event_bus_name = aws_cloudwatch_event_bus.platform.name
  event_pattern = jsonencode({
    "detail-type" = ["OrderPlaced"]
    source        = ["course.orders"]
  })
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "eventbridge_orders" {
  name              = "/eventbridge/${local.name_prefix}/orders"
  retention_in_days = 7
  tags              = local.common_tags
}

resource "aws_cloudwatch_log_resource_policy" "eventbridge" {
  policy_name = "${local.name_prefix}-eventbridge-logs"
  policy_document = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid    = "AllowEventBridge"
      Effect = "Allow"
      Principal = {
        Service = ["events.amazonaws.com", "delivery.logs.amazonaws.com"]
      }
      Action   = ["logs:CreateLogStream", "logs:PutLogEvents"]
      Resource = "${aws_cloudwatch_log_group.eventbridge_orders.arn}:*"
    }]
  })
}

resource "aws_cloudwatch_event_target" "order_placed_logs" {
  rule           = aws_cloudwatch_event_rule.order_placed.name
  event_bus_name = aws_cloudwatch_event_bus.platform.name
  arn            = aws_cloudwatch_log_group.eventbridge_orders.arn
  target_id      = "OrderPlacedLogs"

  depends_on = [aws_cloudwatch_log_resource_policy.eventbridge]
}

resource "aws_dynamodb_table" "orders" {
  name         = "${local.name_prefix}-orders"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }

  tags = local.common_tags
}

resource "aws_ecr_repository" "services" {
  for_each = local.services
  name     = "${local.name_prefix}-${each.key}"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/${local.name_prefix}"
  retention_in_days = 7
  tags              = local.common_tags
}
