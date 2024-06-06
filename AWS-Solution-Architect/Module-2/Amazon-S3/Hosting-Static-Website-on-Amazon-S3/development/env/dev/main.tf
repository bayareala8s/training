resource "aws_s3_bucket" "static_website" {
  bucket = var.bucket_name

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "log"
    enabled = true

    prefix = "log/"
    transition {
      days          = 30
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }

  lifecycle_rule {
    id      = "temp"
    enabled = true

    prefix = "temp/"
    expiration {
      days = 7
    }
  }
}

resource "aws_s3_bucket_policy" "static_website_policy" {
  bucket = aws_s3_bucket.static_website.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = "*",
        Action    = ["s3:GetObject", "s3:PutObject"],
        Resource  = "${aws_s3_bucket.static_website.arn}/*"
      },
      {
        Effect    = "Allow",
        Principal = "*",
        Action    = ["s3:ListBucket","s3:GetBucketPolicy","s3:PutBucketPolicy"],
        Resource  = aws_s3_bucket.static_website.arn
      }
    ]
  })
}

resource "aws_s3_bucket_object" "website_files" {
  for_each = fileset("${path.module}/website", "*")

  bucket = aws_s3_bucket.static_website.bucket
  key    = each.value
  source = "${path.module}/website/${each.value}"

  
}

resource "aws_s3_bucket_object" "index_html" {
  bucket = aws_s3_bucket.static_website.bucket
  key    = "index.html"
  source = "${path.module}/website/index.html"
  content_type = "text/html"
}

resource "aws_s3_bucket_object" "error_html" {
  bucket = aws_s3_bucket.static_website.bucket
  key    = "error.html"
  source = "${path.module}/website/error.html"
  content_type = "text/html"
}


