## Backup Strategies and Services on AWS

### Introduction
Backup strategies are essential to ensure data protection, business continuity, and disaster recovery. AWS provides a range of services and best practices to create effective backup solutions tailored to different use cases and requirements.

### Key Backup Strategies

1. **Full Backup**
   - **Description**: A complete copy of all data is made at regular intervals.
   - **Pros**: Simplifies data restoration.
   - **Cons**: Requires significant storage space and time.
   - **Use Case**: Ideal for small datasets or environments with sufficient storage.

2. **Incremental Backup**
   - **Description**: Only the data that has changed since the last backup is copied.
   - **Pros**: Reduces storage space and backup time.
   - **Cons**: Restoration can be slower and more complex.
   - **Use Case**: Suitable for environments with frequent data changes.

3. **Differential Backup**
   - **Description**: Backs up data changed since the last full backup.
   - **Pros**: Faster to restore than incremental backups.
   - **Cons**: Requires more storage than incremental backups.
   - **Use Case**: Balanced approach for medium-sized datasets.

4. **Synthetic Full Backup**
   - **Description**: Combines previous full and incremental backups to create a new full backup.
   - **Pros**: Reduces the impact on production systems.
   - **Cons**: More complex to manage.
   - **Use Case**: Environments where minimizing downtime is critical.

5. **Continuous Data Protection (CDP)**
   - **Description**: Continuously backs up data changes.
   - **Pros**: Provides the most recent backup and minimizes data loss.
   - **Cons**: Can be resource-intensive.
   - **Use Case**: Mission-critical applications requiring near-zero RPO.

### AWS Backup Services

1. **Amazon S3 and Amazon S3 Glacier**
   - **Use**: Store and archive backups.
   - **Features**: Versioning, lifecycle policies, cross-region replication, high durability, and availability.

2. **AWS Backup**
   - **Use**: Centralized backup management service.
   - **Features**: Policy-based management, automated backups, cross-region backups, compliance monitoring.

3. **Amazon RDS Automated Backups and Snapshots**
   - **Use**: Automated backups for relational databases.
   - **Features**: Automated backups, manual snapshots, point-in-time recovery.

4. **Amazon EBS Snapshots**
   - **Use**: Back up Amazon EC2 instance data.
   - **Features**: Incremental snapshots, cross-region snapshot copies.

5. **AWS Storage Gateway**
   - **Use**: Hybrid cloud storage.
   - **Features**: Backup on-premises data to AWS, supports S3, Glacier, and EBS.

6. **Amazon DynamoDB Backups**
   - **Use**: Backup NoSQL database tables.
   - **Features**: On-demand backups, point-in-time recovery.

7. **AWS Snowball**
   - **Use**: Physical device for transferring large amounts of data.
   - **Features**: Import/export data between on-premises and AWS.

### Best Practices for Backup on AWS

1. **Define Backup Policies**
   - Establish policies for backup frequency, retention periods, and data lifecycle management.

2. **Automate Backups**
   - Use AWS Backup or native service capabilities to automate backup processes and reduce human error.

3. **Cross-Region Backups**
   - Store backups in multiple regions to protect against regional failures.

4. **Data Encryption**
   - Encrypt backups at rest and in transit to ensure data security and compliance.

5. **Regular Testing**
   - Regularly test backup and restore processes to ensure data can be reliably recovered.

6. **Monitor and Audit**
   - Use AWS CloudTrail and Amazon CloudWatch to monitor backup activities and maintain an audit trail.

7. **Cost Management**
   - Implement lifecycle policies to transition data to cost-effective storage classes (e.g., Glacier) and delete outdated backups.

### Implementation Examples

#### Example 1: Automated Backups with AWS Backup

```hcl
# Provider configuration
provider "aws" {
  region = "us-east-1"
}

# Backup Vault
resource "aws_backup_vault" "example_vault" {
  name        = "example_backup_vault"
  kms_key_arn = aws_kms_key.example_key.arn
}

# KMS Key
resource "aws_kms_key" "example_key" {
  description             = "KMS key for backup encryption"
  deletion_window_in_days = 10
}

# Backup Plan
resource "aws_backup_plan" "example_plan" {
  name = "example_backup_plan"

  rule {
    rule_name         = "daily_backup"
    target_vault_name = aws_backup_vault.example_vault.name
    schedule          = "cron(0 3 * * ? *)"

    lifecycle {
      cold_storage_after = 30
      delete_after       = 365
    }
  }
}

# Backup Selection
resource "aws_backup_selection" "example_selection" {
  iam_role_arn   = aws_iam_role.backup_role.arn
  name           = "example_backup_selection"
  backup_plan_id = aws_backup_plan.example_plan.id

  resources = [
    aws_db_instance.example_db.arn
  ]
}

# RDS Instance
resource "aws_db_instance" "example_db" {
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t2.micro"
  name                 = "exampledb"
  username             = "admin"
  password             = "password"
  parameter_group_name = "default.mysql5.6"
  multi_az             = true
  storage_type         = "gp2"
}

# IAM Role for Backup
resource "aws_iam_role" "backup_role" {
  name = "backup_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "backup.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "backup_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
  role       = aws_iam_role.backup_role.name
}
```

#### Example 2: Cross-Region Replication with Amazon S3

```hcl
# Provider configuration
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "us-west-1"
  region = "us-west-1"
}

# S3 Buckets
resource "aws_s3_bucket" "source_bucket" {
  bucket = "source-bucket"
  region = "us-east-1"
  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket" "destination_bucket" {
  provider = aws.us-west-1
  bucket   = "destination-bucket"
  region   = "us-west-1"
  versioning {
    enabled = true
  }
}

# IAM Role and Policy for Replication
resource "aws_iam_role" "replication_role" {
  name = "replication-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "replication_policy" {
  name        = "replication-policy"
  description = "Policy for S3 bucket replication"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetReplicationConfiguration",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.source_bucket.bucket}"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObjectVersion",
        "s3:GetObjectVersionAcl"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.source_bucket.bucket}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ReplicateObject",
        "s3:ReplicateDelete"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.destination_bucket.bucket}/*"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "replication_policy_attachment" {
  role       = aws_iam_role.replication_role.name
  policy_arn = aws_iam_policy.replication_policy.arn
}

# S3 Bucket Replication Configuration
resource "aws_s3_bucket_replication_configuration" "replication" {
  bucket = aws_s3_bucket.source_bucket.bucket

  role = aws_iam_role.replication_role.arn

  rules {
    id     = "replication-rule"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.destination_bucket.arn
      storage_class = "STANDARD"
    }

    filter {
      prefix = ""
    }
  }
}
```

### Conclusion

Effective backup strategies are crucial for data protection and disaster recovery. AWS provides a comprehensive set of services to implement various backup strategies, from simple backups to complex cross-region replication. By leveraging these services and following best practices, organizations can ensure their data is secure, compliant, and available when needed.


 Sure, here's a detailed step-by-step guide with Terraform scripts and comments for each real-world example:

### Example 1: Financial Services Firm (Multi-Site Active-Active)

#### Step-by-Step Guide

1. **Setup Providers**: Configure AWS providers for both primary and secondary regions.
2. **Create S3 Buckets**: Set up S3 buckets in both regions for data replication.
3. **Enable Versioning**: Enable versioning on both S3 buckets to keep track of object versions.
4. **Configure Replication**: Set up replication rules for the primary bucket to replicate objects to the secondary bucket.
5. **Create IAM Role and Policy**: Define the IAM role and policy needed for S3 replication.
6. **Set Up CloudFront Distribution**: Configure CloudFront for global content delivery.
7. **Configure Route 53 DNS Failover**: Set up health checks and DNS failover using Route 53.

#### Terraform Script

```hcl
# Step 1: Setup Providers
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "eu-west-1"
  region = "eu-west-1"
}

# Step 2: Create S3 Buckets
resource "aws_s3_bucket" "primary_bucket" {
  bucket = "primary-financial-services-bucket"
  region = "us-east-1"
}

resource "aws_s3_bucket" "secondary_bucket" {
  provider = aws.eu-west-1
  bucket   = "secondary-financial-services-bucket"
  region   = "eu-west-1"
}

# Step 3: Enable Versioning
resource "aws_s3_bucket_versioning" "primary_versioning" {
  bucket = aws_s3_bucket.primary_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "secondary_versioning" {
  provider = aws.eu-west-1
  bucket   = aws_s3_bucket.secondary_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Step 4: Configure Replication
resource "aws_s3_bucket_replication_configuration" "replication" {
  provider = aws.eu-west-1
  bucket   = aws_s3_bucket.secondary_bucket.id

  role = aws_iam_role.replication_role.arn

  rules {
    id     = "replication-rule"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.secondary_bucket.arn
      storage_class = "STANDARD"
    }

    filter {
      prefix = ""
    }
  }
}

# Step 5: Create IAM Role and Policy
resource "aws_iam_role" "replication_role" {
  name = "replication-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "replication_policy" {
  name        = "replication-policy"
  description = "Policy for S3 bucket replication"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetReplicationConfiguration",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.primary_bucket.id}"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObjectVersion",
        "s3:GetObjectVersionAcl"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.primary_bucket.id}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ReplicateObject",
        "s3:ReplicateDelete"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.secondary_bucket.id}/*"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "replication_policy_attachment" {
  role       = aws_iam_role.replication_role.name
  policy_arn = aws_iam_policy.replication_policy.arn
}

# Step 6: Set Up CloudFront Distribution
resource "aws_cloudfront_distribution" "distribution" {
  origin {
    domain_name = aws_s3_bucket.primary_bucket.bucket_regional_domain_name
    origin_id   = "S3-primary"
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Financial Services CloudFront Distribution"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "S3-primary"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# Step 7: Configure Route 53 DNS Failover
resource "aws_route53_health_check" "primary_health_check" {
  fqdn             = "primary.example.com"
  type             = "HTTP"
  resource_path    = "/health"
  port             = 80
  failure_threshold = 3
}

resource "aws_route53_health_check" "secondary_health_check" {
  fqdn             = "secondary.example.com"
  type             = "HTTP"
  resource_path    = "/health"
  port             = 80
  failure_threshold = 3
}

resource "aws_route53_record" "primary_record" {
  zone_id = "Z3M3LMPEXAMPLE"
  name    = "example.com"
  type    = "A"
  ttl     = "60"

  set_identifier = "primary"
  weight         = 100
  records        = ["1.2.3.4"]  # Replace with the IP of your primary instance

  health_check_id = aws_route53_health_check.primary_health_check.id
}

resource "aws_route53_record" "secondary_record" {
  zone_id = "Z3M3LMPEXAMPLE"
  name    = "example.com"
  type    = "A"
  ttl     = "60"

  set_identifier = "secondary"
  weight         = 100
  records        = ["5.6.7.8"]  # Replace with the IP of your secondary instance

  health_check_id = aws_route53_health_check.secondary_health_check.id
}
```

### Example 2: Media Streaming Service (Warm Standby)

#### Step-by-Step Guide

1. **Setup Providers**: Configure AWS providers for both primary and secondary regions.
2. **Create RDS Instances**: Set up RDS instances in both regions with a read replica in the secondary region.
3. **Create S3 Buckets**: Set up S3 buckets in both regions for media content replication.
4. **Enable Versioning**: Enable versioning on both S3 buckets.
5. **Configure Replication**: Set up replication rules for the primary bucket to replicate objects to the secondary bucket.
6. **Create IAM Role and Policy**: Define the IAM role and policy needed for S3 replication.
7. **Configure Route 53 DNS Failover**: Set up health checks and DNS failover using Route 53.

#### Terraform Script

```hcl
# Step 1: Setup Providers
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "ap-southeast-1"
  region = "ap-southeast-1"
}

# Step 2: Create RDS Instances
resource "aws_db_instance" "primary_db" {
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t2.micro"
  name                 = "primarydb"
  username             = "admin"
  password             = "password"
  parameter_group_name = "default.mysql5.6"
  multi_az             = true
  storage_type         = "gp2"
}

resource "aws_db_instance" "secondary_db" {
  provider             = aws.ap-southeast-1
  replicate_source_db  = aws_db_instance.primary_db.arn
  instance_class       = "db.t2.micro"
  storage_type         = "gp2"
  username             = "admin"
  password             = "password"
  skip_final_snapshot  = true
}

# Step 3: Create S3 Buckets
resource "aws_s3_bucket" "primary_media_bucket" {
  bucket = "primary-media-bucket"
  region = "us-east-1"
}

resource "aws_s3_bucket" "secondary_media_bucket" {
  provider = aws.ap-southeast-1
  bucket   = "secondary-media-bucket"
  region   = "ap-southeast-1"
}

# Step 4: Enable Versioning
resource "aws_s3_bucket_versioning" "primary_versioning" {
  bucket = aws_s3_bucket.primary_media

_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "secondary_versioning" {
  provider = aws.ap-southeast-1
  bucket   = aws_s3_bucket.secondary_media_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Step 5: Configure Replication
resource "aws_s3_bucket_replication_configuration" "replication" {
  provider = aws.ap-southeast-1
  bucket   = aws_s3_bucket.secondary_media_bucket.id

  role = aws_iam_role.replication_role.arn

  rules {
    id     = "replication-rule"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.secondary_media_bucket.arn
      storage_class = "STANDARD"
    }

    filter {
      prefix = ""
    }
  }
}

# Step 6: Create IAM Role and Policy
resource "aws_iam_role" "replication_role" {
  name = "replication-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "replication_policy" {
  name        = "replication-policy"
  description = "Policy for S3 bucket replication"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetReplicationConfiguration",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.primary_media_bucket.id}"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObjectVersion",
        "s3:GetObjectVersionAcl"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.primary_media_bucket.id}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ReplicateObject",
        "s3:ReplicateDelete"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.secondary_media_bucket.id}/*"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "replication_policy_attachment" {
  role       = aws_iam_role.replication_role.name
  policy_arn = aws_iam_policy.replication_policy.arn
}

# Step 7: Configure Route 53 DNS Failover
resource "aws_route53_health_check" "primary_health_check" {
  fqdn             = "primary.streaming-service.com"
  type             = "HTTP"
  resource_path    = "/health"
  port             = 80
  failure_threshold = 3
}

resource "aws_route53_health_check" "secondary_health_check" {
  fqdn             = "secondary.streaming-service.com"
  type             = "HTTP"
  resource_path    = "/health"
  port             = 80
  failure_threshold = 3
}

resource "aws_route53_record" "primary_record" {
  zone_id = "Z3M3LMPEXAMPLE"
  name    = "streaming-service.com"
  type    = "A"
  ttl     = "60"

  set_identifier = "primary"
  weight         = 100
  records        = ["1.2.3.4"]  # Replace with the IP of your primary instance

  health_check_id = aws_route53_health_check.primary_health_check.id
}

resource "aws_route53_record" "secondary_record" {
  zone_id = "Z3M3LMPEXAMPLE"
  name    = "streaming-service.com"
  type    = "A"
  ttl     = "60"

  set_identifier = "secondary"
  weight         = 100
  records        = ["5.6.7.8"]  # Replace with the IP of your secondary instance

  health_check_id = aws_route53_health_check.secondary_health_check.id
}
```

### Example 3: E-Commerce Platform (Pilot Light)

#### Step-by-Step Guide

1. **Setup Providers**: Configure AWS providers for both primary and secondary regions.
2. **Create Primary RDS Instance**: Set up the primary RDS instance in the primary region.
3. **Create Secondary RDS Instance**: Set up the secondary RDS instance as a read replica in the secondary region.
4. **Create S3 Buckets**: Set up S3 buckets in both regions for backup and static content.
5. **Enable Versioning**: Enable versioning on both S3 buckets.
6. **Configure Replication**: Set up replication rules for the primary bucket to replicate objects to the secondary bucket.
7. **Create IAM Role and Policy**: Define the IAM role and policy needed for S3 replication.
8. **Configure Route 53 DNS Failover**: Set up health checks and DNS failover using Route 53.

#### Terraform Script

```hcl
# Step 1: Setup Providers
provider "aws" {
  region = "us-west-2"
}

provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}

# Step 2: Create Primary RDS Instance
resource "aws_db_instance" "primary_db" {
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t2.micro"
  name                 = "primarydb"
  username             = "admin"
  password             = "password"
  parameter_group_name = "default.mysql5.6"
  multi_az             = true
  storage_type         = "gp2"
}

# Step 3: Create Secondary RDS Instance
resource "aws_db_instance" "secondary_db" {
  provider            = aws.us-east-1
  replicate_source_db = aws_db_instance.primary_db.arn
  instance_class      = "db.t2.micro"
  storage_type        = "gp2"
  username            = "admin"
  password            = "password"
  skip_final_snapshot = true
}

# Step 4: Create S3 Buckets
resource "aws_s3_bucket" "primary_bucket" {
  bucket = "primary-ecommerce-bucket"
  region = "us-west-2"
}

resource "aws_s3_bucket" "secondary_bucket" {
  provider = aws.us-east-1
  bucket   = "secondary-ecommerce-bucket"
  region   = "us-east-1"
}

# Step 5: Enable Versioning
resource "aws_s3_bucket_versioning" "primary_versioning" {
  bucket = aws_s3_bucket.primary_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "secondary_versioning" {
  provider = aws.us-east-1
  bucket   = aws_s3_bucket.secondary_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Step 6: Configure Replication
resource "aws_s3_bucket_replication_configuration" "replication" {
  provider = aws.us-east-1
  bucket   = aws_s3_bucket.secondary_bucket.id

  role = aws_iam_role.replication_role.arn

  rules {
    id     = "replication-rule"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.secondary_bucket.arn
      storage_class = "STANDARD"
    }

    filter {
      prefix = ""
    }
  }
}

# Step 7: Create IAM Role and Policy
resource "aws_iam_role" "replication_role" {
  name = "replication-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "replication_policy" {
  name        = "replication-policy"
  description = "Policy for S3 bucket replication"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetReplicationConfiguration",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.primary_bucket.id}"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObjectVersion",
        "s3:GetObjectVersionAcl"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.primary_bucket.id}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ReplicateObject",
        "s3:ReplicateDelete"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.secondary_bucket.id}/*"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "replication_policy_attachment" {
  role       = aws_iam_role.replication_role.name
  policy_arn = aws_iam_policy.replication_policy.

arn
}

# Step 8: Configure Route 53 DNS Failover
resource "aws_route53_health_check" "primary_health_check" {
  fqdn             = "primary.ecommerce.com"
  type             = "HTTP"
  resource_path    = "/health"
  port             = 80
  failure_threshold = 3
}

resource "aws_route53_health_check" "secondary_health_check" {
  fqdn             = "secondary.ecommerce.com"
  type             = "HTTP"
  resource_path    = "/health"
  port             = 80
  failure_threshold = 3
}

resource "aws_route53_record" "primary_record" {
  zone_id = "Z3M3LMPEXAMPLE"
  name    = "ecommerce.com"
  type    = "A"
  ttl     = "60"

  set_identifier = "primary"
  weight         = 100
  records        = ["1.2.3.4"]  # Replace with the IP of your primary instance

  health_check_id = aws_route53_health_check.primary_health_check.id
}

resource "aws_route53_record" "secondary_record" {
  zone_id = "Z3M3LMPEXAMPLE"
  name    = "ecommerce.com"
  type    = "A"
  ttl     = "60"

  set_identifier = "secondary"
  weight         = 100
  records        = ["5.6.7.8"]  # Replace with the IP of your secondary instance

  health_check_id = aws_route53_health_check.secondary_health_check.id
}
```

### Example 4: Healthcare Provider (Backup and Restore)

#### Step-by-Step Guide

1. **Setup Provider**: Configure the AWS provider.
2. **Create RDS Instance**: Set up the RDS instance with automated backups.
3. **Create S3 Bucket**: Set up an S3 bucket for storing backups with versioning and lifecycle policies.
4. **Create Backup Vault**: Set up an AWS Backup Vault for storing backup plans and selections.
5. **Create KMS Key**: Set up a KMS key for encrypting backups.
6. **Create Backup Plan**: Define a backup plan with schedules and lifecycle policies.
7. **Create Backup Selection**: Define resources to be backed up by the backup plan.
8. **Create IAM Role**: Define the IAM role for AWS Backup.
9. **Create Lambda Function**: Set up a Lambda function for automating restores.
10. **Create IAM Role for Lambda**: Define the IAM role and policies for the Lambda function.

#### Terraform Script

```hcl
# Step 1: Setup Provider
provider "aws" {
  region = "us-east-1"
}

# Step 2: Create RDS Instance
resource "aws_db_instance" "db_instance" {
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t2.micro"
  name                 = "healthcaredb"
  username             = "admin"
  password             = "password"
  parameter_group_name = "default.mysql5.6"
  multi_az             = true
  storage_type         = "gp2"
  backup_retention_period = 7
  backup_window        = "03:00-04:00"
}

# Step 3: Create S3 Bucket
resource "aws_s3_bucket" "backup_bucket" {
  bucket = "healthcare-backup-bucket"
  region = "us-east-1"
  versioning {
    enabled = true
  }
  lifecycle_rule {
    id      = "archive"
    enabled = true
    transition {
      days          = 30
      storage_class = "GLACIER"
    }
    expiration {
      days = 365
    }
  }
}

# Step 4: Create Backup Vault
resource "aws_backup_vault" "backup_vault" {
  name        = "healthcare-backup-vault"
  kms_key_arn = aws_kms_key.backup_key.arn
}

# Step 5: Create KMS Key
resource "aws_kms_key" "backup_key" {
  description             = "KMS key for backup encryption"
  deletion_window_in_days = 10
}

# Step 6: Create Backup Plan
resource "aws_backup_plan" "daily_backup" {
  name = "daily-backup"

  rule {
    rule_name         = "daily-backup"
    target_vault_name = aws_backup_vault.backup_vault.name
    schedule          = "cron(0 3 * * ? *)"

    lifecycle {
      cold_storage_after = 30
      delete_after       = 365
    }
  }
}

# Step 7: Create Backup Selection
resource "aws_backup_selection" "backup_selection" {
  iam_role_arn   = aws_iam_role.backup_role.arn
  name           = "daily-backup-selection"
  backup_plan_id = aws_backup_plan.daily_backup.id

  resources = [
    aws_db_instance.db_instance.arn
  ]
}

# Step 8: Create IAM Role for Backup
resource "aws_iam_role" "backup_role" {
  name = "backup_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "backup.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "backup_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
  role       = aws_iam_role.backup_role.name
}

# Step 9: Create Lambda Function for Restore Automation
resource "aws_lambda_function" "restore_function" {
  filename         = "restore_function.zip"
  function_name    = "restore_function"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "restore_function.handler"
  source_code_hash = filebase64sha256("restore_function.zip")
  runtime          = "python3.8"
  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.backup_bucket.bucket
    }
  }
}

# Step 10: Create IAM Role for Lambda
resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_exec.name
}

resource "aws_iam_policy_attachment" "s3_access_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
  role       = aws_iam_role.lambda_exec.name
}
```

This detailed guide and corresponding Terraform scripts provide a comprehensive approach to implementing backup strategies and disaster recovery plans on AWS for different real-world scenarios. Adjust and expand them as necessary to match your specific requirements and environment.
