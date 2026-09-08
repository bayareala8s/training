data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  azs    = slice(data.aws_availability_zones.available.names, 0, 2)
  deploy = var.deploy_service && var.container_image != ""
}

resource "aws_vpc" "lab" {
  cidr_block           = "10.20.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags                 = { Name = "${var.name_prefix}-vpc" }
}

resource "aws_internet_gateway" "lab" {
  vpc_id = aws_vpc.lab.id
  tags   = { Name = "${var.name_prefix}-igw" }
}

resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.lab.id
  cidr_block              = cidrsubnet(aws_vpc.lab.cidr_block, 8, count.index + 1)
  availability_zone       = local.azs[count.index]
  map_public_ip_on_launch = true
  tags                    = { Name = "${var.name_prefix}-public-${count.index}" }
}

# RDS only. No NAT, no IGW route. Tasks reach 5432 over the VPC local route.
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.lab.id
  cidr_block        = cidrsubnet(aws_vpc.lab.cidr_block, 8, count.index + 11)
  availability_zone = local.azs[count.index]
  tags              = { Name = "${var.name_prefix}-private-${count.index}" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.lab.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.lab.id
  }

  tags = { Name = "${var.name_prefix}-public-rt" }
}

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "alb" {
  name        = "${var.name_prefix}-alb"
  description = "ALB ingress 80 from the internet"
  vpc_id      = aws_vpc.lab.id

  ingress {
    description = "HTTP from clients"
    from_port   = 80
    to_port     = 80
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

resource "aws_security_group" "tasks" {
  name        = "${var.name_prefix}-tasks"
  description = "Fargate tasks accept 8080 from the ALB only"
  vpc_id      = aws_vpc.lab.id

  ingress {
    description     = "payment-service from ALB"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "ECR, CloudWatch Logs, Secrets Manager via IGW"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "VPC DNS"
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = [aws_vpc.lab.cidr_block]
  }

  # Inline, not a standalone rule. Mixing the two on this SG dropped 5432 on Phase 2.
  egress {
    description     = "JDBC to RDS"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.rds.id]
  }
}

resource "aws_security_group" "rds" {
  name        = "${var.name_prefix}-rds"
  description = "Postgres 5432 from Fargate tasks only"
  vpc_id      = aws_vpc.lab.id
}

resource "aws_security_group_rule" "rds_from_tasks" {
  type                     = "ingress"
  description              = "Postgres from Fargate tasks"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.rds.id
  source_security_group_id = aws_security_group.tasks.id
}
