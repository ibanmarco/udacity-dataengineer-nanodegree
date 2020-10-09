# AWS Data Lake with Redshift and EMR

This module creates a private Redshift cluster only reachable from a bastion host. It doesn't create either additional VPCs therefore it requires to define the proper `vpc_id` and `subnet_id` to integrate it with your current infrastructure. The security groups have been configured in order to access to PostgreSQL and RedShift via SSH tunneling from your own laptop.

In addition to RedShift, this module will create a transient EMR cluster through a Lambda once an ETL pipeline is uploaded to the S3 bucket.

## Variables:

| Name | Description | Type |
|------|-------------|:----:|
| aws_region | The aws region | string |
| cidr_ssh | Your public IP address in CIDR notation | string |
| core_instance_type | The EC2 instance type of the core node | string |
| db_master_username | Username for the master DB user | string |
| dbname | The name of the default database | string |
| ec2_ami | EC2 AMI Id | string |
| ec2_ebs_optimized | Flag that sets if the launched EC2 instance will be EBS-optimized | string |
| ec2_instance_type | The type of instance to start. Updates to this field will trigger a stop/start of the EC2 instance. | string |
| ec2_monitoring |  If true, the launched EC2 instance will have detailed monitoring enabled. | string |
| emr_release | The release label for the Amazon EMR release | string |
| generic_kms | Id of the KMS | string |
| master_instance_type | The EC2 instance type of the master node | string |
| project | Name of my project :-) | string |
| redshift_cluster_type | The cluster type to use. Either single-node or multi-node. | string |
| redshift_node_type | The type of nodes in the cluster | string |
| redshift_nodes | The number of the nodes in the cluster | string |
| redshift_publicly_accessible | If the cluster can be accessed from a public network | string |
| redshift_skip_final_snapshot | Determines whether a final snapshot of the cluster is created before Amazon Redshift deletes the cluster. | string |
| subnet_id | The subnet Id assgined to the EC2 instance | string |
| vpc_id | The VPC Id | string |
| worker_count | Number of core nodes | string |


## Outputs:

| Name | Description |
|------|-------------|
| bastion_id | Bastion host instance id |
| bastion_ip | Public IP address assigned to bastion host |
| redshift_endpoint | The connection endpoint |
| redshift_role_arn | The IAM Role ARN associated with the cluster  |
| redshift_role_name | The IAM Role name associated with the cluster |
| redshift_sg_id | Id of the security group assigned to Redshift |
