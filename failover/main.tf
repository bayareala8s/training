# Provider for the primary region (us-west-1)
provider "aws" {
  region = "us-west-1"
}

# Provider for the replica region (us-east-1)
provider "aws" {
  alias  = "replica"
  region = "us-east-1"
}

# Create Primary S3 Bucket in us-west-1
resource "aws_s3_bucket" "primary_bucket" {
  bucket = var.primary_bucket_name
  versioning {
    enabled = true
  }

  replication_configuration {
    role = aws_iam_role.s3_replication_role.arn

    rules {
      id     = "PrimaryToReplica"
      status = "Enabled"

      destination {
        bucket        = aws_s3_bucket.replica_bucket.arn
        storage_class = "STANDARD"
      }

      filter {
        prefix = ""
      }
    }
  }

  tags = {
    Environment = "Primary"
  }
}

# Create Replica S3 Bucket in us-east-1
resource "aws_s3_bucket" "replica_bucket" {
  provider = aws.replica

  bucket = var.replica_bucket_name
  versioning {
    enabled = true
  }

  tags = {
    Environment = "Replica"
  }
}

# Create IAM Role for S3 Replication
resource "aws_iam_role" "s3_replication_role" {
  name = "s3-replication-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = { Service = "s3.amazonaws.com" }
      }
    ]
  })
}

# IAM Policy for S3 Replication
resource "aws_iam_role_policy" "s3_replication_policy" {
  name   = "s3-replication-policy"
  role   = aws_iam_role.s3_replication_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetReplicationConfiguration",
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.primary_bucket.arn
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObjectVersion",
          "s3:GetObjectVersionAcl",
          "s3:ReplicateObject",
          "s3:ReplicateDelete"
        ]
        Resource = "${aws_s3_bucket.primary_bucket.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ReplicateObject"
        ]
        Resource = "${aws_s3_bucket.replica_bucket.arn}/*"
      }
    ]
  })
}

# Create IAM Role for Lambda Functions
resource "aws_iam_role" "lambda_role" {
  name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = { Service = "lambda.amazonaws.com" }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda-policy"
  role = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.primary_bucket.arn,
          "${aws_s3_bucket.primary_bucket.arn}/*",
          aws_s3_bucket.replica_bucket.arn,
          "${aws_s3_bucket.replica_bucket.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

# Primary Lambda Function
resource "aws_lambda_function" "primary_lambda" {
  function_name = "primary_lambda"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  handler       = "primary_lambda.lambda_handler"

  filename = "${path.module}/lambda/primary_lambda.py.zip"

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.primary_bucket.id
    }
  }
}

# Backup Lambda Function
resource "aws_lambda_function" "backup_lambda" {
  function_name = "backup_lambda"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  handler       = "backup_lambda.lambda_handler"

  filename = "${path.module}/lambda/backup_lambda.py.zip"

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.replica_bucket.id
    }
  }
}

# S3 Event Notification for Primary Lambda
resource "aws_s3_bucket_notification" "primary_bucket_notification" {
  bucket = aws_s3_bucket.primary_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.primary_lambda.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

# S3 Event Notification for Backup Lambda
resource "aws_s3_bucket_notification" "replica_bucket_notification" {
  provider = aws.replica
  bucket   = aws_s3_bucket.replica_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.backup_lambda.arn
    events              = ["s3:ObjectCreated:*"]
  }
}
