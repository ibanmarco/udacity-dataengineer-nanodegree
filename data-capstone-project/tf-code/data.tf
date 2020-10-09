data "aws_caller_identity" "current" {}

data "aws_vpc" "default_vpc" {
  id = var.vpc_id
}

data "aws_kms_key" "generic_kms" {
  key_id = var.generic_kms
}
