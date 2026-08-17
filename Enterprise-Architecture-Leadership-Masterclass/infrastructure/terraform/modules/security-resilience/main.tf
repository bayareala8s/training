locals {
  required_tags = {
    Project        = "BayLearn"
    Course         = "EnterpriseArchitectureLeadership"
    Module         = "07"
    Student        = var.student_id
    Environment    = "Lab"
    ExpirationDate = var.expiration_date
  }

  tags = merge(local.required_tags, var.tags)

  primary_bucket_name = "${var.name_prefix}-primary-${random_id.suffix.hex}"
  replica_bucket_name = "${var.name_prefix}-replica-${random_id.suffix.hex}"
}

resource "random_id" "suffix" {
  byte_length = 3
}

# -----------------------------------------------------------------------------
# KMS
# -----------------------------------------------------------------------------

data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}

resource "aws_kms_key" "lab" {
  description             = "BayLearn Module 07 lab CMK for ${var.student_id}"
  deletion_window_in_days = 7
  enable_key_rotation     = true
  tags                    = local.tags

  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "baylearn-m07-key-policy"
    Statement = [
      {
        Sid    = "RootAccountAdmin"
        Effect = "Allow"
        Principal = {
          AWS = "arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "AllowLabRolesUseKey"
        Effect = "Allow"
        Principal = {
          AWS = [
            aws_iam_role.settlement_writer.arn,
            aws_iam_role.settlement_reader.arn,
            aws_iam_role.evidence_auditor.arn,
          ]
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:DescribeKey"
        ]
        Resource = "*"
      }
    ]
  })

  depends_on = [
    aws_iam_role.settlement_writer,
    aws_iam_role.settlement_reader,
    aws_iam_role.evidence_auditor,
  ]
}

resource "aws_kms_alias" "lab" {
  name          = "alias/${var.name_prefix}-lab"
  target_key_id = aws_kms_key.lab.key_id
}

# -----------------------------------------------------------------------------
# IAM roles (least privilege)
# -----------------------------------------------------------------------------

data "aws_iam_policy_document" "assume_self" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "AWS"
      identifiers = ["arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
  }
}

resource "aws_iam_role" "settlement_writer" {
  name               = "${var.name_prefix}-settlement-writer"
  assume_role_policy = data.aws_iam_policy_document.assume_self.json
  tags               = local.tags
}

resource "aws_iam_role" "settlement_reader" {
  name               = "${var.name_prefix}-settlement-reader"
  assume_role_policy = data.aws_iam_policy_document.assume_self.json
  tags               = local.tags
}

resource "aws_iam_role" "evidence_auditor" {
  name               = "${var.name_prefix}-evidence-auditor"
  assume_role_policy = data.aws_iam_policy_document.assume_self.json
  tags               = local.tags
}

resource "aws_iam_role_policy" "settlement_writer" {
  name = "settlements-write"
  role = aws_iam_role.settlement_writer.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ListBucketSettlements"
        Effect = "Allow"
        Action = ["s3:ListBucket", "s3:ListBucketVersions"]
        Resource = [
          "arn:${data.aws_partition.current.partition}:s3:::${local.primary_bucket_name}"
        ]
        Condition = {
          StringLike = {
            "s3:prefix" = ["settlements/*", "settlements"]
          }
        }
      },
      {
        Sid    = "WriteSettlements"
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:DeleteObject",
          "s3:DeleteObjectVersion"
        ]
        Resource = [
          "arn:${data.aws_partition.current.partition}:s3:::${local.primary_bucket_name}/settlements/*"
        ]
      },
      {
        Sid      = "UseLabKms"
        Effect   = "Allow"
        Action   = ["kms:Encrypt", "kms:Decrypt", "kms:GenerateDataKey*", "kms:DescribeKey"]
        Resource = [aws_kms_key.lab.arn]
      }
    ]
  })
}

resource "aws_iam_role_policy" "settlement_reader" {
  name = "settlements-read"
  role = aws_iam_role.settlement_reader.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "ListBucketSettlements"
        Effect   = "Allow"
        Action   = ["s3:ListBucket", "s3:ListBucketVersions"]
        Resource = ["arn:${data.aws_partition.current.partition}:s3:::${local.primary_bucket_name}"]
        Condition = {
          StringLike = {
            "s3:prefix" = ["settlements/*", "settlements"]
          }
        }
      },
      {
        Sid      = "ReadSettlements"
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:GetObjectVersion"]
        Resource = ["arn:${data.aws_partition.current.partition}:s3:::${local.primary_bucket_name}/settlements/*"]
      },
      {
        Sid      = "DecryptLabKms"
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:DescribeKey"]
        Resource = [aws_kms_key.lab.arn]
      }
    ]
  })
}

resource "aws_iam_role_policy" "evidence_auditor" {
  name = "evidence-read"
  role = aws_iam_role.evidence_auditor.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "ListEvidencePrefix"
        Effect   = "Allow"
        Action   = ["s3:ListBucket"]
        Resource = ["arn:${data.aws_partition.current.partition}:s3:::${local.primary_bucket_name}"]
        Condition = {
          StringLike = {
            "s3:prefix" = ["evidence/*", "evidence"]
          }
        }
      },
      {
        Sid      = "ReadEvidenceObjects"
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:GetObjectVersion"]
        Resource = ["arn:${data.aws_partition.current.partition}:s3:::${local.primary_bucket_name}/evidence/*"]
      },
      {
        Sid      = "ReadEvidenceTable"
        Effect   = "Allow"
        Action   = ["dynamodb:GetItem", "dynamodb:Query", "dynamodb:Scan"]
        Resource = [aws_dynamodb_table.evidence.arn]
      },
      {
        Sid      = "DecryptLabKms"
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:DescribeKey"]
        Resource = [aws_kms_key.lab.arn]
      }
    ]
  })
}

# -----------------------------------------------------------------------------
# S3 primary
# -----------------------------------------------------------------------------

resource "aws_s3_bucket" "primary" {
  bucket = local.primary_bucket_name
  tags   = local.tags
}

resource "aws_s3_bucket_versioning" "primary" {
  bucket = aws_s3_bucket.primary.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "primary" {
  bucket = aws_s3_bucket.primary.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.lab.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "primary" {
  bucket                  = aws_s3_bucket.primary.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "primary" {
  bucket = aws_s3_bucket.primary.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "DenyInsecureTransport"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.primary.arn,
          "${aws_s3_bucket.primary.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      },
      {
        Sid       = "DenyUnencryptedObjectUploads"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:PutObject"
        Resource  = "${aws_s3_bucket.primary.arn}/*"
        Condition = {
          StringNotEquals = {
            "s3:x-amz-server-side-encryption" = "aws:kms"
          }
        }
      }
    ]
  })
}

# -----------------------------------------------------------------------------
# Optional CRR
# -----------------------------------------------------------------------------

resource "aws_s3_bucket" "replica" {
  count    = var.enable_replication ? 1 : 0
  provider = aws.replica
  bucket   = local.replica_bucket_name
  tags     = local.tags
}

resource "aws_s3_bucket_versioning" "replica" {
  count    = var.enable_replication ? 1 : 0
  provider = aws.replica
  bucket   = aws_s3_bucket.replica[0].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "replica" {
  count    = var.enable_replication ? 1 : 0
  provider = aws.replica
  bucket   = aws_s3_bucket.replica[0].id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "replica" {
  count                   = var.enable_replication ? 1 : 0
  provider                = aws.replica
  bucket                  = aws_s3_bucket.replica[0].id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_iam_role" "replication" {
  count = var.enable_replication ? 1 : 0
  name  = "${var.name_prefix}-s3-replication"
  tags  = local.tags

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "s3.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "replication" {
  count = var.enable_replication ? 1 : 0
  name  = "replication"
  role  = aws_iam_role.replication[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetReplicationConfiguration",
          "s3:ListBucket"
        ]
        Resource = [aws_s3_bucket.primary.arn]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObjectVersionForReplication",
          "s3:GetObjectVersionAcl",
          "s3:GetObjectVersionTagging"
        ]
        Resource = ["${aws_s3_bucket.primary.arn}/*"]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ReplicateObject",
          "s3:ReplicateDelete",
          "s3:ReplicateTags"
        ]
        Resource = ["${aws_s3_bucket.replica[0].arn}/*"]
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:Encrypt",
          "kms:GenerateDataKey*",
          "kms:DescribeKey"
        ]
        Resource = [aws_kms_key.lab.arn]
      }
    ]
  })
}

resource "aws_s3_bucket_replication_configuration" "primary" {
  count  = var.enable_replication ? 1 : 0
  bucket = aws_s3_bucket.primary.id
  role   = aws_iam_role.replication[0].arn

  depends_on = [aws_s3_bucket_versioning.primary, aws_s3_bucket_versioning.replica]

  rule {
    id     = "settlements-crr"
    status = "Enabled"

    filter {
      prefix = "settlements/"
    }

    destination {
      bucket        = aws_s3_bucket.replica[0].arn
      storage_class = "STANDARD"
    }

    delete_marker_replication {
      status = "Disabled"
    }
  }
}

# -----------------------------------------------------------------------------
# DynamoDB evidence registry
# -----------------------------------------------------------------------------

resource "aws_dynamodb_table" "evidence" {
  name         = "${var.name_prefix}-control-evidence"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "control_id"

  attribute {
    name = "control_id"
    type = "S"
  }

  tags = local.tags
}

# -----------------------------------------------------------------------------
# SNS + CloudWatch
# -----------------------------------------------------------------------------

resource "aws_sns_topic" "alarms" {
  name = "${var.name_prefix}-alarms"
  tags = local.tags
}

resource "aws_sns_topic_subscription" "email" {
  count     = var.alert_email != "" ? 1 : 0
  topic_arn = aws_sns_topic.alarms.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

resource "aws_s3_bucket_metric" "primary_entire" {
  bucket = aws_s3_bucket.primary.id
  name   = "EntireBucket"
}

resource "aws_cloudwatch_metric_alarm" "bucket_4xx" {
  alarm_name          = "${var.name_prefix}-s3-4xx-errors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "4xxErrors"
  namespace           = "AWS/S3"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  treat_missing_data  = "notBreaching"
  alarm_description   = "Elevated S3 4xx errors on lab primary bucket"
  alarm_actions       = [aws_sns_topic.alarms.arn]
  ok_actions          = [aws_sns_topic.alarms.arn]
  tags                = local.tags

  dimensions = {
    BucketName = aws_s3_bucket.primary.bucket
    FilterId   = aws_s3_bucket_metric.primary_entire.name
  }
}

resource "aws_cloudwatch_metric_alarm" "drill_signal" {
  alarm_name          = "${var.name_prefix}-drill-custom"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "RecoveryDrillEvents"
  namespace           = "BayLearn/Lab07"
  period              = 60
  statistic           = "Sum"
  threshold           = 1
  treat_missing_data  = "notBreaching"
  alarm_description   = "Fires when lab recovery drill Lambda emits a custom metric"
  alarm_actions       = [aws_sns_topic.alarms.arn]
  tags                = local.tags
}

# -----------------------------------------------------------------------------
# Optional lightweight Lambda for drill metric emission
# -----------------------------------------------------------------------------

data "archive_file" "drill" {
  type        = "zip"
  output_path = "${path.module}/lambda/drill.zip"

  source {
    content  = file("${path.module}/lambda/drill.py")
    filename = "drill.py"
  }
}

resource "aws_iam_role" "drill_lambda" {
  name = "${var.name_prefix}-drill-lambda"
  tags = local.tags

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "drill_lambda" {
  name = "drill-metrics-and-logs"
  role = aws_iam_role.drill_lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:${data.aws_partition.current.partition}:logs:*:${data.aws_caller_identity.current.account_id}:*"
      },
      {
        Effect   = "Allow"
        Action   = ["cloudwatch:PutMetricData"]
        Resource = "*"
        Condition = {
          StringEquals = {
            "cloudwatch:namespace" = "BayLearn/Lab07"
          }
        }
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ]
        Resource = [aws_dynamodb_table.evidence.arn]
      }
    ]
  })
}

resource "aws_lambda_function" "drill" {
  function_name    = "${var.name_prefix}-recovery-drill"
  role             = aws_iam_role.drill_lambda.arn
  handler          = "drill.handler"
  runtime          = "python3.12"
  filename         = data.archive_file.drill.output_path
  source_code_hash = data.archive_file.drill.output_base64sha256
  timeout          = 30
  tags             = local.tags

  environment {
    variables = {
      EVIDENCE_TABLE   = aws_dynamodb_table.evidence.name
      METRIC_NAMESPACE = "BayLearn/Lab07"
    }
  }
}
