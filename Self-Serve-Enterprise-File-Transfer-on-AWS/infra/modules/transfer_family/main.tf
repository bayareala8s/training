terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.50"
    }
    tls = {
      source  = "hashicorp/tls"
      version = ">= 4.0"
    }
    external = {
      source  = "hashicorp/external"
      version = ">= 2.3"
    }
    time = {
      source  = "hashicorp/time"
      version = ">= 0.9"
    }
  }
}

resource "time_sleep" "wait_for_sftp_ready" {
  count = var.enable_server && var.enable_connector && length(var.connector_trusted_host_keys) == 0 ? 1 : 0

  create_duration = "45s"
  depends_on      = [aws_transfer_server.this]
}

data "external" "connector_trusted_host_key" {
  count = var.enable_server && var.enable_connector && length(var.connector_trusted_host_keys) == 0 ? 1 : 0

  program = ["bash", "${path.module}/fetch_sftp_trusted_host_key.sh"]

  query = {
    endpoint = aws_transfer_server.this[0].endpoint
    port     = "22"
  }

  depends_on = [time_sleep.wait_for_sftp_ready]
}

locals {
  connector_trusted_host_key_from_scan = (
    var.enable_server && var.enable_connector && length(var.connector_trusted_host_keys) == 0
    ? data.external.connector_trusted_host_key[0].result.key
    : null
  )
  connector_trusted_host_keys_resolved = (
    length(var.connector_trusted_host_keys) > 0 ? var.connector_trusted_host_keys : (
      local.connector_trusted_host_key_from_scan != null ? [local.connector_trusted_host_key_from_scan] : []
    )
  )
}

resource "tls_private_key" "inbound" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_secretsmanager_secret" "inbound_private_key" {
  name                    = "${var.name_prefix}-sftp-inbound-private-key"
  recovery_window_in_days = var.secret_recovery_days
  tags                    = var.tags
}

resource "aws_secretsmanager_secret_version" "inbound_private_key" {
  secret_id     = aws_secretsmanager_secret.inbound_private_key.id
  secret_string = tls_private_key.inbound.private_key_pem
}

resource "aws_iam_role" "transfer_inbound" {
  name = "${var.name_prefix}-transfer-inbound"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "transfer.amazonaws.com" }
      Action    = "sts:AssumeRole"
      Condition = {
        StringEquals = { "aws:SourceAccount" = var.account_id }
      }
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy" "transfer_inbound_s3" {
  name = "${var.name_prefix}-transfer-inbound-s3"
  role = aws_iam_role.transfer_inbound.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:ListBucket", "s3:GetBucketLocation"]
        Resource = var.bucket_arn
        Condition = {
          StringLike = { "s3:prefix" = ["${var.inbound_prefix}*", trimsuffix(var.inbound_prefix, "/")] }
        }
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject", "s3:GetObjectVersion", "s3:PutObject", "s3:DeleteObject",
          "s3:GetObjectACL", "s3:PutObjectACL"
        ]
        Resource = "${var.bucket_arn}/${var.inbound_prefix}*"
      },
      {
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:Encrypt", "kms:GenerateDataKey", "kms:DescribeKey"]
        Resource = var.kms_key_arn
      }
    ]
  })
}

resource "aws_transfer_server" "this" {
  count                  = var.enable_server ? 1 : 0
  protocols              = ["SFTP"]
  identity_provider_type = "SERVICE_MANAGED"
  endpoint_type          = "PUBLIC"
  domain                 = "S3"
  tags                   = merge(var.tags, { Name = "${var.name_prefix}-sftp" })
}

resource "aws_transfer_user" "inbound" {
  count               = var.enable_server ? 1 : 0
  server_id           = aws_transfer_server.this[0].id
  user_name           = var.inbound_username
  role                = aws_iam_role.transfer_inbound.arn
  home_directory_type = "LOGICAL"

  home_directory_mappings {
    entry  = "/"
    target = "/${var.bucket_id}/${trimsuffix(var.inbound_prefix, "/")}"
  }

  tags = var.tags
}

resource "aws_transfer_ssh_key" "inbound" {
  count     = var.enable_server ? 1 : 0
  server_id = aws_transfer_server.this[0].id
  user_name = aws_transfer_user.inbound[0].user_name
  body      = tls_private_key.inbound.public_key_openssh
}

resource "tls_private_key" "connector" {
  count     = var.enable_connector && var.enable_server ? 1 : 0
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_secretsmanager_secret" "connector_creds" {
  count                   = var.enable_connector && var.enable_server ? 1 : 0
  name                    = "${var.name_prefix}-sftp-connector-secret"
  recovery_window_in_days = var.secret_recovery_days
  tags                    = var.tags
}

resource "aws_secretsmanager_secret_version" "connector_creds" {
  count     = var.enable_connector && var.enable_server ? 1 : 0
  secret_id = aws_secretsmanager_secret.connector_creds[0].id
  secret_string = jsonencode({
    Username   = var.connector_username
    PrivateKey = tls_private_key.connector[0].private_key_openssh
  })
}

resource "aws_iam_role" "transfer_connector_user" {
  count = var.enable_connector && var.enable_server ? 1 : 0
  name  = "${var.name_prefix}-transfer-connector-user"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "transfer.amazonaws.com" }
      Action    = "sts:AssumeRole"
      Condition = { StringEquals = { "aws:SourceAccount" = var.account_id } }
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy" "transfer_connector_user_s3" {
  count = var.enable_connector && var.enable_server ? 1 : 0
  name  = "${var.name_prefix}-transfer-connector-user-s3"
  role  = aws_iam_role.transfer_connector_user[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:ListBucket", "s3:GetBucketLocation"]
        Resource = var.bucket_arn
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject", "s3:GetObjectVersion", "s3:PutObject", "s3:DeleteObject",
          "s3:GetObjectACL", "s3:PutObjectACL"
        ]
        Resource = [
          "${var.bucket_arn}/${var.connector_prefix}*",
          "${var.bucket_arn}/${var.staging_prefix}*",
          "${var.bucket_arn}/${var.inbound_prefix}*",
          "${var.bucket_arn}/partners/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:Encrypt", "kms:GenerateDataKey", "kms:DescribeKey"]
        Resource = var.kms_key_arn
      }
    ]
  })
}

resource "aws_transfer_user" "connector" {
  count               = var.enable_connector && var.enable_server ? 1 : 0
  server_id           = aws_transfer_server.this[0].id
  user_name           = var.connector_username
  role                = aws_iam_role.transfer_connector_user[0].arn
  home_directory_type = "LOGICAL"

  home_directory_mappings {
    entry  = "/"
    target = "/${var.bucket_id}/${trimsuffix(var.connector_prefix, "/")}"
  }

  tags = var.tags
}

resource "aws_transfer_ssh_key" "connector" {
  count     = var.enable_connector && var.enable_server ? 1 : 0
  server_id = aws_transfer_server.this[0].id
  user_name = aws_transfer_user.connector[0].user_name
  body      = tls_private_key.connector[0].public_key_openssh
}

resource "aws_iam_role" "connector_access" {
  count = var.enable_connector && var.enable_server ? 1 : 0
  name  = "${var.name_prefix}-transfer-connector-access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "transfer.amazonaws.com" }
      Action    = "sts:AssumeRole"
      Condition = { StringEquals = { "aws:SourceAccount" = var.account_id } }
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy" "connector_access_s3" {
  count = var.enable_connector && var.enable_server ? 1 : 0
  name  = "${var.name_prefix}-connector-access-s3"
  role  = aws_iam_role.connector_access[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:ListBucket", "s3:GetBucketLocation"]
        Resource = var.bucket_arn
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject", "s3:GetObjectVersion", "s3:PutObject", "s3:DeleteObject",
          "s3:GetObjectACL", "s3:PutObjectACL"
        ]
        Resource = "${var.bucket_arn}/*"
      },
      {
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:Encrypt", "kms:GenerateDataKey", "kms:DescribeKey"]
        Resource = var.kms_key_arn
      },
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = aws_secretsmanager_secret.connector_creds[0].arn
      }
    ]
  })
}

resource "aws_transfer_connector" "this" {
  count       = var.enable_connector && var.enable_server ? 1 : 0
  access_role = aws_iam_role.connector_access[0].arn
  url         = "sftp://${aws_transfer_server.this[0].endpoint}:22"

  sftp_config {
    user_secret_id    = aws_secretsmanager_secret.connector_creds[0].id
    trusted_host_keys = local.connector_trusted_host_keys_resolved
  }

  tags = merge(var.tags, { Name = "${var.name_prefix}-sftp-connector" })
}

data "aws_iam_policy_document" "transfer_bucket" {
  count = var.enable_server ? 1 : 0

  statement {
    sid    = "AllowTransferServer"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["transfer.amazonaws.com"]
    }
    actions = [
      "s3:AbortMultipartUpload", "s3:DeleteObject", "s3:DeleteObjectVersion",
      "s3:GetObject", "s3:GetObjectVersion", "s3:ListBucket", "s3:PutObject",
      "s3:GetObjectACL", "s3:PutObjectACL", "s3:GetBucketLocation",
    ]
    resources = [var.bucket_arn, "${var.bucket_arn}/*"]
    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [var.account_id]
    }
    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values   = [aws_transfer_server.this[0].arn]
    }
  }
}

resource "aws_s3_bucket_policy" "transfer" {
  count  = var.enable_server ? 1 : 0
  bucket = var.bucket_id
  policy = data.aws_iam_policy_document.transfer_bucket[0].json
}

variable "name_prefix" { type = string }
variable "account_id" { type = string }
variable "region" { type = string }
variable "bucket_id" { type = string }
variable "bucket_arn" { type = string }
variable "kms_key_arn" { type = string }
variable "enable_server" {
  type    = bool
  default = true
}
variable "inbound_username" {
  type    = string
  default = "partner-demo"
}
variable "connector_username" {
  type    = string
  default = "connector-demo"
}
variable "inbound_prefix" {
  type    = string
  default = "partners/demo/inbound/"
}
variable "connector_prefix" {
  type    = string
  default = "partners/demo/connector/"
}
variable "staging_prefix" {
  type    = string
  default = "partners/demo/outbound/"
}
variable "enable_connector" {
  type    = bool
  default = true
}
variable "connector_trusted_host_keys" {
  type    = list(string)
  default = []
}
variable "secret_recovery_days" {
  type    = number
  default = 0
}
variable "tags" {
  type    = map(string)
  default = {}
}

output "server_id" {
  value = var.enable_server ? aws_transfer_server.this[0].id : null
}
output "server_endpoint" {
  value = var.enable_server ? aws_transfer_server.this[0].endpoint : null
}
output "inbound_username" {
  value = var.inbound_username
}
output "inbound_private_key_secret_arn" {
  value     = aws_secretsmanager_secret.inbound_private_key.arn
  sensitive = true
}
output "connector_id" {
  value = var.enable_connector && var.enable_server ? aws_transfer_connector.this[0].id : null
}
output "inbound_s3_prefix" {
  value = var.inbound_prefix
}
output "staging_s3_prefix" {
  value = var.staging_prefix
}
