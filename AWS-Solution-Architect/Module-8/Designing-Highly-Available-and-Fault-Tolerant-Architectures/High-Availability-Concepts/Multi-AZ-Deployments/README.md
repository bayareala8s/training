## Detailed Guide for Multi-AZ Deployments in AWS

### Introduction
Multi-AZ (Availability Zone) deployments in AWS enhance the availability and durability of applications by distributing them across multiple, physically separated locations within an AWS region. This guide will cover the concepts, benefits, and implementation of Multi-AZ deployments.

### Key Concepts

1. **Availability Zones (AZs):**
   - AZs are isolated locations within an AWS region. Each AZ has independent power, cooling, and networking to provide high availability and fault tolerance.
   - Using multiple AZs ensures that application failures are isolated and do not affect other AZs.

2. **Multi-AZ Deployment:**
   - Multi-AZ deployments distribute application components across multiple AZs to ensure high availability.
   - This setup automatically handles failover and recovery in case of an AZ failure.

### Benefits of Multi-AZ Deployments

1. **High Availability:**
   - Ensures that applications remain operational even if one AZ fails.
   - Automatically routes traffic to healthy instances in different AZs.

2. **Fault Tolerance:**
   - Isolates application failures to a single AZ, minimizing the impact on the overall application.

3. **Improved Durability:**
   - Data is replicated across multiple AZs, reducing the risk of data loss.

4. **Disaster Recovery:**
   - Provides a resilient architecture that can quickly recover from regional disasters.

### Implementation of Multi-AZ Deployments

#### 1. Multi-AZ Deployment for Amazon RDS

Amazon RDS provides built-in support for Multi-AZ deployments. When enabled, Amazon RDS automatically provisions and maintains a synchronous standby replica in a different AZ.

**Steps to Enable Multi-AZ for RDS:**

1. **Create an RDS Instance with Multi-AZ:**
   - In the AWS Management Console, navigate to RDS.
   - Click on "Create database".
   - Choose the database engine and specify the details.
   - Under "Availability & durability", select "Multi-AZ deployment".

2. **Modify an Existing RDS Instance to Multi-AZ:**
   - In the AWS Management Console, navigate to RDS.
   - Select the RDS instance to modify.
   - Click on "Modify".
   - Under "Availability & durability", select "Multi-AZ deployment".
   - Apply the changes.

**Terraform Script:**
```hcl
resource "aws_db_instance" "example" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  name                 = "exampledb"
  username             = "admin"
  password             = "password"
  multi_az             = true
  publicly_accessible  = false
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  db_subnet_group_name = aws_db_subnet_group.main.name
}
```

#### 2. Multi-AZ Deployment for Amazon EC2

For EC2 instances, Multi-AZ deployment involves launching instances in different AZs and using Elastic Load Balancing (ELB) to distribute traffic.

**Steps to Create Multi-AZ EC2 Deployment:**

1. **Create a VPC and Subnets:**
   - Create a VPC with subnets in different AZs.

2. **Launch EC2 Instances in Different AZs:**
   - Launch EC2 instances in the created subnets.

3. **Create an Application Load Balancer:**
   - Create an ALB and specify the subnets in different AZs.
   - Configure target groups to include the EC2 instances.

**Terraform Script:**
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
```

#### 3. Multi-AZ Deployment for Amazon EFS

Amazon EFS is a file storage service that provides scalable and highly available storage. EFS is inherently designed to be multi-AZ, storing data redundantly across multiple AZs.

**Steps to Create Multi-AZ EFS Deployment:**

1. **Create an EFS File System:**
   - In the AWS Management Console, navigate to EFS.
   - Create a new EFS file system and specify the VPC.

2. **Mount the EFS File System to EC2 Instances:**
   - Install the NFS client on your EC2 instances.
   - Mount the EFS file system to the EC2 instances.

**Terraform Script:**
```hcl
resource "aws_efs_file_system" "example" {
  lifecycle_policy {
    transition_to_ia = "AFTER_30_DAYS"
  }

  provisioned_throughput_in_mibps = 1024
  throughput_mode                 = "provisioned"
}

resource "aws_efs_mount_target" "example" {
  count           = 3
  file_system_id  = aws_efs_file_system.example.id
  subnet_id       = element([aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id], count.index)
  security_groups = [aws_security_group.web_sg.id]
}
```

### Conclusion

Multi-AZ deployments are crucial for building highly available and resilient applications in AWS. By distributing resources across multiple AZs, you can ensure that your application remains operational even in the event of an AZ failure. Using AWS services like RDS, EC2 with ALB, and EFS makes it easier to implement and manage Multi-AZ architectures.


### Real-World Microservices Examples

#### Example 1: E-Commerce Application

**Scenario:** 
An e-commerce platform needs to handle various services such as user authentication, product catalog, shopping cart, and order processing. Each service should be independently deployable and scalable.

**Architecture Overview:**
- **User Service:** Manages user authentication and profile information.
- **Product Service:** Handles product catalog and inventory.
- **Cart Service:** Manages user shopping carts.
- **Order Service:** Processes orders and payments.
- **API Gateway:** Routes requests to appropriate services.
- **Service Discovery:** Helps microservices discover each other.
- **Message Broker:** Facilitates communication between services (e.g., RabbitMQ, Amazon SQS).

**Terraform Script:**
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

resource "aws_instance" "user_service" {
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_1.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "user-service"
  }
}

resource "aws_instance" "product_service" {
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_2.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "product-service"
  }
}

resource "aws_instance" "cart_service" {
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_3.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "cart-service"
  }
}

resource "aws_instance" "order_service" {
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_1.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "order-service"
  }
}

resource "aws_alb" "api_gateway" {
  name            = "api-gateway"
  internal        = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.web_sg.id]
  subnets         = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
}

resource "aws_alb_target_group" "user_service_tg" {
  name     = "user-service-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_alb_target_group" "product_service_tg" {
  name     = "product-service-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_alb_target_group" "cart_service_tg" {
  name     = "cart-service-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_alb_target_group" "order_service_tg" {
  name     = "order-service-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_alb_listener" "http" {
  load_balancer_arn = aws_alb.api_gateway.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "Not Found"
      status_code  = "404"
    }
  }

  dynamic "rule" {
    for_each = [
      {
        priority = 10
        path     = "/user/*"
        target_group_arn = aws_alb_target_group.user_service_tg.arn
      },
      {
        priority = 20
        path     = "/product/*"
        target_group_arn = aws_alb_target_group.product_service_tg.arn
      },
      {
        priority = 30
        path     = "/cart/*"
        target_group_arn = aws_alb_target_group.cart_service_tg.arn
      },
      {
        priority = 40
        path     = "/order/*"
        target_group_arn = aws_alb_target_group.order_service_tg.arn
      }
    ]

    content {
      actions {
        type = "forward"
        target_group_arn = rule.value.target_group_arn
      }

      conditions {
        path_pattern {
          values = [rule.value.path]
        }
      }

      priority = rule.value.priority
    }
  }
}
```

#### Example 2: Financial Services Platform

**Scenario:** 
A financial services platform needs to manage various services such as user account management, transaction processing, fraud detection, and reporting. Each service must be secure, scalable, and independently deployable.

**Architecture Overview:**
- **Account Service:** Manages user accounts and profiles.
- **Transaction Service:** Handles financial transactions.
- **Fraud Detection Service:** Detects and prevents fraudulent activities.
- **Reporting Service:** Generates reports on transactions and user activities.
- **API Gateway:** Routes requests to appropriate services.
- **Service Discovery:** Helps microservices discover each other.
- **Message Broker:** Facilitates communication between services (e.g., RabbitMQ, Amazon SQS).

**Terraform Script:**
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
    to_port

     = 80
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

resource "aws_instance" "account_service" {
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_1.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "account-service"
  }
}

resource "aws_instance" "transaction_service" {
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_2.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "transaction-service"
  }
}

resource "aws_instance" "fraud_service" {
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_3.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "fraud-service"
  }
}

resource "aws_instance" "reporting_service" {
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_1.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "reporting-service"
  }
}

resource "aws_alb" "api_gateway" {
  name            = "api-gateway"
  internal        = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.web_sg.id]
  subnets         = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
}

resource "aws_alb_target_group" "account_service_tg" {
  name     = "account-service-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_alb_target_group" "transaction_service_tg" {
  name     = "transaction-service-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_alb_target_group" "fraud_service_tg" {
  name     = "fraud-service-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_alb_target_group" "reporting_service_tg" {
  name     = "reporting-service-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_alb_listener" "http" {
  load_balancer_arn = aws_alb.api_gateway.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "Not Found"
      status_code  = "404"
    }
  }

  dynamic "rule" {
    for_each = [
      {
        priority = 10
        path     = "/account/*"
        target_group_arn = aws_alb_target_group.account_service_tg.arn
      },
      {
        priority = 20
        path     = "/transaction/*"
        target_group_arn = aws_alb_target_group.transaction_service_tg.arn
      },
      {
        priority = 30
        path     = "/fraud/*"
        target_group_arn = aws_alb_target_group.fraud_service_tg.arn
      },
      {
        priority = 40
        path     = "/report/*"
        target_group_arn = aws_alb_target_group.reporting_service_tg.arn
      }
    ]

    content {
      actions {
        type = "forward"
        target_group_arn = rule.value.target_group_arn
      }

      conditions {
        path_pattern {
          values = [rule.value.path]
        }
      }

      priority = rule.value.priority
    }
  }
}
```

#### Example 3: Media Streaming Platform

**Scenario:** 
A media streaming platform needs to manage various services such as user management, media catalog, streaming service, and analytics. Each service must be scalable and handle high loads.

**Architecture Overview:**
- **User Service:** Manages user profiles and subscriptions.
- **Catalog Service:** Handles the media catalog and metadata.
- **Streaming Service:** Manages media streaming and content delivery.
- **Analytics Service:** Collects and processes usage data.
- **API Gateway:** Routes requests to appropriate services.
- **Service Discovery:** Helps microservices discover each other.
- **Message Broker:** Facilitates communication between services (e.g., RabbitMQ, Amazon SQS).

**Terraform Script:**
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

resource "aws_instance" "user_service" {
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_1.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "user-service"
  }
}

resource "aws_instance" "catalog_service" {
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_2.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "catalog-service"
  }
}

resource "aws_instance" "streaming_service" {
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_1.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "streaming-service"
  }
}

resource "aws_instance" "analytics_service" {
  ami           = "ami-0c55b159cbfafe1f0" // Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_2.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "analytics-service"
  }
}

resource "aws

_alb" "api_gateway" {
  name            = "api-gateway"
  internal        = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.web_sg.id]
  subnets         = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id]
}

resource "aws_alb_target_group" "user_service_tg" {
  name     = "user-service-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_alb_target_group" "catalog_service_tg" {
  name     = "catalog-service-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_alb_target_group" "streaming_service_tg" {
  name     = "streaming-service-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_alb_target_group" "analytics_service_tg" {
  name     = "analytics-service-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_alb_listener" "http" {
  load_balancer_arn = aws_alb.api_gateway.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "Not Found"
      status_code  = "404"
    }
  }

  dynamic "rule" {
    for_each = [
      {
        priority = 10
        path     = "/user/*"
        target_group_arn = aws_alb_target_group.user_service_tg.arn
      },
      {
        priority = 20
        path     = "/catalog/*"
        target_group_arn = aws_alb_target_group.catalog_service_tg.arn
      },
      {
        priority = 30
        path     = "/stream/*"
        target_group_arn = aws_alb_target_group.streaming_service_tg.arn
      },
      {
        priority = 40
        path     = "/analytics/*"
        target_group_arn = aws_alb_target_group.analytics_service_tg.arn
      }
    ]

    content {
      actions {
        type = "forward"
        target_group_arn = rule.value.target_group_arn
      }

      conditions {
        path_pattern {
          values = [rule.value.path]
        }
      }

      priority = rule.value.priority
    }
  }
}
```

These scripts provide a foundation for deploying microservices architectures on AWS for different scenarios. You can further customize them based on specific requirements and best practices.
