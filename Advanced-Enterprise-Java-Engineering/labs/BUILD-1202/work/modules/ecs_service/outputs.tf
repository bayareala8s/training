output "container_port" {
  value = var.container_port
}

output "health_check_path" {
  value = var.health_check_path
}

output "log_group_name" {
  value = aws_cloudwatch_log_group.this.name
}

output "service_contract" {
  description = "Reviewer-readable contract without opening main.tf."
  value = {
    name              = var.name
    container_port    = var.container_port
    health_check_path = var.health_check_path
    image             = var.image
    log_group_name    = aws_cloudwatch_log_group.this.name
    region            = var.region
  }
}
