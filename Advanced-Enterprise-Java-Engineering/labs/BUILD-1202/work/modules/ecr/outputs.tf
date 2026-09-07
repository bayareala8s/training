output "repository_url" {
  description = "Push an immutable tag here. Never :latest."
  value       = aws_ecr_repository.this.repository_url
}

output "repository_arn" {
  value = aws_ecr_repository.this.arn
}
