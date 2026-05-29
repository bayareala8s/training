resource "aws_ecs_cluster" "main" {
  name = "${local.name_prefix}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = local.common_tags
}

resource "aws_service_discovery_private_dns_namespace" "main" {
  name        = local.service_discovery_namespace
  description = "Course microservices discovery"
  vpc         = aws_vpc.main.id
  tags        = local.common_tags
}

resource "aws_service_discovery_service" "services" {
  for_each = local.services

  name = each.key

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.main.id
    dns_records {
      ttl  = 10
      type = "A"
    }
    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}

resource "aws_ecs_task_definition" "services" {
  for_each = local.services

  family                   = "${local.name_prefix}-${each.key}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = each.value.cpu
  memory                   = each.value.memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([
    {
      name      = each.key
      image     = "${aws_ecr_repository.services[each.key].repository_url}:${var.container_image_tag}"
      essential = true
      portMappings = [{
        containerPort = each.value.port
        protocol      = "tcp"
      }]
      environment = concat(
        [
          { name = "AWS_REGION", value = var.aws_region },
          { name = "JWT_SECRET", value = var.jwt_secret },
          { name = "DATABASE_URL", value = "sqlite:////tmp/${each.key}.db" },
          {
            name  = "PRODUCT_SERVICE_URL"
            value = local.product_service_url
          },
          {
            name  = "EVENT_HTTP_ENDPOINT"
            value = local.event_http_endpoint
          },
          { name = "EVENT_PUBLISH_MODE", value = "http" },
          { name = "EVENT_BUS_NAME", value = aws_cloudwatch_event_bus.platform.name },
          { name = "DYNAMODB_ORDERS_TABLE", value = aws_dynamodb_table.orders.name },
        ],
        [for k, v in each.value.extra_env : { name = k, value = v }]
      )
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = each.key
        }
      }
      healthCheck = {
        command     = ["CMD-SHELL", "python -c \"import urllib.request; urllib.request.urlopen('http://localhost:${each.value.port}${each.value.health_path}')\""]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])

  tags = local.common_tags
}

resource "aws_lb_target_group" "services" {
  for_each = local.enable_alb ? local.services : {}

  name        = substr("${local.name_prefix}-${each.key}", 0, 32)
  port        = each.value.port
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    path                = each.value.health_path
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    matcher             = "200"
  }

  tags = local.common_tags
}

resource "aws_ecs_service" "services" {
  for_each = local.services

  name            = each.key
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.services[each.key].arn
  desired_count   = local.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }

  dynamic "load_balancer" {
    for_each = local.enable_alb ? [1] : []
    content {
      target_group_arn = aws_lb_target_group.services[each.key].arn
      container_name   = each.key
      container_port   = each.value.port
    }
  }

  service_registries {
    registry_arn = aws_service_discovery_service.services[each.key].arn
  }

  tags = local.common_tags
}
