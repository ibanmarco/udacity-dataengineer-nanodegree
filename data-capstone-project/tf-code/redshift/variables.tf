variable "project" {
  type = string
}

variable "aws_account_id" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "kms_arn" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "dbname" {
  type = string
}

variable "db_master_username" {
  type = string
}

variable "bastion_private_ip" {
  type = string
}

variable "redshift_node_type" {
  type = string
}

variable "redshift_cluster_type" {
  type = string
}

variable "redshift_nodes" {
  type = string
}

variable "redshift_publicly_accessible" {
  type    = bool
  default = false
}

variable "redshift_skip_final_snapshot" {
  type    = bool
  default = true
}
