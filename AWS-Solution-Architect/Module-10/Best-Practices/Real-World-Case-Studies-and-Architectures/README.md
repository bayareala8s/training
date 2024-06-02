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
