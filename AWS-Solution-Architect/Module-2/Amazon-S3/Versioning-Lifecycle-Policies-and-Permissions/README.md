### Detailed Guidance on S3 Versioning, Lifecycle Policies, and Permissions

#### 1. Versioning

**What is Versioning?**

S3 versioning allows you to keep multiple versions of an object in the same bucket, enabling you to retrieve, preserve, and restore every version of every object stored in your S3 bucket. This can help protect against accidental or malicious deletions and overwrites.

**Enabling Versioning**

To enable versioning on an S3 bucket:

```hcl
resource "aws_s3_bucket" "example_bucket" {
  bucket = "example-bucket"

  versioning {
    enabled = true
  }
}
```

**Managing Versions**

When versioning is enabled:
- Each object is assigned a unique version ID.
- Objects can be retrieved, overwritten, or deleted by specifying their version ID.

To access a specific version of an object, use its version ID in your S3 operations.

**Example Commands:**

- **Upload a new version:**

  ```sh
  aws s3 cp myfile.txt s3://example-bucket/
  ```

- **Retrieve a specific version:**

  ```sh
  aws s3api get-object --bucket example-bucket --key myfile.txt --version-id VERSION_ID myfile.txt
  ```

- **Delete a specific version:**

  ```sh
  aws s3api delete-object --bucket example-bucket --key myfile.txt --version-id VERSION_ID
  ```

#### 2. Lifecycle Policies

**What are Lifecycle Policies?**

Lifecycle policies allow you to define actions to manage your objects during their lifetime. You can set up rules to transition objects to different storage classes or delete them after a specified period.

**Defining Lifecycle Policies**

To define lifecycle policies, you can add lifecycle rules to your S3 bucket configuration.

**Example Lifecycle Policies:**

- **Transitioning Objects:**
  Move objects to the Glacier storage class after 30 days.

  ```hcl
  resource "aws_s3_bucket" "example_bucket" {
    bucket = "example-bucket"

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
  }
  ```

- **Expiring Objects:**
  Delete objects with the "temp/" prefix after 7 days.

  ```hcl
  resource "aws_s3_bucket" "example_bucket" {
    bucket = "example-bucket"

    lifecycle_rule {
      id      = "temp"
      enabled = true

      prefix = "temp/"
      expiration {
        days = 7
      }
    }
  }
  ```

**Example Commands:**

- **Create a lifecycle rule via AWS CLI:**

  ```sh
  aws s3api put-bucket-lifecycle-configuration --bucket example-bucket --lifecycle-configuration file://lifecycle.json
  ```

  ```json
  {
    "Rules": [
      {
        "ID": "Move to Glacier after 30 days",
        "Prefix": "log/",
        "Status": "Enabled",
        "Transitions": [
          {
            "Days": 30,
            "StorageClass": "GLACIER"
          }
        ],
        "Expiration": {
          "Days": 365
        }
      },
      {
        "ID": "Delete temp files after 7 days",
        "Prefix": "temp/",
        "Status": "Enabled",
        "Expiration": {
          "Days": 7
        }
      }
    ]
  }
  ```

#### 3. Permissions

**What are S3 Permissions?**

S3 permissions determine who can access your S3 bucket and what actions they can perform. Permissions can be set at the bucket level, the object level, and using IAM policies.

**Types of Permissions:**

- **Bucket Policies:**
  Apply permissions to all objects within a bucket.

  ```hcl
  resource "aws_s3_bucket_policy" "example_bucket_policy" {
    bucket = aws_s3_bucket.example_bucket.id

    policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Effect    = "Allow",
          Principal = "*",
          Action    = "s3:GetObject",
          Resource  = "${aws_s3_bucket.example_bucket.arn}/*"
        }
      ]
    })
  }
  ```

- **Access Control Lists (ACLs):**
  Set permissions on individual objects.

  ```hcl
  resource "aws_s3_bucket_object" "example_object" {
    bucket = aws_s3_bucket.example_bucket.bucket
    key    = "example-object"
    source = "path/to/example-object"
    acl    = "public-read"
  }
  ```

- **IAM Policies:**
  Attach policies to IAM users, groups, or roles to grant access to S3 resources.

  ```hcl
  resource "aws_iam_role" "s3_access_role" {
    name = "s3_access_role"

    assume_role_policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Effect = "Allow",
          Principal = {
            Service = "ec2.amazonaws.com"
          },
          Action = "sts:AssumeRole"
        }
      ]
    })
  }

  resource "aws_iam_policy" "s3_access_policy" {
    name        = "s3_access_policy"
    description = "Policy to allow access to S3 bucket"
    policy      = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Effect = "Allow",
          Action = [
            "s3:ListBucket",
            "s3:GetObject"
          ],
          Resource = [
            aws_s3_bucket.example_bucket.arn,
            "${aws_s3_bucket.example_bucket.arn}/*"
          ]
        }
      ]
    })
  }

  resource "aws_iam_role_policy_attachment" "attach_s3_access_policy" {
    role       = aws_iam_role.s3_access_role.name
    policy_arn = aws_iam_policy.s3_access_policy.arn
  }
  ```

**Example Commands:**

- **Attach an IAM policy to a role via AWS CLI:**

  ```sh
  aws iam attach-role-policy --role-name s3_access_role --policy-arn arn:aws:iam::aws:policy/s3_access_policy
  ```

### Putting It All Together

Here is a comprehensive Terraform script that includes S3 bucket creation with versioning, lifecycle policies, and permissions:

```hcl
# variables.tf
variable "region" {
  description = "The AWS region to create resources in."
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "The name of the S3 bucket."
  default     = "my-static-website-bucket"
}

# provider.tf
provider "aws" {
  region = var.region
}

# main.tf
resource "aws_s3_bucket" "example_bucket" {
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

resource "aws_s3_bucket_policy" "example_bucket_policy" {
  bucket = aws_s3_bucket.example_bucket.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = "*",
        Action    = "s3:GetObject",
        Resource  = "${aws_s3_bucket.example_bucket.arn}/*"
      }
    ]
  })
}

resource "aws_s3_bucket_object" "website_files" {
  for_each = fileset("${path.module}/website", "*")

  bucket = aws_s3_bucket.example_bucket.bucket
  key    = each.value
  source = "${path.module}/website/${each.value}"
  acl    = "public-read"
}

# iam.tf
resource "aws_iam_role" "s3_access_role" {
  name = "s3_access_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "s3_access_policy" {
  name        = "s3_access_policy"
  description = "Policy to allow access to S3 bucket"
  policy      = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
          "s3:GetObject"
        ],
        Resource = [
          aws_s3_bucket.example_bucket.arn,
          "${aws_s3_bucket.example_bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_s3_access_policy" {
  role       = aws_iam_role.s3_access_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn


}
```

Ensure your directory structure looks like this:

```
.
├── main.tf
├── provider.tf
├── variables.tf
├── iam.tf
└── website
    ├── index.html
    └── error.html
```

### Conclusion

By implementing versioning, lifecycle policies, and fine-grained permissions, you can enhance the security, manageability, and cost-efficiency of your S3 buckets. This detailed guidance and comprehensive Terraform script should help you set up a robust and scalable static website hosting solution on Amazon S3.
