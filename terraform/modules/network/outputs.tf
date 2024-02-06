output "private_subnet_ids" {
  value = [for value in aws_subnet.private : value.id]
}

output "security_group_ids" {
  value = [aws_security_group.allow_postgres.id]
}
