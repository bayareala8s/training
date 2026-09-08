resource "aws_ecr_repository" "payment" {
  name                 = "baypay/payment-service-ecs-demo"
  image_tag_mutability = "IMMUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_lb" "pay" {
  name               = "${var.name_prefix}-alb"
  load_balancer_type = "application"
  internal           = false
  subnets            = aws_subnet.public[*].id
  security_groups    = [aws_security_group.alb.id]
  idle_timeout       = 60
}

resource "aws_lb_target_group" "pay" {
  name        = "${var.name_prefix}-tg"
  port        = 8080
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.lab.id

  deregistration_delay = 30

  health_check {
    enabled             = true
    path                = "/actuator/health/liveness"
    port                = "8080"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.pay.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.pay.arn
  }
}

resource "aws_cloudwatch_log_group" "pay" {
  name              = "/ecs/${var.name_prefix}/payment-service"
  retention_in_days = 3
}

resource "aws_ecs_cluster" "lab" {
  name = "${var.name_prefix}-cluster"

  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}

resource "aws_ecs_task_definition" "payment" {
  count                    = local.deploy ? 1 : 0
  family                   = "${var.name_prefix}-payment"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.task.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  container_definitions = jsonencode([
    {
      name      = "payment"
      image     = var.container_image
      essential = true
      portMappings = [
        {
          protocol      = "tcp"
          containerPort = 8080
        }
      ]
      environment = [
        { name = "SPRING_PROFILES_ACTIVE", value = "ecs" }
      ]
      secrets = [
        {
          name      = "BAYPAY_DB_URL"
          valueFrom = "${aws_secretsmanager_secret.db.arn}:url::"
        },
        {
          name      = "BAYPAY_DB_USER"
          valueFrom = "${aws_secretsmanager_secret.db.arn}:username::"
        },
        {
          name      = "BAYPAY_DB_PASSWORD"
          valueFrom = "${aws_secretsmanager_secret.db.arn}:password::"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.pay.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "payment"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "payment" {
  count           = local.deploy ? 1 : 0
  name            = "${var.name_prefix}-payment"
  cluster         = aws_ecs_cluster.lab.id
  task_definition = aws_ecs_task_definition.payment[0].arn
  desired_count   = 1
  launch_type     = "FARGATE"

  health_check_grace_period_seconds = 180

  network_configuration {
    subnets          = aws_subnet.public[*].id
    security_groups  = [aws_security_group.tasks.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.pay.arn
    container_name   = "payment"
    container_port   = 8080
  }

  depends_on = [
    aws_lb_listener.http,
    aws_secretsmanager_secret_version.db,
    aws_iam_role_policy.execution_secrets,
  ]
}
