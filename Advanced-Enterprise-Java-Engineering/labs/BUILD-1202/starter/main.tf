# BUILD-1202 starter — call finished modules with port 8080 and the liveness path.
# The child modules are hollow. Do not push :latest.

module "ecr" {
  source = "./modules/ecr"
  name   = var.repository_name
  region = var.region
}

module "ecs_service" {
  source = "./modules/ecs_service"
  name   = var.service_name
  region = var.region
}
