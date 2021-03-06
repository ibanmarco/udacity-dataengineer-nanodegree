# Udacity Data Engineer Nanodegree Submissions

This is the repository where all the projects related to [Data Engineer Nanodegree](https://www.udacity.com/course/data-engineer-nanodegree--nd027) resides.

## [Data Modeling with SQL: PostgreSQL](./data-modeling-postgres)
* Modeling user activity data for a music streaming app.
* Creating a Postgres database schema with fact and dimension tables designed to optimize queries on song play analysis and database normalization.
* Creating an ETL pipeline for the analysis and testing the database and ETL pipeline by running queries.


## [Data Modeling with SQL: Cassandra](./data-modeling-cassandra)
* Modeling user activity data for a music streaming app.
* Creating a NoSQL database schema on Apache Cassandra.
* Creating an ETL pipeline for the analysis and testing the database and ETL pipeline by running queries.


## [Data Modeling with AWS RedShift](./data-modeling-redshift)
* Deploying a RDS PostgreSQL and RedShift cluster for ETL by using IaC.
* Building an ETL pipeline up that extracts the data from S3, stages them in Redshift, and transforms data into a set of dimensional tables stored in RDS PostgreSQL.
* Creating a optimized star schema optimized for queries

#### Bonus
A terraform module was created to deploy a RDS PostgreSQL instance and a RedShift cluster in private subnets and both of them can be reachable from your laptop without being exposed to internet. You can find the module [here.](https://github.com/ibanmarco/tf-data-lake-aws)


## [Data Lake with AWS ElasticMapReduce (EMR) - Spark](./data-lake-aws)
* Deploying the AWS infra for ETL by using IaC.
* In the event of uploading the ETL pipeline to the S3 bucket a lambda is invoked in order to create a transient EMR cluster where the ETL pipeline is executed.
* Data is processed on Spark and outputs saved in S3 bucket.

#### Bonus
The previous terraform module was refactored in modules in order to deploy the required AWS resources. You can find the module [here.](https://github.com/ibanmarco/tf-data-lake-aws)


## [Data Pipelines with Apache Airflow](./airflow-data-pipeline)
* Creating data pipeline to automate ETL by using Apache Airflow
* Custom operators and a helpers class that contains all the SQL transformations will be executed to get JSON files from S3 and keep data in RedShift.
