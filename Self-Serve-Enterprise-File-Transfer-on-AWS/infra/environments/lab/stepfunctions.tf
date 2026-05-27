resource "aws_iam_role" "sfn" {
  name = "${local.name_prefix}-sfn"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "states.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = local.tags
}

resource "aws_iam_role_policy" "sfn" {
  name = "${local.name_prefix}-sfn-invoke"
  role = aws_iam_role.sfn.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["lambda:InvokeFunction"]
      Resource = [
        aws_lambda_function.workflow_validate.arn,
        aws_lambda_function.workflow_copy.arn,
        aws_lambda_function.workflow_notify_success.arn,
        aws_lambda_function.workflow_notify_failure.arn,
      ]
    }]
  })
}

resource "aws_sfn_state_machine" "transfer" {
  name     = "${local.name_prefix}-transfer-workflow"
  role_arn = aws_iam_role.sfn.arn

  definition = templatefile("${path.module}/workflows/transfer-workflow.asl.json", {
    validate_lambda_arn       = aws_lambda_function.workflow_validate.arn
    copy_lambda_arn           = aws_lambda_function.workflow_copy.arn
    notify_success_lambda_arn = aws_lambda_function.workflow_notify_success.arn
    notify_failure_lambda_arn = aws_lambda_function.workflow_notify_failure.arn
  })

  tags = local.tags
}
