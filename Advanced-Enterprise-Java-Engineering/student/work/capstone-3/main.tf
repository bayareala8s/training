# CAPSTONE-3 composition — BUILD-1202 modules + ACCOUNT.md contracts.
# No live aws_ecs_service / aws_lb here (BUILD-1202 postponed those).
# ALB health + Fargate 256/512 live in locals.alb_contract and labs/BUILD-1101/work/.
# Image is not :latest. No NAT / EKS / RDS.

locals {
  extra_tags = {
    Course      = "AEJE"
    Module      = "Capstone"
    Lab         = "CAPSTONE-3"
    Environment = "student"
  }

  alb_contract = {
    health_check_path   = "/actuator/health/liveness"
    health_check_port   = 8080
    matcher             = "200"
    container_port      = 8080
    fargate_cpu         = "256"
    fargate_memory      = "512"
    desired_count       = 1
    assign_public_ip    = true
    subnets             = "two public + IGW"
    apply_shape_pointer = "labs/BUILD-1101/work/"
    refused             = ["NAT Gateway", "EKS", "RDS", "RDS Multi-AZ", "second ALB"]
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
