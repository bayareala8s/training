# BUILD-1202 work — AEJE-D-055. Pass port and liveness explicitly (teaching).
# Image is not :latest. No ALB / Fargate service in this root.

locals {
  extra_tags = {
    Course      = "AEJE"
    Module      = "12"
    Lab         = "BUILD-1202"
    Environment = "student"
  }
}

module "ecr" {
  source = "./modules/ecr"
  name   = var.repository_name
  region = var.region
  tags   = local.extra_tags
}

module "ecs_service" {
  source            = "./modules/ecs_service"
  name              = var.service_name
  region            = var.region
  container_port    = 8080
  health_check_path = "/actuator/health/liveness"
  image             = var.container_image
  tags              = local.extra_tags
}
