## Detailed Guide on High Availability Concepts in AWS

High availability in AWS refers to the architecture and practices that ensure applications and services remain accessible and operational under various conditions. Achieving high availability involves redundancy, fault tolerance, and automated recovery mechanisms. Here's a detailed guide on the key concepts and practices:

### 1. **Regions and Availability Zones (AZs)**

#### **Regions:**
- AWS infrastructure is divided into geographical regions. Each region is independent and contains multiple Availability Zones.
- Examples: us-east-1 (N. Virginia), eu-west-1 (Ireland).

#### **Availability Zones:**
- AZs are isolated locations within a region, each with its own power, cooling, and networking.
- Using multiple AZs ensures that application failures are isolated and do not affect other AZs.

### 2. **Elastic Load Balancing (ELB)**

#### **Types of Load Balancers:**
- **Application Load Balancer (ALB):** Operates at the application layer (HTTP/HTTPS), suitable for web applications.
- **Network Load Balancer (NLB):** Operates at the transport layer (TCP/UDP), suitable for high-performance networking.
- **Classic Load Balancer (CLB):** Legacy option for both application and network layers.

#### **Features:**
- Distributes incoming traffic across multiple instances in multiple AZs.
- Health checks to route traffic only to healthy instances.

### 3. **Auto Scaling**

#### **Auto Scaling Groups (ASG):**
- Automatically adjusts the number of instances based on demand.
- Ensures a minimum and maximum number of instances to handle traffic spikes and reduce costs during low demand.

#### **Scaling Policies:**
- **Dynamic Scaling:** Responds to changes in demand.
- **Predictive Scaling:** Forecasts future traffic based on historical data.

### 4. **Amazon Route 53**

#### **DNS Service:**
- Provides domain name resolution (DNS) and routes end-user requests to the appropriate service endpoint.

#### **Routing Policies:**
- **Simple Routing:** Maps a domain to a single resource.
- **Weighted Routing:** Distributes traffic across multiple resources based on specified weights.
- **Latency-based Routing:** Routes traffic to the lowest latency endpoint.
- **Failover Routing:** Automatically redirects traffic to standby resources if the primary resource fails.
- **Geolocation Routing:** Directs traffic based on the user's location.

### 5. **Data Replication**

#### **Amazon S3 Cross-Region Replication (CRR):**
- Automatically replicates objects across buckets in different AWS regions.

#### **Amazon RDS Multi-AZ Deployment:**
- Provides synchronous replication across AZs for high availability and automated failover.

#### **Amazon Aurora Global Database:**
- Spans multiple regions with fast local reads and disaster recovery from region-wide outages.

### 6. **Fault Tolerance and Recovery**

#### **Amazon EC2 Auto Recovery:**
- Monitors instances and automatically recovers them in case of a failure.

#### **AWS Backup:**
- Centralized service to automate and manage backups across AWS services.

#### **Amazon EFS and Amazon FSx:**
- Provides highly available and durable file storage across multiple AZs.

### 7. **Disaster Recovery (DR) Strategies**

#### **Backup and Restore:**
- Regularly back up data and applications and restore them during a disaster.

#### **Pilot Light:**
- Minimal, essential infrastructure is always running, with the ability to scale up rapidly.

#### **Warm Standby:**
- A scaled-down version of a fully functional environment is running and can be scaled up when needed.

#### **Multi-Site Active/Active:**
- Fully redundant environments in multiple regions actively serving traffic.

### 8. **Monitoring and Alerts**

#### **Amazon CloudWatch:**
- Collects monitoring and operational data, including metrics and logs.
- Sets alarms and triggers automated actions based on thresholds.

#### **AWS CloudTrail:**
- Logs API calls and activities for governance, compliance, and operational audits.

#### **AWS Trusted Advisor:**
- Provides real-time guidance to help provision resources following AWS best practices.

### 9. **Security Considerations**

#### **IAM Roles and Policies:**
- Implement fine-grained access control for resources.

#### **AWS Shield and AWS WAF:**
- Protect against DDoS attacks and web application vulnerabilities.

#### **Encryption:**
- Use AWS Key Management Service (KMS) for data encryption at rest and in transit.

### Conclusion

Implementing high availability in AWS involves a combination of architectural strategies, automated management tools, and best practices. By leveraging the services and features provided by AWS, you can ensure that your applications remain resilient, available, and performant under various conditions.


### Real-World Examples of High Availability in AWS

#### Example 1: E-Commerce Website

**Scenario:** 
An e-commerce company wants to host its online store on AWS with high availability, security, and scalability.

**Architecture Overview:**
1. **Region and AZs:** Deploy the application in the us-east-1 region across three Availability Zones (AZs).
2. **Elastic Load Balancing (ELB):** Use an Application Load Balancer (ALB) to distribute incoming traffic across multiple EC2 instances in different AZs.
3. **Auto Scaling:** Configure an Auto Scaling group to ensure the number of EC2 instances adjusts based on traffic demands.
4. **Amazon RDS Multi-AZ:** Use Amazon RDS for MySQL with Multi-AZ deployment for the database to ensure high availability and automatic failover.
5. **Amazon S3:** Store static content (images, CSS, JavaScript) in Amazon S3 with Cross-Region Replication for disaster recovery.
6. **Amazon CloudFront:** Use CloudFront as a Content Delivery Network (CDN) to cache static content at edge locations worldwide, reducing latency.
7. **Amazon Route 53:** Implement Route 53 for DNS with latency-based routing to direct users to the nearest ALB.
8. **Security:** Utilize AWS WAF to protect against common web exploits and AWS Shield for DDoS protection.
9. **Monitoring and Alerts:** Set up CloudWatch to monitor application performance and create alarms for critical metrics.

**Terraform Script (Simplified):**
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "subnet_1" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "subnet_2" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "us-east-1b"
}

resource "aws_subnet" "subnet_3" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.3.0/24"
  availability_zone = "us-east-1c"
}

resource "aws_instance" "web" {
  count         = 3
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = element([aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id], count.index)
  security_groups = [aws_security_group.web_sg.id]
}

resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Allow web traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_alb" "main" {
  name            = "main-alb"
  internal        = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.web_sg.id]
  subnets         = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
}

resource "aws_autoscaling_group" "web_asg" {
  desired_capacity     = 3
  max_size             = 6
  min_size             = 3
  vpc_zone_identifier  = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
  launch_configuration = aws_launch_configuration.web_lc.id

  tag {
    key                 = "Name"
    value               = "web-server"
    propagate_at_launch = true
  }
}

resource "aws_launch_configuration" "web_lc" {
  name          = "web-lc"
  image_id      = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  security_groups = [aws_security_group.web_sg.id]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_rds_instance" "main" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "mydb"
  username             = "admin"
  password             = "password"
  multi_az             = true
  publicly_accessible  = false
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  db_subnet_group_name = aws_db_subnet_group.main.name
}

resource "aws_db_subnet_group" "main" {
  name       = "main"
  subnet_ids = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
}

resource "aws_security_group" "db_sg" {
  name        = "db-sg"
  description = "Allow database traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

#### Example 2: Financial Services Application

**Scenario:** 
A financial services company needs a highly available, secure platform for processing transactions with real-time data replication.

**Architecture Overview:**
1. **Region and AZs:** Deploy the application in the eu-west-1 region across three AZs.
2. **Elastic Load Balancing (ELB):** Use a Network Load Balancer (NLB) for low-latency traffic distribution.
3. **Auto Scaling:** Implement Auto Scaling groups for the application servers to handle varying loads.
4. **Amazon Aurora Global Database:** Use Amazon Aurora with read replicas across multiple regions for low-latency reads and disaster recovery.
5. **Amazon S3:** Store backups and critical data in Amazon S3 with Cross-Region Replication.
6. **Amazon CloudFront:** Distribute static and dynamic content using CloudFront.
7. **Amazon Route 53:** Use Route 53 with geolocation routing to direct users to the nearest application endpoint.
8. **Security:** Utilize IAM roles for least privilege access, AWS Shield for DDoS protection, and AWS WAF for application security.
9. **Monitoring and Alerts:** Set up CloudWatch and AWS Config for compliance and monitoring.

#### Example 3: Media Streaming Service

**Scenario:** 
A media streaming service wants to ensure uninterrupted streaming experience with global reach.

**Architecture Overview:**
1. **Region and AZs:** Deploy the service in multiple regions (us-west-1, eu-central-1, ap-southeast-1) to provide global coverage.
2. **Elastic Load Balancing (ELB):** Use Application Load Balancers (ALBs) in each region to distribute traffic across multiple AZs.
3. **Auto Scaling:** Configure Auto Scaling groups to scale up and down based on the number of concurrent viewers.
4. **Amazon S3:** Store media content in Amazon S3 with Cross-Region Replication.
5. **Amazon CloudFront:** Use CloudFront to cache and deliver media content with low latency.
6. **Amazon Route 53:** Implement Route 53 with latency-based routing to direct users to the nearest region.
7. **Security:** Use IAM roles and policies, AWS Shield for DDoS protection, and AWS WAF to protect the web applications.
8. **Monitoring and Alerts:** Set up CloudWatch for real-time monitoring and AWS X-Ray for tracing requests and identifying performance bottlenecks.

These real-world examples illustrate how different types of applications can leverage AWS services and best practices to achieve high availability, security, and scalability.



Here are the Terraform scripts for each of the real-world examples described:

### Example 1: E-Commerce Website

#### Terraform Script:
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"
}

resource "aws_subnet" "subnet_3" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1c"
}

resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Allow web traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  count         = 3
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = element([aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id], count.index)
  security_groups = [aws_security_group.web_sg.id]
}

resource "aws_alb" "main" {
  name            = "main-alb"
  internal        = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.web_sg.id]
  subnets         = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
}

resource "aws_autoscaling_group" "web_asg" {
  desired_capacity     = 3
  max_size             = 6
  min_size             = 3
  vpc_zone_identifier  = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
  launch_configuration = aws_launch_configuration.web_lc.id

  tag {
    key                 = "Name"
    value               = "web-server"
    propagate_at_launch = true
  }
}

resource "aws_launch_configuration" "web_lc" {
  name          = "web-lc"
  image_id      = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  security_groups = [aws_security_group.web_sg.id]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_rds_instance" "main" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "mydb"
  username             = "admin"
  password             = "password"
  multi_az             = true
  publicly_accessible  = false
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  db_subnet_group_name = aws_db_subnet_group.main.name
}

resource "aws_db_subnet_group" "main" {
  name       = "main"
  subnet_ids = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
}

resource "aws_security_group" "db_sg" {
  name        = "db-sg"
  description = "Allow database traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### Example 2: Financial Services Application

#### Terraform Script:
```hcl
provider "aws" {
  region = "eu-west-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-west-1a"
}

resource "aws_subnet" "subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-west-1b"
}

resource "aws_subnet" "subnet_3" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "eu-west-1c"
}

resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Allow web traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  count         = 3
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = element([aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id], count.index)
  security_groups = [aws_security_group.web_sg.id]
}

resource "aws_alb" "main" {
  name            = "main-alb"
  internal        = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.web_sg.id]
  subnets         = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
}

resource "aws_autoscaling_group" "web_asg" {
  desired_capacity     = 3
  max_size             = 6
  min_size             = 3
  vpc_zone_identifier  = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
  launch_configuration = aws_launch_configuration.web_lc.id

  tag {
    key                 = "Name"
    value               = "web-server"
    propagate_at_launch = true
  }
}

resource "aws_launch_configuration" "web_lc" {
  name          = "web-lc"
  image_id      = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  security_groups = [aws_security_group.web_sg.id]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_aurora_cluster" "main" {
  cluster_identifier = "aurora-cluster"
  engine             = "aurora-mysql"
  engine_version     = "5.7.mysql_aurora.2.03.4"
  master_username    = "admin"
  master_password    = "password"

  db_subnet_group_name = aws_db_subnet_group.main.name

  vpc_security_group_ids = [aws_security_group.db_sg.id]

  depends_on = [aws_rds_cluster_instance.instance_1, aws_rds_cluster_instance.instance_2]
}

resource "aws_rds_cluster_instance" "instance_1" {
  identifier        = "aurora-instance-1"
  cluster_identifier = aws_aurora_cluster.main.id
  instance_class    = "db.t3.medium"
  engine            = aws_aurora_cluster.main.engine


  engine_version    = aws_aurora_cluster.main.engine_version
  publicly_accessible = false
}

resource "aws_rds_cluster_instance" "instance_2" {
  identifier        = "aurora-instance-2"
  cluster_identifier = aws_aurora_cluster.main.id
  instance_class    = "db.t3.medium"
  engine            = aws_aurora_cluster.main.engine
  engine_version    = aws_aurora_cluster.main.engine_version
  publicly_accessible = false
}

resource "aws_db_subnet_group" "main" {
  name       = "main"
  subnet_ids = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
}

resource "aws_security_group" "db_sg" {
  name        = "db-sg"
  description = "Allow database traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### Example 3: Media Streaming Service

#### Terraform Script:
```hcl
provider "aws" {
  region = "us-west-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-west-1a"
}

resource "aws_subnet" "subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-west-1b"
}

resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Allow web traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  count         = 2
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = element([aws_subnet.subnet_1.id, aws_subnet.subnet_2.id], count.index)
  security_groups = [aws_security_group.web_sg.id]
}

resource "aws_alb" "main" {
  name            = "main-alb"
  internal        = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.web_sg.id]
  subnets         = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id]
}

resource "aws_autoscaling_group" "web_asg" {
  desired_capacity     = 2
  max_size             = 4
  min_size             = 2
  vpc_zone_identifier  = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id]
  launch_configuration = aws_launch_configuration.web_lc.id

  tag {
    key                 = "Name"
    value               = "web-server"
    propagate_at_launch = true
  }
}

resource "aws_launch_configuration" "web_lc" {
  name          = "web-lc"
  image_id      = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  security_groups = [aws_security_group.web_sg.id]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_cloudfront_distribution" "media" {
  origin {
    domain_name = aws_s3_bucket.media.bucket_regional_domain_name
    origin_id   = "media-s3-origin"
  }

  enabled             = true
  default_cache_behavior {
    target_origin_id       = "media-s3-origin"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

resource "aws_s3_bucket" "media" {
  bucket = "media-bucket"
  acl    = "private"
}

resource "aws_s3_bucket_replication_configuration" "media" {
  bucket = aws_s3_bucket.media.bucket

  role = aws_iam_role.replication_role.arn

  rule {
    id     = "ReplicationRule"
    status = "Enabled"

    destination {
      bucket = aws_s3_bucket.replica.arn
    }
  }
}

resource "aws_s3_bucket" "replica" {
  bucket = "media-bucket-replica"
  acl    = "private"
  region = "eu-central-1"
}

resource "aws_iam_role" "replication_role" {
  name = "replication-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      },
    ]
  })
}

resource "aws_iam_role_policy" "replication_policy" {
  name = "replication-policy"
  role = aws_iam_role.replication_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetReplicationConfiguration",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.media.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObjectVersion",
          "s3:GetObjectVersionAcl"
        ]
        Resource = [
          "${aws_s3_bucket.media.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ReplicateObject",
          "s3:ReplicateDelete",
          "s3:ReplicateTags"
        ]
        Resource = [
          "${aws_s3_bucket.replica.arn}/*"
        ]
      }
    ]
  })
}
```

These scripts provide a foundation for deploying high-availability architectures on AWS for different scenarios. You can further customize them based on specific requirements and best practices.
