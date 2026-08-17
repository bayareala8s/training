Here are a few detailed real-world case studies and architectures for AWS across different industries:

### 1. E-Commerce Company Hosting an Online Store

#### Objective:
An e-commerce company wants to host its online store on AWS with high availability, security, and scalability.

#### Architecture:
- **VPC Configuration**:
  - **VPC**: A single VPC with CIDR block 10.0.0.0/16.
  - **Subnets**: Multiple subnets in different availability zones for redundancy.
    - Public Subnets: For Load Balancer, Bastion Host.
    - Private Subnets: For EC2 instances hosting the application, RDS instances.

- **Internet Gateway**: Attached to the VPC for internet access.

- **NAT Gateway**: In public subnets to allow instances in private subnets to access the internet.

- **Security Groups**: Strictly controlled to allow only necessary traffic.
  - Web Servers: Allow inbound traffic on port 80 (HTTP) and 443 (HTTPS).
  - Database Servers: Allow inbound traffic only from web servers on port 3306 (MySQL).

- **Elastic Load Balancer (ELB)**: Distributes incoming traffic across multiple EC2 instances.

- **EC2 Instances**: Auto-scaling groups to handle varying load.
  - Application servers in private subnets.
  - Bastion host in a public subnet for administrative access.

- **RDS (Relational Database Service)**: For the database, deployed in Multi-AZ for high availability.

- **S3**: For static content storage and backups.

- **CloudFront**: CDN for faster delivery of content to users.

- **Route 53**: DNS service to route traffic to the application.

- **CloudWatch**: Monitoring and logging.

#### Terraform Script (Partial):
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
  map_public_ip_on_launch = true
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 2}.0/24"
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = element(aws_subnet.public.*.id, 0)
}

resource "aws_eip" "nat" {
  vpc = true
}

resource "aws_security_group" "web" {
  vpc_id = aws_vpc.main.id

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

resource "aws_security_group" "db" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Additional resources for ELB, EC2 instances, RDS, etc.
```

### 2. Media Streaming Service

#### Objective:
A media streaming service needs a scalable architecture to handle high traffic and deliver content seamlessly to a global audience.

#### Architecture:
- **VPC**: Configured with public and private subnets across multiple availability zones.

- **Elastic Load Balancer**: Distributes incoming traffic to the media servers.

- **EC2 Instances**: Auto-scaling groups for media servers to handle varying load.

- **S3**: Storage for media files.

- **CloudFront**: CDN to cache content and deliver it quickly to users globally.

- **DynamoDB**: NoSQL database for storing metadata about media files.

- **Elastic Transcoder**: To transcode media files into different formats for various devices.

- **Route 53**: DNS service.

- **IAM**: Fine-grained access control to resources.

#### Terraform Script (Partial):
```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = element(["us-west-2a", "us-west-2b", "us-west-2c"], count.index)
  map_public_ip_on_launch = true
}

resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 3}.0/24"
  availability_zone = element(["us-west-2a", "us-west-2b", "us-west-2c"], count.index)
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_security_group" "web" {
  vpc_id = aws_vpc.main.id

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

resource "aws_s3_bucket" "media" {
  bucket = "media-bucket"
}

resource "aws_dynamodb_table" "media_metadata" {
  name         = "media_metadata"
  hash_key     = "media_id"

  attribute {
    name = "media_id"
    type = "S"
  }

  billing_mode = "PAY_PER_REQUEST"
}

# Additional resources for EC2 instances, CloudFront, etc.
```

### 3. Financial Services Company

#### Objective:
A financial services company wants a secure and compliant architecture for handling sensitive customer data.

#### Architecture:
- **VPC**: Configured with public and private subnets.

- **Direct Connect**: For secure, high-speed connection to on-premises data centers.

- **NAT Gateway**: Allows instances in private subnets to access the internet.

- **EC2 Instances**: For web servers, application servers, and backend processing.

- **RDS**: Multi-AZ deployment for databases.

- **S3**: For storing backups and logs.

- **KMS**: To manage encryption keys for data at rest.

- **CloudHSM**: Hardware security module for cryptographic operations.

- **IAM**: To manage access control.

- **CloudTrail**: For logging and monitoring API calls.

- **Config**: To monitor configuration changes.

- **WAF**: Web application firewall for additional security.

#### Terraform Script (Partial):
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
  map_public_ip_on_launch = true
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 2}.0/24"
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_security_group" "web" {
  vpc_id = aws_v

pc.main.id

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

resource "aws_rds_instance" "db" {
  allocated_storage    = 100
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.medium"
  name                 = "mydb"
  username             = "admin"
  password             = "password"
  skip_final_snapshot  = true
  multi_az             = true
  publicly_accessible  = false
  storage_encrypted    = true
  kms_key_id           = aws_kms_key.mykey.arn
  vpc_security_group_ids = [aws_security_group.web.id]
}

resource "aws_kms_key" "mykey" {
  description = "KMS key for RDS encryption"
}

# Additional resources for Direct Connect, CloudTrail, Config, etc.
```

These examples illustrate how to design and implement AWS architectures for different industries and use cases, ensuring high availability, security, and scalability. Each architecture is tailored to the specific needs of the business, leveraging AWS services effectively.


Sure! Here are visual text diagrams along with detailed step-by-step explanations for each of the real-world examples provided:

### 1. E-Commerce Company Hosting an Online Store

#### Visual Text Diagram:
```
                             +-------------------------+
                             |       Route 53          |
                             +-------------------------+
                                       |
                                       |
                             +-------------------------+
                             |       CloudFront        |
                             +-------------------------+
                                       |
                                       |
                             +-------------------------+
                             |       ELB               |
                             +-------------------------+
                              /              \
                             /                \
                   +----------------+    +----------------+
                   |  Public Subnet |    |  Public Subnet |
                   |  (us-east-1a)  |    |  (us-east-1b)  |
                   +----------------+    +----------------+
                          |                     |
                          |                     |
+----------------+        |                     |        +----------------+
|  NAT Gateway   |        |                     |        |  NAT Gateway   |
+----------------+        |                     |        +----------------+
        |                 |                     |                 |
+----------------+  +------------+        +------------+  +----------------+
| Bastion Host   |  | Web Server |        | Web Server |  | Bastion Host   |
+----------------+  +------------+        +------------+  +----------------+
        |                 |                     |                 |
+----------------+  +----------------+  +----------------+  +----------------+
|  Private Subnet|  |  Private Subnet |  |  Private Subnet |  |  Private Subnet |
|  (us-east-1a)  |  |  (us-east-1a)  |  |  (us-east-1b)  |  |  (us-east-1b)  |
+----------------+  +----------------+  +----------------+  +----------------+
                          |                     |                     |
                          |                     |                     |
                   +----------------+    +----------------+    +----------------+
                   |     RDS        |    |     RDS        |    |     RDS        |
                   | Multi-AZ (DB1) |    | Multi-AZ (DB1) |    | Multi-AZ (DB1) |
                   +----------------+    +----------------+    +----------------+
                          |                     |                     |
                   +----------------+    +----------------+    +----------------+
                   |      S3        |    |      S3        |    |      S3        |
                   +----------------+    +----------------+    +----------------+
```

#### Step-by-Step Explanation:
1. **Route 53**: DNS service to route user requests to CloudFront.
2. **CloudFront**: CDN to cache content and deliver it quickly to users globally.
3. **ELB (Elastic Load Balancer)**: Distributes incoming traffic to multiple web servers in different availability zones for redundancy and high availability.
4. **Public Subnets**: Host NAT Gateways, Bastion Hosts, and Load Balancers.
   - **NAT Gateway**: Allows instances in private subnets to access the internet for updates and patches.
   - **Bastion Host**: Provides secure administrative access to the instances in private subnets.
   - **Web Servers**: Host the application, deployed in auto-scaling groups.
5. **Private Subnets**: Host EC2 instances for the application and databases.
   - **Application Servers**: EC2 instances running the application.
   - **RDS (Relational Database Service)**: Multi-AZ deployment for high availability of the database.
6. **S3**: Storage for static content, backups, and logs.

### 2. Media Streaming Service

#### Visual Text Diagram:
```
                             +-------------------------+
                             |       Route 53          |
                             +-------------------------+
                                       |
                                       |
                             +-------------------------+
                             |       CloudFront        |
                             +-------------------------+
                                       |
                                       |
                             +-------------------------+
                             |       ELB               |
                             +-------------------------+
                              /              \
                             /                \
                   +----------------+    +----------------+
                   |  Public Subnet |    |  Public Subnet |
                   |  (us-west-2a)  |    |  (us-west-2b)  |
                   +----------------+    +----------------+
                          |                     |
                          |                     |
+----------------+        |                     |        +----------------+
|  NAT Gateway   |        |                     |        |  NAT Gateway   |
+----------------+        |                     |        +----------------+
        |                 |                     |                 |
+----------------+  +------------+        +------------+  +----------------+
| Media Server   |  | Media Server |        | Media Server |  | Media Server   |
+----------------+  +------------+        +------------+  +----------------+
        |                 |                     |                 |
+----------------+  +----------------+  +----------------+  +----------------+
|  Private Subnet|  |  Private Subnet |  |  Private Subnet |  |  Private Subnet |
|  (us-west-2a)  |  |  (us-west-2a)  |  |  (us-west-2b)  |  |  (us-west-2b)  |
+----------------+  +----------------+  +----------------+  +----------------+
                          |                     |                     |
                          |                     |                     |
                   +----------------+    +----------------+    +----------------+
                   |      S3        |    |      S3        |    |      S3        |
                   +----------------+    +----------------+    +----------------+
                          |                     |                     |
                   +----------------+    +----------------+    +----------------+
                   |  DynamoDB      |    |  DynamoDB      |    |  DynamoDB      |
                   +----------------+    +----------------+    +----------------+
                          |                     |                     |
                   +----------------+    +----------------+    +----------------+
                   | ElasticTranscoder|    | ElasticTranscoder|    | ElasticTranscoder|
                   +----------------+    +----------------+    +----------------+
```

#### Step-by-Step Explanation:
1. **Route 53**: DNS service to route user requests to CloudFront.
2. **CloudFront**: CDN to cache content and deliver it quickly to users globally.
3. **ELB (Elastic Load Balancer)**: Distributes incoming traffic to multiple media servers in different availability zones for redundancy and high availability.
4. **Public Subnets**: Host NAT Gateways, Media Servers, and Load Balancers.
   - **NAT Gateway**: Allows instances in private subnets to access the internet for updates and patches.
   - **Media Servers**: EC2 instances running the media streaming application, deployed in auto-scaling groups.
5. **Private Subnets**: Host EC2 instances for media servers and databases.
   - **S3**: Storage for media files.
   - **DynamoDB**: NoSQL database for storing metadata about media files.
   - **Elastic Transcoder**: To transcode media files into different formats for various devices.

### 3. Financial Services Company

#### Visual Text Diagram:
```
                             +-------------------------+
                             |       Route 53          |
                             +-------------------------+
                                       |
                                       |
                             +-------------------------+
                             |       Direct Connect    |
                             +-------------------------+
                                       |
                                       |
                             +-------------------------+
                             |       VPC               |
                             +-------------------------+
                              /              \
                             /                \
                   +----------------+    +----------------+
                   |  Public Subnet |    |  Public Subnet |
                   |  (us-east-1a)  |    |  (us-east-1b)  |
                   +----------------+    +----------------+
                          |                     |
                          |                     |
+----------------+        |                     |        +----------------+
|  NAT Gateway   |        |                     |        |  NAT Gateway   |
+----------------+        |                     |        +----------------+
        |                 |                     |                 |
+----------------+  +------------+        +------------+  +----------------+
| Bastion Host   |  | Web Server |        | Web Server |  | Bastion Host   |
+----------------+  +------------+        +------------+  +----------------+
        |                 |                     |                 |
+----------------+  +----------------+  +----------------+  +----------------+
|  Private Subnet|  |  Private Subnet |  |  Private Subnet |  |  Private Subnet |
|  (us-east-1a)  |  |  (us-east-1a)  |  |  (us-east-1b)  |  |  (us-east-1b)  |
+----------------+  +----------------+  +----------------+  +----------------+
                          |                     |                     |
                          |                     |                     |
                   +----------------+    +----------------+    +----------------+
                   |     RDS        |    |     RDS        |    |     RDS        |
                   | Multi-AZ (DB1) |    | Multi-AZ (DB1) |    | Multi-AZ (DB1) |
                   +----------------+    +----------------+    +----------------+
                          |                     |                     |
                   +----------------+    +----------------+    +----------------+
                   |      S3        |    |      S3        |    |      S3        |
                   +----------------+    +----------------+    +----------------+
                          |                     |                     |
                   +----------------+    +----------------+    +----------------+
                   |      KMS       |    |      KMS       |    |      KMS       |
                   +----------------+    +----------------+    +----------------+
                          |                     |                     |
                   +----------------+    +----------------+    +----------------+
                   |    CloudHSM    |   

 |    CloudHSM    |    |    CloudHSM    |
                   +----------------+    +----------------+    +----------------+
                          |                     |                     |
                   +----------------+    +----------------+    +----------------+
                   |   CloudTrail   |    |   CloudTrail   |    |   CloudTrail   |
                   +----------------+    +----------------+    +----------------+
                          |                     |                     |
                   +----------------+    +----------------+    +----------------+
                   |     Config     |    |     Config     |    |     Config     |
                   +----------------+    +----------------+    +----------------+
                          |                     |                     |
                   +----------------+    +----------------+    +----------------+
                   |      WAF       |    |      WAF       |    |      WAF       |
                   +----------------+    +----------------+    +----------------+
```

#### Step-by-Step Explanation:
1. **Route 53**: DNS service to route user requests to the application.
2. **Direct Connect**: Provides a dedicated connection to the on-premises data center, ensuring secure and high-speed connectivity.
3. **VPC**: Configured with public and private subnets across multiple availability zones for redundancy and high availability.
4. **Public Subnets**: Host NAT Gateways, Bastion Hosts, and Load Balancers.
   - **NAT Gateway**: Allows instances in private subnets to access the internet for updates and patches.
   - **Bastion Host**: Provides secure administrative access to the instances in private subnets.
   - **Web Servers**: Host the application, deployed in auto-scaling groups.
5. **Private Subnets**: Host EC2 instances for the application and databases.
   - **RDS (Relational Database Service)**: Multi-AZ deployment for high availability of the database.
   - **S3**: Storage for static content, backups, and logs.
   - **KMS**: Manages encryption keys for data at rest.
   - **CloudHSM**: Hardware security module for cryptographic operations.
6. **CloudTrail**: For logging and monitoring API calls to ensure compliance and security.
7. **Config**: Monitors configuration changes and ensures compliance with policies.
8. **WAF (Web Application Firewall)**: Provides additional security for the web application.

These diagrams and explanations provide a detailed overview of each architecture and how different AWS services are used to meet specific requirements for each industry and use case.


Sure! Below are detailed step-by-step Terraform scripts with comments for each of the real-world examples:

### 1. E-Commerce Company Hosting an Online Store

#### Terraform Script:
```hcl
# Provider configuration
provider "aws" {
  region = "us-east-1"
}

# Create a VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# Create Public Subnets
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
  map_public_ip_on_launch = true
}

# Create Private Subnets
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 2}.0/24"
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
}

# Create an Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

# Create NAT Gateways
resource "aws_nat_gateway" "nat" {
  count         = 2
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = element(aws_subnet.public.*.id, count.index)
}

# Create Elastic IPs for NAT Gateways
resource "aws_eip" "nat" {
  count = 2
  vpc = true
}

# Create a Route Table for Public Subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

# Associate Public Subnets with Route Table
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = element(aws_subnet.public.*.id, count.index)
  route_table_id = aws_route_table.public.id
}

# Create Route Tables for Private Subnets
resource "aws_route_table" "private" {
  count = 2
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = element(aws_nat_gateway.nat.*.id, count.index)
  }
}

# Associate Private Subnets with Route Tables
resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = element(aws_subnet.private.*.id, count.index)
  route_table_id = element(aws_route_table.private.*.id, count.index)
}

# Create Security Group for Web Servers
resource "aws_security_group" "web" {
  vpc_id = aws_vpc.main.id

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

# Create Security Group for RDS
resource "aws_security_group" "db" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port      = 3306
    to_port        = 3306
    protocol       = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an Auto Scaling Group for Web Servers
resource "aws_autoscaling_group" "web" {
  desired_capacity     = 2
  max_size             = 4
  min_size             = 2
  vpc_zone_identifier  = aws_subnet.private.*.id
  launch_configuration = aws_launch_configuration.web.id
}

# Create a Launch Configuration for Web Servers
resource "aws_launch_configuration" "web" {
  image_id        = "ami-0c55b159cbfafe1f0" # Use an appropriate AMI
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.web.id]

  lifecycle {
    create_before_destroy = true
  }
}

# Create RDS Instance
resource "aws_db_instance" "db" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "mydb"
  username             = "admin"
  password             = "password"
  vpc_security_group_ids = [aws_security_group.db.id]
  multi_az             = true
  publicly_accessible  = false
}

# Create an S3 Bucket for Static Content
resource "aws_s3_bucket" "static" {
  bucket = "ecommerce-static-content"
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}

# Create CloudFront Distribution for S3 Bucket
resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.static.id}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.origin_access_identity.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.static.id}"

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

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# Create Route 53 Record to point to CloudFront Distribution
resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.cdn.domain_name
    zone_id                = aws_cloudfront_distribution.cdn.hosted_zone_id
    evaluate_target_health = false
  }
}
```

### 2. Media Streaming Service

#### Terraform Script:
```hcl
# Provider configuration
provider "aws" {
  region = "us-west-2"
}

# Create a VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# Create Public Subnets
resource "aws_subnet" "public" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = element(["us-west-2a", "us-west-2b", "us-west-2c"], count.index)
  map_public_ip_on_launch = true
}

# Create Private Subnets
resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 3}.0/24"
  availability_zone = element(["us-west-2a", "us-west-2b", "us-west-2c"], count.index)
}

# Create an Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

# Create NAT Gateways
resource "aws_nat_gateway" "nat" {
  count         = 3
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = element(aws_subnet.public.*.id, count.index)
}

# Create Elastic IPs for NAT Gateways
resource "aws_eip" "nat" {
  count = 3
  vpc = true
}

# Create a Route Table for Public Subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

# Associate Public Subnets with Route Table
resource "aws_route_table_association" "public" {
  count          = 3
  subnet_id      = element(aws

_subnet.public.*.id, count.index)
  route_table_id = aws_route_table.public.id
}

# Create Route Tables for Private Subnets
resource "aws_route_table" "private" {
  count = 3
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = element(aws_nat_gateway.nat.*.id, count.index)
  }
}

# Associate Private Subnets with Route Tables
resource "aws_route_table_association" "private" {
  count          = 3
  subnet_id      = element(aws_subnet.private.*.id, count.index)
  route_table_id = element(aws_route_table.private.*.id, count.index)
}

# Create Security Group for Media Servers
resource "aws_security_group" "media" {
  vpc_id = aws_vpc.main.id

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

# Create an Auto Scaling Group for Media Servers
resource "aws_autoscaling_group" "media" {
  desired_capacity     = 3
  max_size             = 6
  min_size             = 3
  vpc_zone_identifier  = aws_subnet.private.*.id
  launch_configuration = aws_launch_configuration.media.id
}

# Create a Launch Configuration for Media Servers
resource "aws_launch_configuration" "media" {
  image_id        = "ami-0c55b159cbfafe1f0" # Use an appropriate AMI
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.media.id]

  lifecycle {
    create_before_destroy = true
  }
}

# Create an S3 Bucket for Media Files
resource "aws_s3_bucket" "media" {
  bucket = "media-streaming-service"
  acl    = "private"
}

# Create DynamoDB Table for Media Metadata
resource "aws_dynamodb_table" "media_metadata" {
  name         = "media_metadata"
  hash_key     = "media_id"

  attribute {
    name = "media_id"
    type = "S"
  }

  billing_mode = "PAY_PER_REQUEST"
}

# Create Elastic Transcoder Pipeline
resource "aws_elastictranscoder_pipeline" "media_pipeline" {
  name = "media-transcoding-pipeline"
  input_bucket = aws_s3_bucket.media.bucket
  output_bucket = aws_s3_bucket.media.bucket

  role = aws_iam_role.transcoder_role.arn

  notifications {
    progressing = "arn:aws:sns:us-west-2:123456789012:transcoder-notifications"
    completed   = "arn:aws:sns:us-west-2:123456789012:transcoder-notifications"
    warning     = "arn:aws:sns:us-west-2:123456789012:transcoder-notifications"
    error       = "arn:aws:sns:us-west-2:123456789012:transcoder-notifications"
  }
}

# Create CloudFront Distribution for S3 Bucket
resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = aws_s3_bucket.media.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.media.id}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.origin_access_identity.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.media.id}"

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

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# Create Route 53 Record to point to CloudFront Distribution
resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.cdn.domain_name
    zone_id                = aws_cloudfront_distribution.cdn.hosted_zone_id
    evaluate_target_health = false
  }
}

# Create IAM Role for Elastic Transcoder
resource "aws_iam_role" "transcoder_role" {
  name = "elastic-transcoder-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "elastictranscoder.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Attach Policy to IAM Role
resource "aws_iam_role_policy" "transcoder_policy" {
  name = "elastic-transcoder-policy"
  role = aws_iam_role.transcoder_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": "arn:aws:s3:::${aws_s3_bucket.media.bucket}"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": "arn:aws:s3:::${aws_s3_bucket.media.bucket}/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "arn:aws:sns:us-west-2:123456789012:transcoder-notifications"
    },
    {
      "Effect": "Allow",
      "Action": [
        "elastictranscoder:*"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}
```

### 3. Financial Services Company

#### Terraform Script:
```hcl
# Provider configuration
provider "aws" {
  region = "us-east-1"
}

# Create a VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# Create Public Subnets
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
  map_public_ip_on_launch = true
}

# Create Private Subnets
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 2}.0/24"
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
}

# Create an Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

# Create NAT Gateways
resource "aws_nat_gateway" "nat" {
  count         = 2
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = element(aws_subnet.public.*.id, count.index)
}

# Create Elastic IPs for NAT Gateways
resource "aws_eip" "nat" {
  count = 2
  vpc = true
}

# Create a Route Table for Public Subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

# Associate Public Subnets with Route Table
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = element(aws_subnet.public.*.id, count.index)
  route_table_id = aws_route_table.public.id
}

# Create Route Tables for Private Subnets
resource "aws_route_table" "private" {
  count = 2
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = element(aws_nat_gateway.nat.*.id, count.index)
  }
}

# Associate Private Subnets with Route Tables
resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = element(aws_subnet

.private.*.id, count.index)
  route_table_id = element(aws_route_table.private.*.id, count.index)
}

# Create Security Group for Web Servers
resource "aws_security_group" "web" {
  vpc_id = aws_vpc.main.id

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

# Create Security Group for RDS
resource "aws_security_group" "db" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port      = 3306
    to_port        = 3306
    protocol       = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an Auto Scaling Group for Web Servers
resource "aws_autoscaling_group" "web" {
  desired_capacity     = 2
  max_size             = 4
  min_size             = 2
  vpc_zone_identifier  = aws_subnet.private.*.id
  launch_configuration = aws_launch_configuration.web.id
}

# Create a Launch Configuration for Web Servers
resource "aws_launch_configuration" "web" {
  image_id        = "ami-0c55b159cbfafe1f0" # Use an appropriate AMI
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.web.id]

  lifecycle {
    create_before_destroy = true
  }
}

# Create RDS Instance
resource "aws_db_instance" "db" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "mydb"
  username             = "admin"
  password             = "password"
  vpc_security_group_ids = [aws_security_group.db.id]
  multi_az             = true
  publicly_accessible  = false
  storage_encrypted    = true
  kms_key_id           = aws_kms_key.mykey.arn
}

# Create an S3 Bucket for Backups and Logs
resource "aws_s3_bucket" "logs" {
  bucket = "financial-services-logs"
  acl    = "private"
}

# Create KMS Key for Encryption
resource "aws_kms_key" "mykey" {
  description = "KMS key for RDS encryption"
}

# Create CloudTrail for Logging API Calls
resource "aws_cloudtrail" "main" {
  name                          = "financial-services-cloudtrail"
  s3_bucket_name                = aws_s3_bucket.logs.bucket
  include_global_service_events = true
  is_multi_region_trail         = true
}

# Create Config for Monitoring Configuration Changes
resource "aws_config_configuration_recorder" "main" {
  name     = "config-recorder"
  role_arn = aws_iam_role.config_role.arn
}

resource "aws_config_delivery_channel" "main" {
  name           = "config-delivery-channel"
  s3_bucket_name = aws_s3_bucket.logs.bucket
}

# Create IAM Role for Config
resource "aws_iam_role" "config_role" {
  name = "config-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "config.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Attach Policy to IAM Role
resource "aws_iam_role_policy" "config_policy" {
  name = "config-policy"
  role = aws_iam_role.config_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.logs.bucket}",
        "arn:aws:s3:::${aws_s3_bucket.logs.bucket}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "config:*"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

# Create WAF for Web Application Firewall
resource "aws_waf_web_acl" "main" {
  name        = "financial-services-waf"
  metric_name = "financialServicesWAF"

  default_action {
    type = "ALLOW"
  }

  rule {
    action {
      type = "BLOCK"
    }

    priority = 1
    rule_id  = aws_waf_rule.sql_injection_rule.id
  }
}

# Create WAF Rule for SQL Injection
resource "aws_waf_rule" "sql_injection_rule" {
  name        = "SQLInjectionRule"
  metric_name = "SQLInjectionRule"

  predicates {
    data_id = aws_waf_sql_injection_match_set.sql_injection_match_set.id
    negated = false
    type    = "SqlInjectionMatch"
  }
}

# Create SQL Injection Match Set for WAF
resource "aws_waf_sql_injection_match_set" "sql_injection_match_set" {
  name = "sqlInjectionMatchSet"

  sql_injection_match_tuples {
    field_to_match {
      type = "QUERY_STRING"
    }

    text_transformation = "URL_DECODE"
  }
}
```

These Terraform scripts provide a comprehensive step-by-step setup for each real-world example, including all necessary resources and configurations. Each section is commented to explain the purpose and function of the resources being created.


Sure! Here is a detailed step-by-step guide for different architectural patterns covering various AWS services.

### Architectural Pattern 1: Multi-Tier Architecture

#### Description:
Multi-tier architecture divides the application into layers: presentation (web), application logic, and data storage. This pattern provides separation of concerns, improved security, and scalability.

#### Steps:
1. **VPC Setup**:
   - Create a VPC with public and private subnets.

2. **Internet Gateway and NAT Gateway**:
   - Attach an Internet Gateway to the VPC.
   - Create NAT Gateways in the public subnets.

3. **Route Tables**:
   - Create route tables for public and private subnets, associating them with appropriate gateways.

4. **Security Groups**:
   - Create security groups for web servers, application servers, and databases with appropriate rules.

5. **Load Balancer**:
   - Set up an Elastic Load Balancer (ELB) to distribute traffic across multiple web servers.

6. **EC2 Instances**:
   - Deploy EC2 instances in the public subnets for web servers.
   - Deploy EC2 instances in the private subnets for application servers.

7. **RDS**:
   - Set up an RDS instance in the private subnet for the database.

8. **Auto Scaling**:
   - Configure Auto Scaling groups for web and application servers to handle varying loads.

#### Example:
```hcl
provider "aws" {
  region = "us-east-1"
}

# Create VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# Create Public Subnets
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
  map_public_ip_on_launch = true
}

# Create Private Subnets
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 2}.0/24"
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
}

# Create Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

# Create NAT Gateway
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = element(aws_subnet.public.*.id, 0)
}

# Create Elastic IP for NAT Gateway
resource "aws_eip" "nat" {
  vpc = true
}

# Create Route Table for Public Subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

# Associate Public Subnets with Route Table
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = element(aws_subnet.public.*.id, count.index)
  route_table_id = aws_route_table.public.id
}

# Create Route Table for Private Subnets
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }
}

# Associate Private Subnets with Route Table
resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = element(aws_subnet.private.*.id, count.index)
  route_table_id = aws_route_table.private.id
}

# Create Security Groups
resource "aws_security_group" "web" {
  vpc_id = aws_vpc.main.id

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

resource "aws_security_group" "app" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 8080
    to_port     = 8080
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

resource "aws_security_group" "db" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port      = 3306
    to_port        = 3306
    protocol       = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create Load Balancer
resource "aws_elb" "web" {
  name               = "web-elb"
  availability_zones = ["us-east-1a", "us-east-1b"]

  listener {
    instance_port     = 80
    instance_protocol = "HTTP"
    lb_port           = 80
    lb_protocol       = "HTTP"
  }

  health_check {
    target              = "HTTP:80/"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }

  instances             = aws_instance.web.*.id
  security_groups       = [aws_security_group.web.id]
}

# Create EC2 Instances for Web Servers
resource "aws_instance" "web" {
  count         = 2
  ami           = "ami-0c55b159cbfafe1f0" # Use an appropriate AMI
  instance_type = "t2.micro"
  subnet_id     = element(aws_subnet.public.*.id, count.index)
  security_groups = [aws_security_group.web.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              echo "Hello, World" > /var/www/html/index.html
              EOF
}

# Create EC2 Instances for Application Servers
resource "aws_instance" "app" {
  count         = 2
  ami           = "ami-0c55b159cbfafe1f0" # Use an appropriate AMI
  instance_type = "t2.micro"
  subnet_id     = element(aws_subnet.private.*.id, count.index)
  security_groups = [aws_security_group.app.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y java
              # Additional application setup commands
              EOF
}

# Create RDS Instance
resource "aws_db_instance" "db" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "mydb"
  username             = "admin"
  password             = "password"
  vpc_security_group_ids = [aws_security_group.db.id]
  multi_az             = true
  publicly_accessible  = false
  storage_encrypted    = true
}

# Create Auto Scaling Group for Web Servers
resource "aws_autoscaling_group" "web_asg" {
  desired_capacity     = 2
  max_size             = 4
  min_size             = 2
  vpc_zone_identifier  = aws_subnet.public.*.id
  launch_configuration = aws_launch_configuration.web_lc.id
}

# Create Launch Configuration for Web Servers
resource "aws_launch_configuration" "web_lc" {
  image_id        = "ami-0c55b159cbfafe1f0" # Use an appropriate AMI
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.web.id]

  lifecycle {
    create_before_destroy = true
  }
}

# Create Auto Scaling Group for Application Servers
resource "aws_autoscaling_group" "app_asg" {
  desired_capacity     = 2
  max_size             = 4
  min_size             = 2
  vpc_zone_identifier  = aws_subnet.private.*.id
  launch_configuration = aws_launch_configuration.app_lc.id
}

# Create Launch Configuration for Application Servers
resource "aws_launch_configuration" "app_lc" {
  image_id        = "ami-0c55b159cbfafe1f0" # Use an appropriate AMI
  instance

_type   = "t2.micro"
  security_groups = [aws_security_group.app.id]

  lifecycle {
    create_before_destroy = true
  }
}
```

### Architectural Pattern 2: Serverless Architecture

#### Description:
Serverless architecture leverages AWS Lambda functions, API Gateway, and other managed services to build scalable applications without managing servers.

#### Steps:
1. **API Gateway**:
   - Create an API Gateway to expose HTTP endpoints.

2. **Lambda Functions**:
   - Create Lambda functions to handle business logic.

3. **DynamoDB**:
   - Use DynamoDB for a scalable NoSQL database.

4. **S3**:
   - Use S3 for static content storage and hosting.

5. **IAM Roles**:
   - Create IAM roles and policies for Lambda functions.

6. **CloudFront**:
   - Use CloudFront to deliver content with low latency.

#### Example:
```hcl
provider "aws" {
  region = "us-east-1"
}

# Create IAM Role for Lambda Function
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Attach Policy to IAM Role
resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Create Lambda Function
resource "aws_lambda_function" "my_function" {
  function_name = "my_lambda_function"
  handler       = "index.handler"
  runtime       = "nodejs12.x"
  role          = aws_iam_role.lambda_exec_role.arn

  filename = "lambda_function_payload.zip" # Zip file containing Lambda function code
  source_code_hash = filebase64sha256("lambda_function_payload.zip")

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.my_table.name
    }
  }
}

# Create API Gateway
resource "aws_api_gateway_rest_api" "my_api" {
  name        = "my_api"
  description = "API Gateway for my application"
}

# Create API Gateway Resource
resource "aws_api_gateway_resource" "resource" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  parent_id   = aws_api_gateway_rest_api.my_api.root_resource_id
  path_part   = "myresource"
}

# Create API Gateway Method
resource "aws_api_gateway_method" "method" {
  rest_api_id   = aws_api_gateway_rest_api.my_api.id
  resource_id   = aws_api_gateway_resource.resource.id
  http_method   = "POST"
  authorization = "NONE"
}

# Create API Gateway Integration
resource "aws_api_gateway_integration" "integration" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  resource_id = aws_api_gateway_resource.resource.id
  http_method = aws_api_gateway_method.method.http_method
  type        = "AWS_PROXY"
  integration_http_method = "POST"
  uri         = aws_lambda_function.my_function.invoke_arn
}

# Create DynamoDB Table
resource "aws_dynamodb_table" "my_table" {
  name         = "my_table"
  hash_key     = "id"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "id"
    type = "S"
  }
}

# Create S3 Bucket for Static Content
resource "aws_s3_bucket" "static" {
  bucket = "my-static-content"
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}

# Create CloudFront Distribution for S3 Bucket
resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.static.id}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.origin_access_identity.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.static.id}"

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

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# Create Route 53 Record to point to CloudFront Distribution
resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.cdn.domain_name
    zone_id                = aws_cloudfront_distribution.cdn.hosted_zone_id
    evaluate_target_health = false
  }
}
```

### Architectural Pattern 3: Microservices Architecture

#### Description:
Microservices architecture decomposes an application into loosely coupled services that are deployed and scaled independently.

#### Steps:
1. **ECS or EKS**:
   - Use ECS (Elastic Container Service) or EKS (Elastic Kubernetes Service) for container orchestration.

2. **Fargate**:
   - Use AWS Fargate for serverless container management.

3. **API Gateway**:
   - Create an API Gateway to route requests to different microservices.

4. **Service Discovery**:
   - Use AWS Cloud Map for service discovery.

5. **CI/CD**:
   - Use AWS CodePipeline, CodeBuild, and CodeDeploy for continuous integration and deployment.

6. **Monitoring**:
   - Use CloudWatch and X-Ray for monitoring and tracing.

#### Example:
```hcl
provider "aws" {
  region = "us-west-2"
}

# Create ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "my-cluster"
}

# Create VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# Create Public Subnets
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = element(["us-west-2a", "us-west-2b"], count.index)
  map_public_ip_on_launch = true
}

# Create Private Subnets
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 2}.0/24"
  availability_zone = element(["us-west-2a", "us-west-2b"], count.index)
}

# Create Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

# Create NAT Gateway
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = element(aws_subnet.public.*.id, 0)
}

# Create Elastic IP for NAT Gateway
resource "aws_eip" "nat" {
  vpc = true
}

# Create Route Table for Public Subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

# Associate Public Subnets with Route Table
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = element(aws_subnet.public.*.id, count.index)
  route_table_id = aws_route_table.public.id
}

# Create Route Table for Private Subnets
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }
}

# Associate Private Subnets with Route Table
resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = element(aws_subnet.private.*.id, count.index)
  route_table_id = aws_route_table.private.id
}

# Create Security Group for ECS
resource "aws_security_group" "ecs" {
  vpc_id = aws_vpc.main.id

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
    cidr_blocks = ["0.0.0.

0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create ECS Task Definition
resource "aws_ecs_task_definition" "app" {
  family                   = "my-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  container_definitions = <<EOF
[
  {
    "name": "my-app",
    "image": "nginx",
    "essential": true,
    "portMappings": [
      {
        "containerPort": 80,
        "hostPort": 80
      }
    ]
  }
]
EOF

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_execution_role.arn
}

# Create IAM Role for ECS Task Execution
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs_task_execution_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Attach Policy to IAM Role
resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Create ECS Service
resource "aws_ecs_service" "app" {
  name            = "my-app"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 2
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = aws_subnet.private.*.id
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true
  }
}

# Create API Gateway
resource "aws_api_gateway_rest_api" "my_api" {
  name        = "my_api"
  description = "API Gateway for my application"
}

# Create API Gateway Resource
resource "aws_api_gateway_resource" "resource" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  parent_id   = aws_api_gateway_rest_api.my_api.root_resource_id
  path_part   = "myresource"
}

# Create API Gateway Method
resource "aws_api_gateway_method" "method" {
  rest_api_id   = aws_api_gateway_rest_api.my_api.id
  resource_id   = aws_api_gateway_resource.resource.id
  http_method   = "GET"
  authorization = "NONE"
}

# Create API Gateway Integration
resource "aws_api_gateway_integration" "integration" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  resource_id = aws_api_gateway_resource.resource.id
  http_method = aws_api_gateway_method.method.http_method
  type        = "HTTP_PROXY"
  integration_http_method = "GET"
  uri         = "http://${aws_ecs_service.app.load_balancers[0].dns_name}"
}

# Create CloudWatch Log Group
resource "aws_cloudwatch_log_group" "my_app" {
  name              = "/ecs/my-app"
  retention_in_days = 30
}

# Create X-Ray Group
resource "aws_xray_group" "my_app" {
  filter_expression = "service(\"my-app\")"
  group_name        = "my_app"
}

# Create CloudMap Namespace
resource "aws_service_discovery_private_dns_namespace" "my_app" {
  name        = "myapp.local"
  vpc         = aws_vpc.main.id
  description = "Private DNS namespace for my app"
}

# Create CloudMap Service
resource "aws_service_discovery_service" "my_app" {
  name        = "my-app"
  namespace_id = aws_service_discovery_private_dns_namespace.my_app.id

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.my_app.id
    dns_records {
      type = "A"
      ttl  = 10
    }
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}
```

### Architectural Pattern 4: Data Lake Architecture

#### Description:
A data lake architecture uses Amazon S3 to store vast amounts of raw data in various formats, and services like AWS Glue, Athena, and Redshift Spectrum to process and analyze this data.

#### Steps:
1. **S3 Buckets**:
   - Create S3 buckets to store raw, processed, and curated data.

2. **AWS Glue**:
   - Use AWS Glue for ETL (extract, transform, load) jobs.

3. **Athena**:
   - Use Athena to query the data stored in S3.

4. **Redshift Spectrum**:
   - Use Redshift Spectrum to run SQL queries on the data in S3.

5. **IAM Roles**:
   - Create IAM roles and policies for Glue, Athena, and Redshift.

6. **Kinesis**:
   - Use Kinesis for real-time data streaming into the data lake.

#### Example:
```hcl
provider "aws" {
  region = "us-east-1"
}

# Create S3 Buckets
resource "aws_s3_bucket" "raw_data" {
  bucket = "my-data-lake-raw"
  acl    = "private"
}

resource "aws_s3_bucket" "processed_data" {
  bucket = "my-data-lake-processed"
  acl    = "private"
}

resource "aws_s3_bucket" "curated_data" {
  bucket = "my-data-lake-curated"
  acl    = "private"
}

# Create IAM Role for AWS Glue
resource "aws_iam_role" "glue_role" {
  name = "AWSGlueServiceRole"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "glue.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Attach Policy to IAM Role
resource "aws_iam_role_policy_attachment" "glue_policy" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# Create AWS Glue Database
resource "aws_glue_catalog_database" "my_database" {
  name = "my_database"
}

# Create AWS Glue Crawler
resource "aws_glue_crawler" "my_crawler" {
  name         = "my_crawler"
  role         = aws_iam_role.glue_role.arn
  database_name = aws_glue_catalog_database.my_database.name
  s3_target {
    path = aws_s3_bucket.raw_data.bucket
  }
}

# Create AWS Glue Job
resource "aws_glue_job" "my_job" {
  name     = "my_job"
  role_arn = aws_iam_role.glue_role.arn

  command {
    name            = "glueetl"
    script_location = "s3://${aws_s3_bucket.processed_data.bucket}/scripts/my_script.py"
  }

  default_arguments = {
    "--job-language" = "python"
    "--TempDir"      = "s3://${aws_s3_bucket.processed_data.bucket}/temp/"
  }

  max_retries       = 1
  timeout           = 10
  glue_version      = "2.0"
  number_of_workers = 10
  worker_type       = "G.1X"
}

# Create IAM Role for Athena
resource "aws_iam_role" "athena_role" {
  name = "AWSAthenaServiceRole"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "athena.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Attach Policy to IAM Role
resource "aws_iam_role_policy_attachment" "athena_policy" {
  role       = aws_iam_role.athena_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAthenaFullAccess"
}

# Create Athena Workgroup
resource "aws_athena_workgroup" "my_workgroup" {
  name        = "my_workgroup"
  state       = "ENABLED"
  description = "My Athena Workgroup"

  configuration {
    enforce_workgroup_configuration = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.processed_data.bucket}/results/"
    }
  }
}

# Create IAM Role for Redshift Spectrum
resource "aws_iam_role" "redshift_spectrum_role" {
  name = "AWSRedshiftSpectrumRole"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "redshift.amazonaws.com"
      },
      "Action": "sts

:AssumeRole"
    }
  ]
}
EOF
}

# Attach Policy to IAM Role
resource "aws_iam_role_policy_attachment" "redshift_spectrum_policy" {
  role       = aws_iam_role.redshift_spectrum_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRedshiftSpectrumPreviewFullAccess"
}

# Create Kinesis Stream
resource "aws_kinesis_stream" "my_stream" {
  name             = "my_stream"
  shard_count      = 1
  retention_period = 24
}

# Create Kinesis Firehose Delivery Stream
resource "aws_kinesis_firehose_delivery_stream" "my_firehose" {
  name        = "my_firehose"
  destination = "s3"

  s3_configuration {
    role_arn         = aws_iam_role.firehose_role.arn
    bucket_arn       = aws_s3_bucket.raw_data.arn
    buffer_size      = 5
    buffer_interval  = 300
    compression_format = "UNCOMPRESSED"
  }
}

# Create IAM Role for Kinesis Firehose
resource "aws_iam_role" "firehose_role" {
  name = "AWSKinesisFirehoseRole"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "firehose.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Attach Policy to IAM Role
resource "aws_iam_role_policy_attachment" "firehose_policy" {
  role       = aws_iam_role.firehose_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonKinesisFirehoseFullAccess"
}
```

These architectural patterns and Terraform scripts cover a wide range of AWS services, demonstrating different approaches to building scalable, secure, and efficient applications on AWS. Each script includes detailed steps and comments to guide you through the implementation process.


Sure! Here are visual text diagrams with step-by-step details for each of the architectural patterns:

### Architectural Pattern 1: Multi-Tier Architecture

#### Visual Text Diagram:
```
                            +------------------------+
                            |       Route 53         |
                            +------------------------+
                                      |
                                      |
                            +------------------------+
                            |       ELB              |
                            +------------------------+
                             /             \
                            /               \
                 +----------------+   +----------------+
                 |  Public Subnet |   |  Public Subnet |
                 |  (us-east-1a)  |   |  (us-east-1b)  |
                 +----------------+   +----------------+
                        |                    |
                        |                    |
          +------------------+   +------------------+
          | Web Server (EC2) |   | Web Server (EC2) |
          +------------------+   +------------------+
                        |                    |
                        |                    |
                 +----------------+   +----------------+
                 |  Private Subnet|   |  Private Subnet|
                 |  (us-east-1a)  |   |  (us-east-1b)  |
                 +----------------+   +----------------+
                        |                    |
                        |                    |
         +----------------------+  +----------------------+
         | App Server (EC2)     |  | App Server (EC2)     |
         +----------------------+  +----------------------+
                        |                    |
                        |                    |
          +------------------+   +------------------+
          | RDS (Multi-AZ)   |   | RDS (Multi-AZ)   |
          +------------------+   +------------------+
                        |                    |
                        |                    |
           +-------------------+  +-------------------+
           | S3 (Static Content)|  | S3 (Backups/Logs)|
           +-------------------+  +-------------------+
```

#### Step-by-Step Details:
1. **Route 53**: DNS service to route traffic to the ELB.
2. **ELB (Elastic Load Balancer)**: Distributes incoming traffic to the web servers in different availability zones.
3. **Public Subnets**: Host the web servers.
   - **Web Server (EC2)**: Handles the presentation layer of the application.
4. **Private Subnets**: Host the application servers and RDS instances.
   - **App Server (EC2)**: Handles the application logic layer.
   - **RDS (Multi-AZ)**: Provides a highly available and fault-tolerant database solution.
5. **S3 Buckets**:
   - **Static Content**: Stores static files such as images and videos.
   - **Backups/Logs**: Stores backups and log files.

### Architectural Pattern 2: Serverless Architecture

#### Visual Text Diagram:
```
                               +-------------------------+
                               |       Route 53          |
                               +-------------------------+
                                         |
                                         |
                               +-------------------------+
                               |       CloudFront        |
                               +-------------------------+
                                         |
                                         |
                               +-------------------------+
                               |      API Gateway        |
                               +-------------------------+
                                /           |           \
                               /            |            \
                 +------------------+ +------------------+ +------------------+
                 | Lambda Function  | | Lambda Function  | | Lambda Function  |
                 +------------------+ +------------------+ +------------------+
                         |                   |                   |
                         |                   |                   |
                 +-------------------+ +-------------------+ +-------------------+
                 | DynamoDB Table    | | DynamoDB Table    | | DynamoDB Table    |
                 +-------------------+ +-------------------+ +-------------------+
                         |                   |                   |
                         |                   |                   |
               +------------------+ +------------------+ +------------------+
               | S3 (Static Content)| | S3 (Static Content)| | S3 (Static Content)|
               +------------------+ +------------------+ +------------------+
```

#### Step-by-Step Details:
1. **Route 53**: DNS service to route traffic to CloudFront.
2. **CloudFront**: CDN to cache content and deliver it quickly to users globally.
3. **API Gateway**: Exposes HTTP endpoints to invoke Lambda functions.
4. **Lambda Functions**: Stateless compute functions that handle business logic.
5. **DynamoDB**: NoSQL database to store application data.
6. **S3 Buckets**: Store static content for the application.

### Architectural Pattern 3: Microservices Architecture

#### Visual Text Diagram:
```
                             +---------------------------+
                             |       Route 53            |
                             +---------------------------+
                                       |
                                       |
                             +---------------------------+
                             |       API Gateway         |
                             +---------------------------+
                              /           |           \
                             /            |            \
              +-------------------+ +-------------------+ +-------------------+
              | ECS Service       | | ECS Service       | | ECS Service       |
              | (Microservice A)  | | (Microservice B)  | | (Microservice C)  |
              +-------------------+ +-------------------+ +-------------------+
                      |                     |                     |
                      |                     |                     |
        +-------------------+ +-------------------+ +-------------------+
        | Private Subnet    | | Private Subnet    | | Private Subnet    |
        | (us-west-2a)      | | (us-west-2b)      | | (us-west-2c)      |
        +-------------------+ +-------------------+ +-------------------+
                      |                     |                     |
                      |                     |                     |
             +--------------------+ +--------------------+ +--------------------+
             | RDS (Database A)   | | RDS (Database B)   | | RDS (Database C)   |
             +--------------------+ +--------------------+ +--------------------+
                      |                     |                     |
                      |                     |                     |
          +-------------------+ +-------------------+ +-------------------+
          | CloudWatch        | | CloudWatch        | | CloudWatch        |
          | Logs & Metrics    | | Logs & Metrics    | | Logs & Metrics    |
          +-------------------+ +-------------------+ +-------------------+
                      |                     |                     |
                      |                     |                     |
            +------------------+ +------------------+ +------------------+
            | CloudMap (Service)| | CloudMap (Service)| | CloudMap (Service)|
            +------------------+ +------------------+ +------------------+
```

#### Step-by-Step Details:
1. **Route 53**: DNS service to route traffic to API Gateway.
2. **API Gateway**: Routes requests to different microservices.
3. **ECS Services**: Host different microservices.
   - **Microservice A, B, C**: Different microservices running on ECS.
4. **Private Subnets**: Host RDS instances.
   - **RDS (Database A, B, C)**: Databases for each microservice.
5. **CloudWatch**: Monitors logs and metrics for the microservices.
6. **CloudMap**: Provides service discovery for the microservices.

### Architectural Pattern 4: Data Lake Architecture

#### Visual Text Diagram:
```
                       +------------------------+
                       |       Route 53         |
                       +------------------------+
                                 |
                                 |
                       +------------------------+
                       |       CloudFront       |
                       +------------------------+
                                 |
                                 |
                       +------------------------+
                       |         S3             |
                       |  (Raw Data Storage)    |
                       +------------------------+
                                 |
                                 |
                       +------------------------+
                       |       AWS Glue         |
                       +------------------------+
                        /         |          \
                       /          |           \
      +------------------+ +------------------+ +------------------+
      |  AWS Glue ETL    | |  AWS Glue ETL    | |  AWS Glue ETL    |
      +------------------+ +------------------+ +------------------+
                |                   |                    |
                |                   |                    |
      +-------------------+ +-------------------+ +-------------------+
      | S3 (Processed Data)| | S3 (Processed Data)| | S3 (Processed Data)|
      +-------------------+ +-------------------+ +-------------------+
                |                   |                    |
                |                   |                    |
      +-------------------+ +-------------------+ +-------------------+
      |  Athena Queries   | |  Athena Queries   | |  Athena Queries   |
      +-------------------+ +-------------------+ +-------------------+
                |                   |                    |
                |                   |                    |
      +-------------------+ +-------------------+ +-------------------+
      | Redshift Spectrum | | Redshift Spectrum | | Redshift Spectrum |
      +-------------------+ +-------------------+ +-------------------+
                |                   |                    |
                |                   |                    |
      +-------------------+ +-------------------+ +-------------------+
      | Kinesis Streams   | | Kinesis Streams   | | Kinesis Streams   |
      +-------------------+ +-------------------+ +-------------------+
                |                   |                    |
                |                   |                    |
      +-------------------+ +-------------------+ +-------------------+
      |  S3 (Curated Data)| |  S3 (Curated Data)| |  S3 (Curated Data)|
      +-------------------+ +-------------------+ +-------------------+
```

#### Step-by-Step Details:
1. **Route 53**: DNS service to route traffic to CloudFront.
2. **CloudFront**: CDN to cache content and deliver it quickly to users globally.
3. **S3 Buckets**:
   - **Raw Data Storage**: Stores raw data.
4. **AWS Glue**: Extract, transform, load (ETL) service.
   - **AWS Glue ETL**: Processes raw data and stores it in the

 processed data bucket.
5. **S3 Buckets**:
   - **Processed Data**: Stores processed data.
6. **Athena**: Query the processed data stored in S3.
7. **Redshift Spectrum**: Run SQL queries on the processed data in S3.
8. **Kinesis**: Real-time data streaming into the data lake.
   - **Kinesis Streams**: Streams data to the data lake.
9. **S3 Buckets**:
   - **Curated Data**: Stores curated data after further processing.

These visual text diagrams with step-by-step details provide a clear overview of each architectural pattern, showing how different AWS services are integrated to build scalable, secure, and efficient applications.

