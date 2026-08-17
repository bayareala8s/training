# Step 1: Configure the AWS Provider
provider "aws" {
  region = "us-west-2"
}

# Step 2: Create a new VPC for our EKS Cluster
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "main"
  }
}

# Step 3: Create a Subnet within our VPC
resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "main"
  }
}

# Step 4: Create an EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "17.1.0"

  cluster_name    = "my-cluster"
  cluster_version = "1.20"
  subnets         = [aws_subnet.main.id]

  node_groups = {
    eks_nodes = {
      desired_capacity = 2
      max_capacity     = 2
      min_capacity     = 1

      instance_type = "t3.micro"
    }
  }
}

# Step 5: Create a Security Group for our RDS Instance
resource "aws_security_group" "rds" {
  name        = "rds"
  description = "Allow inbound traffic from EKS nodes to RDS"
  vpc_id      = aws_vpc.main.id
}

# Step 6: Allow EKS nodes to communicate with RDS
resource "aws_security_group_rule" "rds_access" {
  type              = "ingress"
  from_port         = 5432
  to_port           = 5432
  protocol          = "tcp"
  security_group_id = aws_security_group.rds.id
  cidr_blocks       = [aws_vpc.main.cidr_block]
}

# Step 7: Create an RDS instance
resource "aws_db_instance" "default" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "13.3"
  instance_class       = "db.t2.micro"
  name                 = "mydb"
  username             = "foo"
  password = "foobarbaz"
  parameter_group_name = "default.postgres13"
  vpc_security_group_ids = [aws_security_group.rds.id]
  skip_final_snapshot = true
}