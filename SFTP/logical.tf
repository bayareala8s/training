resource "aws_iam_policy" "sftp_policy" {
  name        = "sftp-access-policy"
  description = "Policy to restrict user access to specific folders and prevent folder creation"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = "s3:ListBucket",
        Resource = "arn:aws:s3:::${var.bucket_name}",
        Condition = {
          StringLike: {
            "s3:prefix": [
              "user1/",
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
          "s3:PutObject"
        ],
        Resource = [
          "arn:aws:s3:::${var.bucket_name}/user1/folder1/*",
          "arn:aws:s3:::${var.bucket_name}/user1/folder2/*"
        ]
      },
      {
        Effect: "Deny",
        Action: "s3:PutObject",
        Resource: [
          "arn:aws:s3:::${var.bucket_name}/user1/",
          "arn:aws:s3:::${var.bucket_name}/user1/folder1/",
          "arn:aws:s3:::${var.bucket_name}/user1/folder2/"
        ],
        Condition: {
          StringEquals: {
            "s3:x-amz-object-lock-mode": "COMPLIANCE"
          }
        }
      }
    ]
  })
}
