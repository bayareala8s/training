output "vpc_id" {
  value = module.vpc.vpc_id
}

output "lab_instance_id" {
  value = try(module.compute[0].instance_id, null)
}
