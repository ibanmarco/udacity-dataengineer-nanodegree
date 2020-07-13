# Data Modeling with AWS RedShift

## Introduction:

* A startup wants to analyze the data they've been collecting on songs and user activity on their new music streaming app.

* The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## Datasets:

Two datasets were used:

* Song dataset: It is really a subset that contains metadata about a song and the artist of that song.
* Log dataset: Log files simulating activity logs from a music streaming app.


## HowTo: AWS, Python scripts and Jupyter notebook

### Requirements:

The following Python packages were used:
```
ipython-sql
psycopg2
boto3
configparser

```

### AWS deployment:

A terraform module was created to deploy a RDS PostgreSQL instance and a RedShift cluster in private subnets. A bastion EC2 instance was created in order to access them and SSH tunneling was used to run python scripts and Jupyter notebook. You can find the module [here.](https://github.com/ibanmarco/tf-data-lake-aws

Review the `terraform.tfvars` file and fill the variables with the proper value before running terraform:

* First initialize a working directory:
```
terraform init
```

* Verify everything is fine running the plan:
```
terraform plan
```

* Apply terraform in `us-west-2` region:
```
terraform apply
```


### Python files and Jupyter Notebook:

Once the PostgreSQL server is up and reachable, follow these steps to run this project:

* Run `create_tables.py` manually. This process will create the fact and dimension tables for the star schema in Redshift

* Run `etl.py` manually to load data from S3 into staging tables on Redshift and then process that data into the analytics tables on Redshift.

* Verify the content of the tables using `test.ipynb`.


### Bonus:

You don't need to destroy all the terraform resources to reduce cost, only follow the following steps:

* Stop the RDS instance:
```
aws rds stop-db-instance --db-instance-identifier <YOUR_INSTANCE_ID> --region us-west-2
```

* Stop the EC2 instance:
```
aws ec2 stop-instances --instance-ids <YOUR_INSTANCE_ID> --region us-west-2
```

* Destroy the RedShift cluster:
```
terraform destroy --target=aws_redshift_cluster.redshift
```


To restart again:

* Start the RDS instance:
```
aws rds start-db-instance --db-instance-identifier  <YOUR_INSTANCE_ID> --region us-west-2
```

* Start the EC2 instance:
```
aws ec2 start-instances --instance-ids  <YOUR_INSTANCE_ID>--region us-west-2
```

* Create the RedShift cluster:
```
terraform apply --target=aws_redshift_cluster.redshift
```
