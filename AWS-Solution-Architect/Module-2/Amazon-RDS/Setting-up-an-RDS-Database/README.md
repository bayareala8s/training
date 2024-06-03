## Step-by-Step Guide to Setting Up an RDS Database with Terraform

This guide provides a detailed walkthrough for setting up an AWS RDS database using Terraform. We'll cover two examples: setting up a MySQL instance for an e-commerce platform and a PostgreSQL instance for a healthcare application.

### Example 1: Setting Up an RDS MySQL Instance for an E-commerce Platform

#### Prerequisites
- Ensure Terraform is installed.
- AWS CLI configured with appropriate credentials.

#### Directory Structure
```
.
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
```

### Terraform Configuration Files

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

### Example 2: Setting Up an RDS PostgreSQL Instance for a Healthcare Application

#### Prerequisites
- Ensure Terraform is installed.
- AWS CLI configured with appropriate credentials.

#### Directory Structure
```
.
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
```

### Terraform Configuration Files

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

By following these steps and using the provided Terraform scripts, you can set up AWS RDS instances for MySQL and PostgreSQL databases, tailored to different application needs. If you have any specific questions or need further customization, feel free to ask!
