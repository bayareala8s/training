output "cluster_name" {
  value = aws_eks_cluster.lab.name
}

output "cluster_endpoint" {
  value = aws_eks_cluster.lab.endpoint
}

output "node_group_name" {
  value = aws_eks_node_group.lab.node_group_name
}

output "shared_rds_endpoint" {
  description = "Same private hostname the ECS tasks use."
  value       = data.terraform_remote_state.ecs.outputs.db_endpoint
}

output "shared_ecr_repository_url" {
  description = "Same image repository as the ECS lab. Never :latest."
  value       = data.terraform_remote_state.ecs.outputs.ecr_repository_url
}

output "shared_secret_arn" {
  value = data.terraform_remote_state.ecs.outputs.secret_arn
}

output "kubeconfig_command" {
  value = "aws eks update-kubeconfig --region ${var.region} --name ${aws_eks_cluster.lab.name}"
}
