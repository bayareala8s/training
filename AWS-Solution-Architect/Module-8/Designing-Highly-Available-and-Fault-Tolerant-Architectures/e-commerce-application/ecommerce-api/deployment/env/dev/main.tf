provider "aws" {
  region = "us-west-2"
}

# Create a VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# Create an Internet Gateway for the VPC
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

# Allocate an Elastic IP for the NAT Gateway
resource "aws_eip" "main" {
  domain = "vpc"
}

# Create a NAT Gateway in the first public subnet
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.main.id
  subnet_id     = aws_subnet.public[0].id
}

# Create public subnets in different availability zones
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index}.0/24"
  availability_zone       = element(data.aws_availability_zones.available.names, count.index)
  map_public_ip_on_launch = true
}

# Create private subnets in different availability zones
resource "aws_subnet" "private" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 2}.0/24"
  availability_zone       = element(data.aws_availability_zones.available.names, count.index)
}

# Create a route table for public subnets and associate it with the Internet Gateway
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

# Create a route table for private subnets and associate it with the NAT Gateway
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }
}

# Associate public subnets with the public route table
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Associate private subnets with the private route table
resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

# Security group for the Application Load Balancer
resource "aws_security_group" "alb" {
  vpc_id = aws_vpc.main.id

  ingress {
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

# Security group for the ECS tasks
resource "aws_security_group" "ecs" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 3000
    to_port     = 3000
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

# Security group for the RDS instance
resource "aws_security_group" "rds" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [aws_security_group.ecs.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create a custom parameter group for PostgreSQL
resource "aws_db_parameter_group" "postgres" {
  name        = "custom-postgres-parameter-group"
  family      = "postgres16"
  description = "Custom parameter group for PostgreSQL"

  parameter {
    name  = "rds.force_ssl"
    value = "0"
  }
}

# Create a PostgreSQL RDS instance
resource "aws_db_instance" "postgres" {
  allocated_storage    = 20
  engine               = "postgres"
  instance_class       = "db.t3.micro"
  db_name              = "ecommerce"
  username             = "postgres"
  password             = "your-password"
  skip_final_snapshot  = true
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name = aws_db_subnet_group.main.name
  multi_az             = false
}

# Create a DB subnet group for the RDS instance
resource "aws_db_subnet_group" "main" {
  name       = "main"
  subnet_ids = aws_subnet.private[*].id
}

# IAM role for ECS task execution
resource "aws_iam_role" "ecs_task_execution" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
    "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess",
  ]
}

# Create an ECS cluster
resource "aws_ecs_cluster" "main" {
  name = "ecommerce-cluster"
}

# Create an ECR repository
resource "aws_ecr_repository" "main" {
  name = "ecommerce-api"
}

# Create a CloudWatch log group
resource "aws_cloudwatch_log_group" "ecs_log_group" {
  name              = "/ecs/ecommerce-api"
  retention_in_days = 7
}

# Define an ECS task definition
resource "aws_ecs_task_definition" "app" {
  family                   = "ecommerce-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn

  container_definitions = jsonencode([
    {
      name      = "ecommerce-api"
      image     = "${aws_ecr_repository.main.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 3000
          hostPort      = 3000
        }
      ]
      environment = [
        {
          name  = "POSTGRES_HOST"
          value = aws_db_instance.postgres.address
        },
        {
          name  = "POSTGRES_PORT"
          value = "5432"
        },
        {
          name  = "POSTGRES_USER"
          value = "postgres"
        },
        {
          name  = "POSTGRES_PASSWORD"
          value = "your-password"
        },
        {
          name  = "POSTGRES_DB"
          value = "ecommerce"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/ecommerce-api"
          "awslogs-region"        = "us-west-2"
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}

# Create an ECS service
resource "aws_ecs_service" "main" {
  name            = "ecommerce-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 1

  launch_type = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.public[*].id
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.main.arn
    container_name   = "ecommerce-api"
    container_port   = 3000
  }

  depends_on = [aws_lb_listener.main]
}

# Create an Application Load Balancer
resource "aws_lb" "main" {
  name               = "ecommerce-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id
}

# Create a target group for the load balancer
resource "aws_lb_target_group" "main" {
  name        = "ecommerce-tg"
  port        = 3000
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"
}

# Create a listener for the load balancer
resource "aws_lb_listener" "main" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.arn
  }
}

# Data source for availability zones
data "aws_availability_zones" "available" {}

# Fetching the AWS account ID to ensure the bucket name is unique
data "aws_caller_identity" "current" {}

# Create an S3 bucket for CloudFront logs with a unique name
resource "aws_s3_bucket" "cloudfront_logs" {
  bucket = "cloudfront-logs-bucket-${data.aws_caller_identity.current.account_id}"
  acl    = "log-delivery-write"

  lifecycle {
    #prevent_destroy = true
  }
}

# Attach a bucket policy to allow CloudFront to write logs
resource "aws_s3_bucket_policy" "cloudfront_logs_policy" {
  bucket = aws_s3_bucket.cloudfront_logs.bucket

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "cloudfront.amazonaws.com"
        },
        Action = "s3:PutObject",
        Resource = "${aws_s3_bucket.cloudfront_logs.arn}/*",
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = "arn:aws:cloudfront::${data.aws_caller_identity.current.account_id}:distribution/*"
          }
        }
      }
    ]
  })
}

# Create a CloudFront origin access identity (OAI)
resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for ALB"
}

# Create CloudFront distribution
resource "aws_cloudfront_distribution" "api_distribution" {
  origin {
    domain_name = aws_lb.main.dns_name
    origin_id   = "alb_origin"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1", "TLSv1.1", "TLSv1.2"]
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CloudFront distribution for APIs"
  default_root_object = ""

  #aliases = ["your-api-domain.com"] # Optional, add your custom domain here

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "alb_origin"

    forwarded_values {
      query_string = true
      cookies {
        forward = "all"
      }
    }

    viewer_protocol_policy = "redirect-to-https"

    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  price_class = "PriceClass_All"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
    # To use your own certificate, specify the ARN
    # acm_certificate_arn            = "arn:aws:acm:region:account-id:certificate/certificate-id"
    # ssl_support_method             = "sni-only"
    # minimum_protocol_version       = "TLSv1.2_2019"
  }

  logging_config {
    bucket = aws_s3_bucket.cloudfront_logs.bucket_domain_name
    include_cookies = false
    prefix = "api-logs/"
  }
}









