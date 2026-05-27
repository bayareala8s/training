locals {
  large_inbound_prefix   = "${local.partner_prefix}/large/inbound/"
  large_processed_prefix = "${local.partner_prefix}/large/processed/"
}

module "networking" {
  count  = var.enable_ecs_worker ? 1 : 0
  source = "../../modules/networking"

  name_prefix = local.name_prefix
  aws_region  = data.aws_region.current.id
  tags        = local.tags
}

module "ecs_worker" {
  count  = var.enable_ecs_worker ? 1 : 0
  source = "../../modules/ecs_worker"

  name_prefix        = local.name_prefix
  aws_region         = data.aws_region.current.id
  landing_bucket_arn = module.landing_bucket.bucket_arn
  kms_key_arn        = module.kms.key_arn
  task_cpu           = var.ecs_task_cpu
  task_memory        = var.ecs_task_memory
  image_tag          = var.ecs_image_tag
  force_delete       = var.force_destroy
  tags               = local.tags
}

resource "aws_iam_role_policy" "lambda_ecs_dispatch" {
  count = var.enable_ecs_worker ? 1 : 0
  name  = "${local.name_prefix}-lambda-ecs"
  role  = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["ecs:RunTask"]
        Resource = module.ecs_worker[0].task_definition_arn
        Condition = {
          ArnEquals = {
            "ecs:cluster" = module.ecs_worker[0].cluster_arn
          }
        }
      },
      {
        Effect   = "Allow"
        Action   = ["ecs:DescribeTasks", "ecs:DescribeTaskDefinition"]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = ["iam:PassRole"]
        Resource = [
          module.ecs_worker[0].execution_role_arn,
          module.ecs_worker[0].task_role_arn,
        ]
      }
    ]
  })
}

data "archive_file" "ecs_dispatcher_zip" {
  count       = var.enable_ecs_worker ? 1 : 0
  type        = "zip"
  source_dir  = "${path.module}/../../../app/lambdas/ecs_dispatcher"
  output_path = "${path.module}/.build/ecs_dispatcher.zip"
}

resource "aws_lambda_function" "ecs_dispatcher" {
  count            = var.enable_ecs_worker ? 1 : 0
  function_name    = "${local.name_prefix}-ecs-dispatcher"
  role             = aws_iam_role.lambda.arn
  handler          = "handler.handler"
  runtime          = "python3.11"
  timeout          = 60
  filename         = data.archive_file.ecs_dispatcher_zip[0].output_path
  source_code_hash = data.archive_file.ecs_dispatcher_zip[0].output_base64sha256

  environment {
    variables = {
      ECS_CLUSTER     = module.ecs_worker[0].cluster_name
      TASK_DEFINITION = module.ecs_worker[0].task_definition_family
      SUBNETS         = join(",", module.networking[0].public_subnet_ids)
      SECURITY_GROUPS = module.networking[0].ecs_security_group_id
      DEST_PREFIX     = local.large_processed_prefix
    }
  }

  tags = local.tags

  depends_on = [module.ecs_worker, module.networking]
}

resource "aws_lambda_permission" "s3_invoke_ecs_dispatcher" {
  count         = var.enable_ecs_worker ? 1 : 0
  statement_id  = "AllowS3InvokeEcsDispatcher"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ecs_dispatcher[0].function_name
  principal     = "s3.amazonaws.com"
  source_arn    = module.landing_bucket.bucket_arn
}

# S3 bucket notifications are merged in lambda.tf (aws_s3_bucket_notification.landing).
