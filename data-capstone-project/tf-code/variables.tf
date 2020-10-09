variable "aws_region" {
  type = string
}

variable "project" {
  type = string
}

variable "cidr_ssh" {
  type = string
}

variable "ec2_ami" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "private_subnet_id" {
  type = string
}

variable "public_subnet_id" {
  type = string
}

variable "ec2_instance_type" {
  type = string
}

###########################
variable "generic_kms" {
  type = string
}

variable "dbname" {
  type = string
}

variable "db_master_username" {
  type = string
}

#
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

variable "emr_release" {
  type = string
}

variable "worker_count" {
  type = string
}

variable "master_instance_type" {
  type = string
}

variable "core_instance_type" {
  type = string
}
