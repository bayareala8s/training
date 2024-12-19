{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:role/sftp-access-role"
      },
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::my-sftp-bucket",
      "Condition": {
        "StringLike": {
          "s3:prefix": [
            "user1/*",
            "user1/folder1/*",
            "user1/folder2/*"
          ]
        }
      }
    },
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:role/sftp-access-role"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::my-sftp-bucket/user1/*",
        "arn:aws:s3:::my-sftp-bucket/user1/folder1/*",
        "arn:aws:s3:::my-sftp-bucket/user1/folder2/*"
      ]
    }
  ]
}
