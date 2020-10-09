module "bastion" {
  source            = "./bastion"
  project           = var.project
  cidr_ssh          = var.cidr_ssh
  ec2_ami           = var.ec2_ami
  vpc_id            = var.vpc_id
  private_subnet_id = var.private_subnet_id
  public_subnet_id  = var.public_subnet_id
  ec2_instance_type = var.ec2_instance_type
}

module "s3_bucket" {
  source     = "./s3_bucket"
  project    = "${var.project}"
  aws_region = "${var.aws_region}"
}

module "rds" {
  source                    = "./rds"
  project                   = var.project
  kms_arn                   = data.aws_kms_key.generic_kms.arn
  vpc_id                    = var.vpc_id
  bastion_private_ip        = module.bastion.bastion_private_ip
  rds_instance_class        = var.rds_instance_class
  rds_storage_type          = var.rds_storage_type
  rds_allocated_storage     = var.rds_allocated_storage
  rds_max_allocated_storage = var.rds_max_allocated_storage
  dbname                    = var.dbname
  db_master_username        = var.db_master_username
}

module "redshift" {
  source                = "./redshift"
  project               = var.project
  aws_region            = var.aws_region
  kms_arn               = data.aws_kms_key.generic_kms.arn
  vpc_id                = var.vpc_id
  bastion_private_ip    = module.bastion.bastion_private_ip
  aws_account_id        = data.aws_caller_identity.current.account_id
  dbname                = var.dbname
  db_master_username    = var.db_master_username
  redshift_node_type    = var.redshift_node_type
  redshift_cluster_type = var.redshift_cluster_type
  redshift_nodes        = var.redshift_nodes
}

module "emr" {
  source               = "./emr"
  project              = var.project
  aws_region           = var.aws_region
  etl_bucket_name      = module.s3_bucket.etl_bucket_name
  etl_bucket_arn       = module.s3_bucket.etl_bucket_arn
  postgresql_endpoint  = "postgresql_endpoint" # module.rds.rds_postgresql_endpoint
  redshift_endpoint    = "redshift_endpoint"   #module.redshift.redshift_endpoint
  emr_release          = var.emr_release
  worker_count         = var.worker_count
  master_instance_type = var.master_instance_type
  core_instance_type   = var.core_instance_type

}
