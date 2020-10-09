aws_region        = "us-west-2"
project           = "ETL-Analysis"
cidr_ssh          = ""
ec2_ami           = ""
vpc_id            = ""
private_subnet_id = ""
public_subnet_id  = ""
ec2_instance_type = "t2.micro"
generic_kms       = "alias/generic_key"

# RedShift
dbname                    = "etldb"
db_master_username        = "admindb"
redshift_node_type        = "dc2.large"
redshift_cluster_type     = "multi-node"
redshift_nodes            = "2"

# EMR
emr_release          = "emr-5.30.1"
worker_count         = "1"
master_instance_type = " m5.xlarge"
core_instance_type   = " m5.xlarge"
