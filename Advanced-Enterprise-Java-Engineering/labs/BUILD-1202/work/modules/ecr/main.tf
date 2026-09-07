resource "aws_ecr_repository" "this" {
  name                 = var.name
  image_tag_mutability = "IMMUTABLE"
  force_delete         = true
  tags                 = var.tags

  image_scanning_configuration {
    scan_on_push = true
  }
}
