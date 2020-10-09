output "redshift_role_name" {
  value = aws_iam_role.etl_redshift.name
}

output "redshift_role_arn" {
  value = aws_iam_role.etl_redshift.arn
}

output "redshift_sg_id" {
  value = aws_security_group.redshift_sg.id
}

output "redshift_endpoint" {
  value = aws_redshift_cluster.redshift.endpoint
}
