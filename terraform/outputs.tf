output "db_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.jac_learning_db.endpoint
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.jac_learning_vpc.id
}

output "public_subnet_id" {
  description = "Public subnet ID"
  value       = aws_subnet.public_subnet.id
}
