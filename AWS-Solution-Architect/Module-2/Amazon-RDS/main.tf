# Configure the AWS provider
provider "aws" {
  region = "us-west-2"
}

# Data source for availability zones
data "aws_availability_zones" "available" {}

# Define a VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "main-vpc"
  }
}

# Define Subnets
resource "aws_subnet" "main" {
  count                   = 3
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone       = element(data.aws_availability_zones.available.names, count.index)

  tags = {
    Name = "main-subnet-${count.index}"
  }
}

# Define an Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main-igw"
  }
}

# Define a Route Table
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "main-route-table"
  }
}

# Associate Route Table with Subnets
resource "aws_route_table_association" "main" {
  count          = 3
  subnet_id      = aws_subnet.main[count.index].id
  route_table_id = aws_route_table.main.id
}

# Define a Security Group for RDS
resource "aws_security_group" "db_sg" {
  name        = "db_security_group"
  description = "Allow access to the RDS instances"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "db-security-group"
  }
}

# Define a DB Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "main"
  subnet_ids = aws_subnet.main.*.id

  tags = {
    Name = "main"
  }
}

# Create the Primary PostgreSQL RDS Instance with Cost Optimization
resource "aws_db_instance" "primary" {
  allocated_storage    = 20  # Reduced storage allocation
  storage_type         = "gp2"  # General Purpose (SSD) storage for cost savings
  engine               = "postgres"
  engine_version       = "16.2"  # Updated to PostgreSQL 16.2
  instance_class       = "db.t3.micro"  # Smaller instance class for cost savings
  db_name              = "ecommerce_db"
  username             = "pgadmin"  # Updated username
  password             = "password"  # Use secrets management for real applications
  parameter_group_name = "default.postgres16"
  multi_az             = true  # High availability still required
  publicly_accessible  = false
  skip_final_snapshot  = true
  backup_retention_period = 7  # Enable automated backups

  vpc_security_group_ids = [aws_security_group.db_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  tags = {
    Name = "ecommerce-primary-db"
  }

  performance_insights_enabled  = true
  performance_insights_retention_period = 7  # Retention period in days
  # Optional, if you want to encrypt performance insights data
  # performance_insights_kms_key_id = aws_kms_key.rds.arn 
}

# Add a null resource to ensure dependency
resource "null_resource" "wait_for_primary" {
  depends_on = [aws_db_instance.primary]
}

# Create Read Replicas with Cost Optimization
resource "aws_db_instance" "read_replica" {
  count                = 2
  storage_type         = "gp2"  # General Purpose (SSD) storage for cost savings
  engine               = "postgres"
  engine_version       = "16.2"  # Same version as primary
  instance_class       = "db.t3.micro"  # Smaller instance class for cost savings
  parameter_group_name = "default.postgres16"
  publicly_accessible  = false
  replicate_source_db  = aws_db_instance.primary.id

  vpc_security_group_ids = [aws_security_group.db_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  tags = {
    Name = "ecommerce-read-replica-${count.index}"
  }

  depends_on = [null_resource.wait_for_primary]
}

# Enable CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "cpu_utilization_high" {
  alarm_name                = "cpu_utilization_high"
  comparison_operator       = "GreaterThanThreshold"
  evaluation_periods        = "2"
  metric_name               = "CPUUtilization"
  namespace                 = "AWS/RDS"
  period                    = "300"
  statistic                 = "Average"
  threshold                 = "80"

  alarm_description         = "This alarm triggers when CPU utilization exceeds 80%"
  dimensions = {
    DBInstanceIdentifier = aws_db_instance.primary.id
  }

  actions_enabled           = true
  alarm_actions             = [aws_sns_topic.alerts.arn]
  ok_actions                = [aws_sns_topic.alerts.arn]

  tags = {
    Name = "cpu-utilization-high"
  }
}

# SNS Topic for Alerts
resource "aws_sns_topic" "alerts" {
  name = "rds-alerts"
}

# Optional: KMS Key for Performance Insights
resource "aws_kms_key" "rds" {
  description = "KMS key for RDS Performance Insights"

  tags = {
    Name = "rds-kms-key"
  }
}
