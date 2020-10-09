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

variable "ec2_ebs_optimized" {
  type    = bool
  default = false
}

variable "ec2_monitoring" {
  type    = bool
  default = true
}
