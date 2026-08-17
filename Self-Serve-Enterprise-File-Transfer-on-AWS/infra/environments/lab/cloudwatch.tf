resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "${local.name_prefix}-lambda-errors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 1
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.s3_processor.function_name
  }

  alarm_description = "BayLearn Lab 7: S3 processor Lambda errors"
  tags              = local.tags
}

resource "aws_cloudwatch_metric_alarm" "sfn_failed" {
  alarm_name          = "${local.name_prefix}-sfn-failed"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "ExecutionsFailed"
  namespace           = "AWS/States"
  period              = 900
  statistic           = "Sum"
  threshold           = 1
  treat_missing_data  = "notBreaching"

  dimensions = {
    StateMachineArn = aws_sfn_state_machine.transfer.arn
  }

  alarm_description = "BayLearn Lab 7: Step Functions failures"
  tags              = local.tags
}

resource "aws_cloudwatch_dashboard" "lab" {
  dashboard_name = "${local.name_prefix}-ops"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          title  = "Lambda Errors"
          region = data.aws_region.current.id
          metrics = [
            ["AWS/Lambda", "Errors", "FunctionName", aws_lambda_function.s3_processor.function_name],
            [".", ".", ".", aws_lambda_function.workflow_validate.function_name],
            [".", ".", ".", aws_lambda_function.api.function_name],
          ]
          stat = "Sum"
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          title  = "Step Functions"
          region = data.aws_region.current.id
          metrics = [
            ["AWS/States", "ExecutionsSucceeded", "StateMachineArn", aws_sfn_state_machine.transfer.arn],
            ["AWS/States", "ExecutionsFailed", "StateMachineArn", aws_sfn_state_machine.transfer.arn],
          ]
          stat = "Sum"
        }
      }
    ]
  })
}
