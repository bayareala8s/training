provider "aws" {
  region = "us-west-2"
}

resource "aws_iam_role" "sftp_role" {
  name = "SFTPTransferRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "transfer.amazonaws.com"
          },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "sftp_policy" {
  name   = "SFTPS3AccessPolicy"
  role   = aws_iam_role.sftp_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject"
        ],
        Resource = [
          "arn:aws:s3:::bayareala8s-sftp-bucket",
          "arn:aws:s3:::bayareala8s-sftp-bucket/*"
        ]
      }
    ]
  })
}

resource "aws_s3_bucket" "sftp_bucket" {
  bucket = "bayareala8s-sftp-bucket"
}

resource "aws_transfer_server" "sftp_server" {
  endpoint_type = "PUBLIC"
  identity_provider_type = "SERVICE_MANAGED"
  tags = {
    Name = "MySFTPServer"
  }
}

resource "aws_transfer_user" "sftp_user" {
  user_name          = "sftp_user"
  server_id          = aws_transfer_server.sftp_server.id
  role               = aws_iam_role.sftp_role.arn
  home_directory_type = "LOGICAL"

  home_directory_mappings {
    entry  = "/"
    target = "/bayareala8s-sftp-bucket"
  }

  tags = {
    Name = "SFTPUser"
  }
}