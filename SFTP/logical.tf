# Define the AWS provider
provider "aws" {
  region = "us-west-2"
}

# Define variables for bucket name and user information
variable "bucket_name" {
  default = "my-sftp-bucket"
}

variable "username" {
  default = "user1"
}

# Create an S3 bucket
resource "aws_s3_bucket" "sftp_bucket" {
  bucket = var.bucket_name
  acl    = "private"

  tags = {
    Name        = "SFTP Bucket"
    Environment = "Production"
  }
}

# Create sub-folders in the S3 bucket
resource "aws_s3_bucket_object" "sftp_folders" {
  for_each = toset(["user1/folder1/", "user1/folder2/"])
  bucket   = aws_s3_bucket.sftp_bucket.id
  key      = each.value
}

# Create an IAM role for AWS Transfer Family
resource "aws_iam_role" "sftp_role" {
  name = "sftp-access-role"

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

# Attach policies to the IAM role to restrict access to sub-folders
resource "aws_iam_policy" "sftp_policy" {
  name        = "sftp-access-policy"
  description = "Policy to restrict user access to specific folders"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = "s3:ListBucket",
        Resource = "arn:aws:s3:::${var.bucket_name}",
        Condition = {
          StringLike = {
            "s3:prefix": [
              "user1/folder1/*",
              "user1/folder2/*"
            ]
          }
        }
      },
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ],
        Resource = [
          "arn:aws:s3:::${var.bucket_name}/user1/folder1/*",
          "arn:aws:s3:::${var.bucket_name}/user1/folder2/*"
        ]
      }
    ]
  })
}

# Attach the policy to the IAM role
resource "aws_iam_role_policy_attachment" "sftp_role_attach" {
  role       = aws_iam_role.sftp_role.name
  policy_arn = aws_iam_policy.sftp_policy.arn
}

# Create the AWS Transfer Family server
resource "aws_transfer_server" "sftp_server" {
  identity_provider_type = "SERVICE_MANAGED"
  endpoint_type          = "PUBLIC"
  logging_role           = aws_iam_role.sftp_role.arn

  tags = {
    Name        = "SFTP Server"
    Environment = "Production"
  }
}

# Create the SFTP user
resource "aws_transfer_user" "sftp_user" {
  server_id    = aws_transfer_server.sftp_server.id
  user_name    = var.username
  role         = aws_iam_role.sftp_role.arn
  home_directory = "/user1"
}


ssh-keygen -t rsa -b 2048 -f user1-sftp-key
