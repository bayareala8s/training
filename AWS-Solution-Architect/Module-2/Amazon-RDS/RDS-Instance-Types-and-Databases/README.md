### RDS Instance Types and Supported Databases

AWS RDS offers various instance types optimized for different use cases, such as general-purpose, memory-optimized, and burstable performance instances. Each instance type is designed to deliver a specific balance of compute, memory, and network resources.

### RDS Instance Classes

#### 1. General Purpose (Burstable Performance)
- **T3 and T4g Instances**: Suitable for workloads with moderate CPU usage that can benefit from CPU burst capabilities.

#### 2. Standard Purpose (Balance of Compute, Memory, and Network Resources)
- **M5 and M6g Instances**: Suitable for a wide range of applications, providing a balance of compute, memory, and network resources.

#### 3. Memory Optimized
- **R5 and R6g Instances**: Ideal for memory-intensive applications like databases, caching, and real-time big data analytics.

#### 4. Compute Optimized
- **C5 and C6g Instances**: Designed for compute-intensive applications that benefit from high-performance processors.

#### 5. Storage Optimized
- **I3 Instances**: Optimized for applications requiring high, sequential read and write access to large datasets on local storage.

### Supported Databases and Versions

#### 1. Amazon Aurora
- MySQL-Compatible Edition: Aurora MySQL 5.6, 5.7, and 8.0
- PostgreSQL-Compatible Edition: Aurora PostgreSQL 9.6, 10.x, 11.x, 12.x, and 13.x

#### 2. PostgreSQL
- PostgreSQL versions 9.6, 10.x, 11.x, 12.x, 13.x, 14.x

#### 3. MySQL
- MySQL versions 5.6, 5.7, and 8.0

#### 4. MariaDB
- MariaDB versions 10.2, 10.3, 10.4, 10.5, and 10.6

#### 5. Oracle
- Oracle Database versions 12.1, 12.2, 18c, 19c

#### 6. SQL Server
- SQL Server 2012, 2014, 2016, 2017, 2019 (Web, Express, Standard, Enterprise editions)

### Example Terraform Scripts for Different Databases

Below are the Terraform scripts to deploy an RDS instance for various database engines.

### Example 1: Deploying an RDS PostgreSQL Instance

#### main.tf
```hcl
# main.tf

# Define the provider
provider "aws" {
  region = var.region
}

# Create a VPC
resource "aws_vpc" "main_vpc" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = "main_vpc"
  }
}

# Create Subnets
resource "aws_subnet" "subnet_a" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = var.subnet_a_cidr
  availability_zone = "${var.region}a"
  tags = {
    Name = "subnet_a"
  }
}

resource "aws_subnet" "subnet_b" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = var.subnet_b_cidr
  availability_zone = "${var.region}b"
  tags = {
    Name = "subnet_b"
  }
}

# Create an Internet Gateway
resource "aws_internet_gateway" "main_igw" {
  vpc_id = aws_vpc.main_vpc.id
  tags = {
    Name = "main_igw"
  }
}

# Create Route Table and Associate with Subnets
resource "aws_route_table" "main_rt" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main_igw.id
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet_a.id
  route_table_id = aws_route_table.main_rt.id
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.subnet_b.id
  route_table_id = aws_route_table.main_rt.id
}

# Create Security Group
resource "aws_security_group" "main_sg" {
  vpc_id = aws_vpc.main_vpc.id
  name   = "main_sg"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "main_sg"
  }
}

# Create RDS PostgreSQL Instance
resource "aws_db_instance" "postgres_instance" {
  allocated_storage    = 50
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "13.4"
  instance_class       = "db.m5.large"
  name                 = var.db_name
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.postgres13"
  multi_az             = true
  publicly_accessible  = false
  vpc_security_group_ids = [aws_security_group.main_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.main_subnet_group.name
  tags = {
    Name = "postgres_instance"
  }
}

# Create a DB Subnet Group
resource "aws_db_subnet_group" "main_subnet_group" {
  name       = "main_subnet_group"
  subnet_ids = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id]
  tags = {
    Name = "main_subnet_group"
  }
}
```

#### variables.tf
```hcl
# variables.tf

variable "region" {
  description = "The AWS region to deploy resources."
  type        = string
  default     = "us-west-2"
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_a_cidr" {
  description = "The CIDR block for subnet A."
  type        = string
  default     = "10.0.1.0/24"
}

variable "subnet_b_cidr" {
  description = "The CIDR block for subnet B."
  type        = string
  default     = "10.0.2.0/24"
}

variable "my_ip_cidr" {
  description = "Your IP address in CIDR notation."
  type        = string
}

variable "db_name" {
  description = "The name of the RDS database."
  type        = string
  default     = "healthcare_db"
}

variable "db_username" {
  description = "The username for the RDS database."
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "The password for the RDS database."
  type        = string
}
```

#### outputs.tf
```hcl
# outputs.tf

output "vpc_id" {
  description = "The ID of the VPC."
  value       = aws_vpc.main_vpc.id
}

output "subnet_a_id" {
  description = "The ID of subnet A."
  value       = aws_subnet.subnet_a.id
}

output "subnet_b_id" {
  description = "The ID of subnet B."
  value       = aws_subnet.subnet_b.id
}

output "rds_endpoint" {
  description = "The endpoint of the RDS instance."
  value       = aws_db_instance.postgres_instance.endpoint
}

output "rds_db_name" {
  description = "The name of the RDS database."
  value       = aws_db_instance.postgres_instance.name
}
```

#### terraform.tfvars
```hcl
# terraform.tfvars

my_ip_cidr = "your.ip.address/32"
db_password = "your_db_password"
```

### Example 2: Deploying an RDS MySQL Instance

#### main.tf
```hcl
# main.tf

# Define the provider
provider "aws" {
  region = var.region
}

# Create a VPC
resource "aws_vpc" "main_vpc" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = "main_vpc"
  }
}

# Create Subnets
resource "aws_subnet" "subnet_a" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = var.subnet_a_cidr
  availability_zone = "${var.region}a"
  tags = {
    Name = "subnet_a"
  }
}

resource "aws_subnet" "subnet_b" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = var.subnet_b_cidr
  availability_zone = "${var.region}b"
  tags = {
    Name = "subnet_b"
  }
}

# Create an Internet Gateway
resource "aws_internet_gateway" "main_igw" {
  vpc_id = aws

_vpc.main_vpc.id
  tags = {
    Name = "main_igw"
  }
}

# Create Route Table and Associate with Subnets
resource "aws_route_table" "main_rt" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main_igw.id
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet_a.id
  route_table_id = aws_route_table.main_rt.id
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.subnet_b.id
  route_table_id = aws_route_table.main_rt.id
}

# Create Security Group
resource "aws_security_group" "main_sg" {
  vpc_id = aws_vpc.main_vpc.id
  name   = "main_sg"

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "main_sg"
  }
}

# Create RDS MySQL Instance
resource "aws_db_instance" "mysql_instance" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.medium"
  name                 = var.db_name
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.mysql8.0"
  multi_az             = true
  publicly_accessible  = false
  vpc_security_group_ids = [aws_security_group.main_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.main_subnet_group.name
  tags = {
    Name = "mysql_instance"
  }
}

# Create a DB Subnet Group
resource "aws_db_subnet_group" "main_subnet_group" {
  name       = "main_subnet_group"
  subnet_ids = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id]
  tags = {
    Name = "main_subnet_group"
  }
}
```

#### variables.tf
```hcl
# variables.tf

variable "region" {
  description = "The AWS region to deploy resources."
  type        = string
  default     = "us-west-2"
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_a_cidr" {
  description = "The CIDR block for subnet A."
  type        = string
  default     = "10.0.1.0/24"
}

variable "subnet_b_cidr" {
  description = "The CIDR block for subnet B."
  type        = string
  default     = "10.0.2.0/24"
}

variable "my_ip_cidr" {
  description = "Your IP address in CIDR notation."
  type        = string
}

variable "db_name" {
  description = "The name of the RDS database."
  type        = string
  default     = "ecommerce_db"
}

variable "db_username" {
  description = "The username for the RDS database."
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "The password for the RDS database."
  type        = string
}
```

#### outputs.tf
```hcl
# outputs.tf

output "vpc_id" {
  description = "The ID of the VPC."
  value       = aws_vpc.main_vpc.id
}

output "subnet_a_id" {
  description = "The ID of subnet A."
  value       = aws_subnet.subnet_a.id
}

output "subnet_b_id" {
  description = "The ID of subnet B."
  value       = aws_subnet.subnet_b.id
}

output "rds_endpoint" {
  description = "The endpoint of the RDS instance."
  value       = aws_db_instance.mysql_instance.endpoint
}

output "rds_db_name" {
  description = "The name of the RDS database."
  value       = aws_db_instance.mysql_instance.name
}
```

#### terraform.tfvars
```hcl
# terraform.tfvars

my_ip_cidr = "your.ip.address/32"
db_password = "your_db_password"
```

### Steps to Apply Terraform Scripts

1. **Initialize Terraform:**
   ```sh
   terraform init
   ```

2. **Validate the Configuration:**
   ```sh
   terraform validate
   ```

3. **Plan the Deployment:**
   ```sh
   terraform plan
   ```

4. **Apply the Configuration:**
   ```sh
   terraform apply
   ```

These scripts and steps will help you set up AWS RDS instances for different use cases, ensuring that you have a robust, secure, and high-performing database infrastructure. If you have any specific questions or need further customization, feel free to ask!
