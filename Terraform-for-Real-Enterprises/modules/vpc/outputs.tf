output "vpc_id" {
  value = aws_vpc.this.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

output "vpc_cidr" {
  value = aws_vpc.this.cidr_block
}

output "nat_instance_id" {
  value       = try(aws_instance.nat[0].id, null)
  description = "NAT EC2 instance ID if using NAT instance mode"
}
