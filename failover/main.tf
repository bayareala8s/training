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

  # Cross-region replication configuration
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

# IAM Role for S3 Replication
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
