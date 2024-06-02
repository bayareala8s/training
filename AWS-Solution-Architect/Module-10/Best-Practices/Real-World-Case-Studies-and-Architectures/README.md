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
