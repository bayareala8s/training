## AWS Disaster Recovery Guide

### Introduction
Disaster recovery (DR) on AWS involves planning and implementing strategies to recover critical IT systems and data quickly and efficiently after a disaster. AWS offers various tools and services that enable businesses to create robust DR solutions. This guide will provide a comprehensive overview of AWS DR strategies, services, and best practices.

### Disaster Recovery Strategies
1. **Backup and Restore**
   - **Description**: Data is regularly backed up to Amazon S3, Amazon Glacier, or other storage services. In the event of a disaster, these backups are restored to recover the system.
   - **Use Case**: Suitable for non-critical systems with a higher Recovery Time Objective (RTO) and Recovery Point Objective (RPO).

2. **Pilot Light**
   - **Description**: A minimal version of the critical systems runs on AWS, with the full environment activated only during a disaster.
   - **Use Case**: Appropriate for systems that require faster recovery but can tolerate some downtime.

3. **Warm Standby**
   - **Description**: A scaled-down version of a fully functional environment is always running on AWS. In case of a disaster, this environment is scaled up to handle the full production load.
   - **Use Case**: Suitable for critical systems requiring lower RTO and RPO.

4. **Multi-Site (Active-Active)**
   - **Description**: Fully functional systems are running simultaneously in two or more locations. Traffic is distributed across these sites, and if one fails, the others take over.
   - **Use Case**: Ideal for mission-critical systems needing near-zero RTO and RPO.

### AWS Services for Disaster Recovery

1. **Amazon S3 and Amazon Glacier**
   - **Use**: Store and archive backups with high durability and availability.
   - **Features**: Versioning, Lifecycle policies, Cross-Region Replication.

2. **AWS Backup**
   - **Use**: Centralized backup service to automate and manage backups across AWS services.
   - **Features**: Policy-based management, automated backups, compliance monitoring.

3. **Amazon RDS and Aurora**
   - **Use**: Managed relational databases with automated backups and snapshots.
   - **Features**: Multi-AZ deployments, automated failover, read replicas.

4. **Amazon EC2**
   - **Use**: Run virtual servers in the cloud.
   - **Features**: AMI snapshots, EBS snapshots, Auto Scaling.

5. **AWS Lambda**
   - **Use**: Serverless compute for automating DR processes.
   - **Features**: Trigger-based execution, integration with other AWS services.

6. **AWS CloudFormation**
   - **Use**: Automate the provisioning and management of AWS resources.
   - **Features**: Infrastructure as Code (IaC), templates for creating environments.

7. **AWS Route 53**
   - **Use**: Scalable DNS service.
   - **Features**: Health checks, DNS failover, traffic routing policies.

8. **Amazon VPC**
   - **Use**: Isolate your AWS resources in a virtual network.
   - **Features**: VPC peering, Transit Gateways, subnets, security groups.

### Best Practices for Disaster Recovery on AWS

1. **Define RTO and RPO**: Clearly define the Recovery Time Objective (RTO) and Recovery Point Objective (RPO) for your critical systems.

2. **Use Multiple Regions**: Distribute your DR infrastructure across multiple AWS regions to mitigate the risk of a regional outage.

3. **Automate DR Processes**: Use AWS Lambda and CloudFormation to automate recovery processes and minimize human intervention.

4. **Regular Testing**: Regularly test your DR plans to ensure they work as expected. Simulate different disaster scenarios and evaluate the effectiveness of your recovery strategies.

5. **Data Encryption**: Encrypt your backups and data in transit and at rest to ensure security and compliance.

6. **Monitor and Audit**: Use AWS CloudTrail and Amazon CloudWatch to monitor your DR processes and maintain an audit trail of all activities.

7. **Document and Update DR Plans**: Keep your DR plans well-documented and regularly updated to reflect any changes in your infrastructure or business requirements.

### Example DR Scenario: E-commerce Website

#### Scenario
An e-commerce company wants to ensure its online store remains available and secure during a disaster. The company opts for a warm standby DR strategy.

#### Architecture

1. **Primary Region (us-east-1)**
   - **Amazon RDS (Multi-AZ)**: Primary database instance with automated backups.
   - **Amazon EC2 Auto Scaling Group**: For web servers and application servers.
   - **Amazon S3**: For static content and backups.
   - **Amazon Route 53**: For DNS and health checks.

2. **Secondary Region (us-west-2)**
   - **Amazon RDS (Read Replica)**: Read replica for the primary database.
   - **Amazon EC2 Auto Scaling Group**: Smaller instance pool mirroring the primary region.
   - **Amazon S3**: For replicating backups.
   - **Amazon Route 53**: For failover routing.

#### Failover Process

1. **Database Failover**: Amazon RDS automatically fails over to the secondary region's read replica if the primary instance is unavailable.
2. **DNS Failover**: Amazon Route 53 health checks detect the failure and redirect traffic to the secondary region.
3. **Scaling Up**: Auto Scaling in the secondary region increases the instance count to handle the full production load.
4. **Data Sync**: Regularly sync data and application state between regions using AWS DataSync or custom scripts.

### Conclusion

AWS offers a comprehensive suite of tools and services for implementing effective disaster recovery strategies. By leveraging these resources, businesses can ensure their critical systems remain resilient and available, even in the face of unexpected disasters. Implementing a robust DR plan tailored to specific needs and regularly testing and updating it is crucial for maintaining business continuity.


### Real-World Examples of AWS Disaster Recovery

#### Example 1: Financial Services Firm

**Company**: A large financial services firm.

**Challenge**: Ensure continuous availability and data integrity for critical banking applications.

**DR Strategy**: Multi-Site (Active-Active)

**Architecture**:
- **Regions**: us-east-1 and eu-west-1
- **Amazon RDS (Aurora Multi-Master)**: For synchronous replication of databases across regions.
- **Amazon EC2 Auto Scaling**: For application servers running in both regions.
- **Amazon Route 53**: For global DNS routing and failover.
- **Amazon S3**: For storing backups and static content with cross-region replication enabled.
- **AWS Lambda**: For automating failover procedures and health checks.
- **Amazon CloudWatch**: For monitoring and alerting on application performance and availability.

**Implementation**:
- **Database Replication**: Aurora Multi-Master setup to ensure that database writes can occur in multiple regions simultaneously.
- **Global Load Balancing**: Route 53 is configured with latency-based routing and health checks to direct traffic to the closest healthy region.
- **Automated Failover**: Lambda functions automatically trigger failover procedures in case of regional outages, scaling up resources in the active region.

**Outcome**:
- Achieved near-zero RTO and RPO.
- Continuous availability of critical banking applications.
- Seamless customer experience without noticeable downtime.

#### Example 2: Media Streaming Service

**Company**: A global media streaming service provider.

**Challenge**: Ensure uninterrupted streaming services to a global audience.

**DR Strategy**: Warm Standby

**Architecture**:
- **Primary Region**: us-east-1
- **Secondary Region**: ap-southeast-1
- **Amazon RDS (Multi-AZ)**: For the primary database with read replicas in the secondary region.
- **Amazon EC2**: For application and streaming servers, with a scaled-down version running in the secondary region.
- **Amazon S3**: For content storage with cross-region replication.
- **Amazon CloudFront**: For global content delivery.
- **Amazon Route 53**: For DNS and health checks.

**Implementation**:
- **Database Read Replicas**: Regularly updated read replicas in the secondary region to ensure data availability.
- **Content Replication**: S3 cross-region replication to keep media content in sync between regions.
- **Scalable Infrastructure**: Auto Scaling in the secondary region set to quickly scale up the number of instances when needed.
- **DNS Failover**: Route 53 configured to detect failures and route traffic to the secondary region.

**Outcome**:
- Reduced downtime and minimal disruption during regional failures.
- Fast recovery times due to pre-provisioned resources in the secondary region.
- Consistent and reliable streaming service for users worldwide.

#### Example 3: E-Commerce Platform

**Company**: A leading e-commerce platform.

**Challenge**: Maintain high availability and protect sensitive customer data.

**DR Strategy**: Pilot Light

**Architecture**:
- **Primary Region**: us-west-2
- **Secondary Region**: us-east-1
- **Amazon RDS**: Primary database in the primary region, with periodic snapshots copied to the secondary region.
- **Amazon EC2**: Critical application components running in the primary region, with minimal instances in the secondary region.
- **Amazon S3**: For backup storage and static content with cross-region replication.
- **AWS CloudFormation**: For automating the provisioning of infrastructure.
- **Amazon Route 53**: For DNS failover and health checks.

**Implementation**:
- **Database Snapshots**: Regular RDS snapshots copied to the secondary region to ensure data availability.
- **Pre-Provisioned Resources**: Essential services running in a minimal state in the secondary region, ready to scale up when needed.
- **Automated Provisioning**: CloudFormation templates to quickly launch and configure the necessary resources in the secondary region during a disaster.
- **DNS Failover**: Route 53 configured to reroute traffic to the secondary region when primary services are unavailable.

**Outcome**:
- Efficient use of resources with cost savings by maintaining minimal standby infrastructure.
- Quick recovery with automated scaling and provisioning in the secondary region.
- Ensured data protection and availability with regular snapshots and backups.

#### Example 4: Healthcare Provider

**Company**: A large healthcare provider with multiple clinics and hospitals.

**Challenge**: Protect patient data and ensure availability of healthcare applications.

**DR Strategy**: Backup and Restore

**Architecture**:
- **Primary Region**: us-east-1
- **Amazon RDS**: For patient records and other critical databases.
- **Amazon S3**: For storing backups, patient records, and other important data.
- **AWS Backup**: For centralized backup management.
- **AWS Lambda**: For automating backup and restore processes.
- **Amazon Route 53**: For DNS management.

**Implementation**:
- **Automated Backups**: Using AWS Backup to schedule and manage regular backups of databases and file systems.
- **Data Archiving**: Storing long-term backups and historical data in Amazon Glacier for cost-effective storage.
- **Automated Restore**: Lambda functions to automate the restoration of backups in case of data loss or corruption.
- **DNS Management**: Route 53 configured to manage DNS records for healthcare applications.

**Outcome**:
- Reliable backup and restore processes ensuring data integrity and availability.
- Cost-effective storage of backups and archived data.
- Enhanced data protection and compliance with healthcare regulations.

### Conclusion

These real-world examples demonstrate how AWS services can be leveraged to implement robust disaster recovery strategies tailored to different industries and use cases. By carefully planning and using AWS tools, businesses can achieve high availability, protect critical data, and ensure business continuity even in the face of unexpected disasters.



Here are the Terraform scripts for each of the real-world examples provided:

### Example 1: Financial Services Firm (Multi-Site Active-Active)

```hcl
# Provider configuration
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "eu-west-1"
  region = "eu-west-1"
}

# S3 buckets for cross-region replication
resource "aws_s3_bucket" "primary_bucket" {
  bucket = "primary-financial-services-bucket"
  region = "us-east-1"
}

resource "aws_s3_bucket" "secondary_bucket" {
  provider = aws.eu-west-1
  bucket   = "secondary-financial-services-bucket"
  region   = "eu-west-1"
}

# Enable versioning on both buckets
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

# Enable replication from primary to secondary bucket
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

# IAM role and policy for replication
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

# CloudFront distribution for global content delivery
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

# Route 53 DNS failover configuration
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
  records        = [aws_instance.primary_instance.public_ip]

  health_check_id = aws_route53_health_check.primary_health_check.id
}

resource "aws_route53_record" "secondary_record" {
  zone_id = "Z3M3LMPEXAMPLE"
  name    = "example.com"
  type    = "A"
  ttl     = "60"

  set_identifier = "secondary"
  weight         = 100
  records        = [aws_instance.secondary_instance.public_ip]

  health_check_id = aws_route53_health_check.secondary_health_check.id
}
```

### Example 2: Media Streaming Service (Warm Standby)

```hcl
# Provider configuration
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "ap-southeast-1"
  region = "ap-southeast-1"
}

# RDS instance in primary region
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

# Read replica in secondary region
resource "aws_db_instance" "secondary_db" {
  provider             = aws.ap-southeast-1
  replicate_source_db  = aws_db_instance.primary_db.arn
  instance_class       = "db.t2.micro"
  storage_type         = "gp2"
  username             = "admin"
  password             = "password"
  skip_final_snapshot  = true
}

# S3 bucket for media content with cross-region replication
resource "aws_s3_bucket" "primary_media_bucket" {
  bucket = "primary-media-bucket"
  region = "us-east-1"
}

resource "aws_s3_bucket" "secondary_media_bucket" {
  provider = aws.ap-southeast-1
  bucket   = "secondary-media-bucket"
  region   = "ap-southeast-1"
}

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

# IAM role and policy for replication
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
      "

Action": [
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

# Route 53 DNS failover configuration
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
  records        = [aws_instance.primary_instance.public_ip]

  health_check_id = aws_route53_health_check.primary_health_check.id
}

resource "aws_route53_record" "secondary_record" {
  zone_id = "Z3M3LMPEXAMPLE"
  name    = "streaming-service.com"
  type    = "A"
  ttl     = "60"

  set_identifier = "secondary"
  weight         = 100
  records        = [aws_instance.secondary_instance.public_ip]

  health_check_id = aws_route53_health_check.secondary_health_check.id
}
```

### Example 3: E-Commerce Platform (Pilot Light)

```hcl
# Provider configuration
provider "aws" {
  region = "us-west-2"
}

provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}

# Primary RDS instance
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

# Secondary RDS instance in pilot light configuration
resource "aws_db_instance" "secondary_db" {
  provider            = aws.us-east-1
  replicate_source_db = aws_db_instance.primary_db.arn
  instance_class      = "db.t2.micro"
  storage_type        = "gp2"
  username            = "admin"
  password            = "password"
  skip_final_snapshot = true
}

# S3 buckets for backup and static content with cross-region replication
resource "aws_s3_bucket" "primary_bucket" {
  bucket = "primary-ecommerce-bucket"
  region = "us-west-2"
}

resource "aws_s3_bucket" "secondary_bucket" {
  provider = aws.us-east-1
  bucket   = "secondary-ecommerce-bucket"
  region   = "us-east-1"
}

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

# IAM role and policy for replication
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

# Route 53 DNS failover configuration
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
  records        = [aws_instance.primary_instance.public_ip]

  health_check_id = aws_route53_health_check.primary_health_check.id
}

resource "aws_route53_record" "secondary_record" {
  zone_id = "Z3M3LMPEXAMPLE"
  name    = "ecommerce.com"
  type    = "A"
  ttl     = "60"

  set_identifier = "secondary"
  weight         = 100
  records        = [aws_instance.secondary_instance.public_ip]

  health_check_id = aws_route53_health_check.secondary_health_check.id
}
```

### Example 4: Healthcare Provider (Backup and Restore)

```hcl
# Provider configuration
provider "aws" {
  region = "us-east-1"
}

# RDS instance
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

# S3 bucket for backups
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

# Backup plan
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

# Backup vault
resource "aws_backup_vault" "backup_vault" {
  name        = "healthcare-backup-vault"
  kms_key_arn = aws_kms_key.backup_key.arn
}

# KMS key for encryption
resource "aws_kms_key" "backup_key" {
  description             = "KMS key for backup encryption"
  deletion_window_in_days = 10
}

# Backup selection
resource "aws_backup_selection" "backup_selection" {
  iam_role_arn   = aws_iam_role.backup_role.arn
  name           = "daily-backup-selection"
  backup_plan_id = aws_backup_plan.daily_backup.id

  resources = [
    aws_db_instance.db_instance.arn
  ]
}

# IAM role for backup
resource "aws_

iam_role" "backup_role" {
  name = "backup-role"

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

# Lambda function for restore automation
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

# IAM role for Lambda
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

These scripts provide a foundational setup for each disaster recovery strategy. Adjust and expand them as necessary to match your specific requirements and environment.
