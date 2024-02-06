output "user_pool_id" {
  value = module.cognito.user_pool_id
}

output "user_pool_client_id" {
  value = module.cognito.user_pool_client_id
}


output "private_subnet_ids" {
  value = module.network.private_subnet_ids
}

output "security_group_ids" {
  value = module.network.security_group_ids
}
