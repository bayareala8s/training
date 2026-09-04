module "ecr" {
  source = "./modules/ecr"
  name   = var.repository_name
  region = var.region
  tags = {
    Course = "AEJE"
    Lab    = "BUILD-1202"
  }
}

module "ecs_service" {
  source            = "./modules/ecs_service"
  name              = var.service_name
  region            = var.region
  container_port    = var.container_port
  health_check_path = var.health_check_path
  image             = "${module.ecr.repository_url}:pinned-not-latest"
  tags = {
    Course = "AEJE"
    Lab    = "BUILD-1202"
  }
}
