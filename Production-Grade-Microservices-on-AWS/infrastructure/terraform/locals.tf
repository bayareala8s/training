locals {
  name_prefix = "${var.project_name}-${var.environment}"
  active      = var.platform_active

  desired_count = local.active ? var.ecs_desired_count : 0
  enable_nat    = local.active
  enable_alb    = local.active

  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    Course      = "production-microservices-aws"
    ManagedBy   = "terraform"
    Active      = tostring(local.active)
  }

  services = {
    user-service = {
      port           = 8001
      cpu            = 256
      memory         = 512
      path_patterns  = ["/users*", "/auth*"]
      health_path    = "/health"
      extra_env      = {}
    }
    product-service = {
      port           = 8002
      cpu            = 256
      memory         = 512
      path_patterns  = ["/products*"]
      health_path    = "/health"
      extra_env      = {}
    }
    order-service = {
      port          = 8003
      cpu           = 256
      memory        = 512
      path_patterns = ["/orders*"]
      health_path   = "/health"
      extra_env     = {}
    }
    notification-service = {
      port           = 8004
      cpu            = 256
      memory         = 512
      path_patterns  = ["/events*"]
      health_path    = "/health"
      extra_env      = {}
    }
  }

  service_discovery_namespace = "${local.name_prefix}.local"

  # Route inter-service HTTP via ALB when active (more reliable than Cloud Map in Fargate labs)
  product_service_url = local.enable_alb ? "http://${aws_lb.main[0].dns_name}" : "http://product-service.${local.service_discovery_namespace}:${local.services["product-service"].port}"
  event_http_endpoint = local.enable_alb ? "http://${aws_lb.main[0].dns_name}/events" : "http://notification-service.${local.service_discovery_namespace}:${local.services["notification-service"].port}/events"
}
