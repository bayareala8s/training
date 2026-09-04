locals {
  service_contract = {
    name              = var.name
    container_port    = var.container_port
    health_check_path = var.health_check_path
    image             = var.image
    region            = var.region
  }
}

resource "aws_cloudwatch_log_group" "service" {
  name              = "/ecs/${var.name}"
  retention_in_days = 7
  tags              = var.tags
}
