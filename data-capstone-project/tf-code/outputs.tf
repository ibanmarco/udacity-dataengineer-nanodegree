output "bastion_public_ip" {
  value = module.bastion.bastion_public_ip
}

output "bastion_private_ip" {
  value = module.bastion.bastion_private_ip
}

output "bastion_id" {
  value = module.bastion.bastion_id
}

output "rds_postgresql_endpoint" {
  value = module.rds.rds_postgresql_endpoint
}

output "redshift_role_name" {
  value = module.redshift.redshift_role_name
}

output "redshift_role_arn" {
  value = module.redshift.redshift_role_arn
}

output "redshift_sg_id" {
  value = module.redshift.redshift_sg_id
}

output "redshift_endpoint" {
  value = module.redshift.redshift_endpoint
}
