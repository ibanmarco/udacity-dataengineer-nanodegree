variable "aws_region" {
  type = string
}

variable "project" {
  type = string
}

variable "etl_bucket_name" {
  type = string
}

variable "etl_bucket_arn" {
  type = string
}

variable "postgresql_endpoint" {
  type = string
}

variable "redshift_endpoint" {
  type = string
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
