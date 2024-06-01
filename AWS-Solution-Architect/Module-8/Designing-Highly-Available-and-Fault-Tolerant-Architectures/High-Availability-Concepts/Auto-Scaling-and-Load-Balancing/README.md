## Detailed Guide on Auto Scaling and Load Balancing in AWS

### Introduction
Auto Scaling and Load Balancing are essential components of a resilient and scalable architecture in AWS. They help maintain application availability, optimize performance, and manage costs by automatically adjusting the number of instances and distributing traffic.

### Key Concepts

1. **Auto Scaling:**
   - **Auto Scaling Group (ASG):** A collection of EC2 instances that are managed as a group. ASG ensures that your application has the right number of instances to handle the load.
   - **Scaling Policies:** Define the conditions under which the ASG should add or remove instances. These can be based on metrics like CPU utilization, request count, or custom metrics.
   - **Launch Configuration/Template:** Defines the instance type, AMI, key pair, security groups, and other instance settings for the instances in the ASG.

2. **Load Balancing:**
   - **Elastic Load Balancer (ELB):** Distributes incoming traffic across multiple targets (EC2 instances, containers, IP addresses) in one or more Availability Zones (AZs).
   - **Types of Load Balancers:**
     - **Application Load Balancer (ALB):** Operates at the application layer (HTTP/HTTPS) and is suitable for web applications.
     - **Network Load Balancer (NLB):** Operates at the transport layer (TCP/UDP) and is suitable for high-performance networking.
     - **Classic Load Balancer (CLB):** Legacy option for both application and network layers.

### Benefits of Auto Scaling and Load Balancing

- **High Availability:** Ensures applications remain operational and accessible.
- **Fault Tolerance:** Distributes traffic and workload to healthy instances.
- **Cost Optimization:** Adjusts the number of running instances based on demand.
- **Improved Performance:** Balances load to avoid overloading any single instance.

### Implementation Steps

#### 1. Creating a VPC

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
```

#### 2. Setting Up Security Groups

**Terraform Script:**
```hcl
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
```

#### 3. Creating a Launch Configuration/Template

**Terraform Script:**
```hcl
resource "aws_launch_configuration" "web_lc" {
  name          = "web-lc"
  image_id      = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t3.micro"
  security_groups = [aws_security_group.web_sg.id]

  lifecycle {
    create_before_destroy = true
  }
}
```

#### 4. Creating an Auto Scaling Group (ASG)

**Terraform Script:**
```hcl
resource "aws_autoscaling_group" "web_asg" {
  desired_capacity     = 2
  max_size             = 4
  min_size             = 1
  vpc_zone_identifier  = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
  launch_configuration = aws_launch_configuration.web_lc.id

  tag {
    key                 = "Name"
    value               = "web-server"
    propagate_at_launch = true
  }
}
```

#### 5. Creating an Application Load Balancer (ALB)

**Terraform Script:**
```hcl
resource "aws_alb" "main" {
  name            = "main-alb"
  internal        = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.web_sg.id]
  subnets         = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
}

resource "aws_alb_target_group" "web_tg" {
  name     = "web-tg"
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
  load_balancer_arn = aws_alb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.web_tg.arn
  }
}
```

#### 6. Adding Auto Scaling Policies

**Terraform Script:**
```hcl
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.web_asg.name

  metric_aggregation_type = "Average"
  estimated_instance_warmup = 60

  step_adjustment {
    scaling_adjustment          = 1
    metric_interval_lower_bound = 0
  }
}

resource "aws_autoscaling_policy" "scale_down" {
  name                   = "scale-down"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.web_asg.name

  metric_aggregation_type = "Average"
  estimated_instance_warmup = 60

  step_adjustment {
    scaling_adjustment          = -1
    metric_interval_lower_bound = 0
  }
}
```

### Monitoring and Alerts

#### 1. Setting Up CloudWatch Alarms

**Terraform Script:**
```hcl
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"

  alarm_actions       = [aws_autoscaling_policy.scale_up.arn]
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.web_asg.name
  }
}

resource "aws_cloudwatch_metric_alarm" "low_cpu" {
  alarm_name          = "low-cpu"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "20"

  alarm_actions       = [aws_autoscaling_policy.scale_down.arn]
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.web_asg.name
  }
}
```

### Conclusion

Auto Scaling and Load Balancing are fundamental for creating a scalable and resilient architecture in AWS. By using Terraform, you can automate the creation and management of these components, ensuring your applications are always available, performant, and cost-effective. This guide provided a detailed step-by-step implementation of Auto Scaling and Load Balancing using Terraform scripts, from creating a VPC to setting up monitoring and alerts.


## Detailed Guide on Real-World Examples and Implementation

### Real-World Example 1: E-Commerce Application

#### Scenario:
An e-commerce platform needs to handle various services such as user authentication, product catalog, shopping cart, and order processing. Each service should be independently deployable and scalable.

### Step-by-Step Implementation

#### 1. Setting Up the Environment

**Step 1: Provider Configuration**

Configure the AWS provider.
```hcl
provider "aws" {
  region = "us-east-1"
}
```

**Step 2: Create a VPC**

Create a VPC with subnets in multiple Availability Zones (AZs).
```hcl
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
```

#### 2. Creating Security Groups

Define security groups to control inbound and outbound traffic.
```hcl
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
```

#### 3. Launching EC2 Instances for Microservices

Launch EC2 instances for each microservice.
```hcl
resource "aws_instance" "user_service" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_1.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "user-service"
  }
}

resource "aws_instance" "product_service" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_2.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "product-service"
  }
}

resource "aws_instance" "cart_service" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_3.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "cart-service"
  }
}

resource "aws_instance" "order_service" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_1.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "order-service"
  }
}
```

#### 4. Setting Up an Application Load Balancer (ALB)

Create an ALB and define target groups for each microservice.
```hcl
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
```

#### 5. Configuring ALB Listener with Routing Rules

Define listener rules to route traffic to the appropriate target groups.
```hcl
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

### Real-World Example 2: Financial Services Platform

#### Scenario:
A financial services platform needs to manage various services such as user account management, transaction processing, fraud detection, and reporting. Each service must be secure, scalable, and independently deployable.

### Step-by-Step Implementation

#### 1. Setting Up the Environment

**Step 1: Provider Configuration**

Configure the AWS provider.
```hcl
provider "aws" {
  region = "us-east-1"
}
```

**Step 2: Create a VPC**

Create a VPC with subnets in multiple Availability Zones (AZs).
```hcl
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
```

#### 2. Creating Security Groups

Define security groups to

 control inbound and outbound traffic.
```hcl
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
```

#### 3. Launching EC2 Instances for Microservices

Launch EC2 instances for each microservice.
```hcl
resource "aws_instance" "account_service" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_1.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "account-service"
  }
}

resource "aws_instance" "transaction_service" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_2.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "transaction-service"
  }
}

resource "aws_instance" "fraud_service" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_3.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "fraud-service"
  }
}

resource "aws_instance" "reporting_service" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_1.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "reporting-service"
  }
}
```

#### 4. Setting Up an Application Load Balancer (ALB)

Create an ALB and define target groups for each microservice.
```hcl
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
```

#### 5. Configuring ALB Listener with Routing Rules

Define listener rules to route traffic to the appropriate target groups.
```hcl
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

### Real-World Example 3: Media Streaming Platform

#### Scenario:
A media streaming platform needs to manage various services such as user management, media catalog, streaming service, and analytics. Each service must be scalable and handle high loads.

### Step-by-Step Implementation

#### 1. Setting Up the Environment

**Step 1: Provider Configuration**

Configure the AWS provider.
```hcl
provider "aws" {
  region = "us-west-1"
}
```

**Step 2: Create a VPC**

Create a VPC with subnets in multiple Availability Zones (AZs).
```hcl
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
```

#### 2. Creating Security Groups

Define security groups to control inbound and outbound traffic.
```hcl
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
```

#### 3. Launching EC2 Instances for Microservices

Launch EC2 instances for each microservice.
```hcl
resource "aws_instance" "user_service" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_1.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "user-service"
  }
}

resource "aws_instance" "catalog_service" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_2.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "catalog-service"
  }
}

resource "aws_instance" "stream

ing_service" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_1.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "streaming-service"
  }
}

resource "aws_instance" "analytics_service" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.subnet_2.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "analytics-service"
  }
}
```

#### 4. Setting Up an Application Load Balancer (ALB)

Create an ALB and define target groups for each microservice.
```hcl
resource "aws_alb" "api_gateway" {
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
```

#### 5. Configuring ALB Listener with Routing Rules

Define listener rules to route traffic to the appropriate target groups.
```hcl
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

These detailed step-by-step guides provide comprehensive examples for implementing real-world microservices architectures in AWS using Terraform. Each example covers the setup of a VPC, security groups, EC2 instances for microservices, load balancers, and routing rules to ensure a scalable, highly available, and resilient infrastructure.
