# Contract module: port + health path. Cheap resource = log group.
# Do not create aws_lb or aws_ecs_service (BUILD-1101 / COST-1105).

resource "aws_cloudwatch_log_group" "this" {
  name              = "/ecs/${var.name}"
  retention_in_days = 7
  tags              = var.tags
}
