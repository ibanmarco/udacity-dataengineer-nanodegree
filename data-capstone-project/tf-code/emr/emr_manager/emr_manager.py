import os, boto3, botocore
from botocore.exceptions import ClientError
from pprint import pprint


def create_emr_cluster(aws_region, s3_bucket_name, filename)
    # EMR transient cluster will be created to perform the ETL pipeline

    try:
        cluster_name = f"{int(datetime.datetime.now().timestamp())}-EMR-cluster"
        aws_region_name = os.environ['aws_region_name']
        key_name = os.environ['key_name']
        emr_release = os.environ['emr_release']
        worker_count = os.environ['worker_count']
        master_instance_type = os.environ['master_instance_type']
        core_instance_type = os.environ['core_instance_type']
        aws_region_name = os.environ['aws_region_name']
        postgresql_endpoint = os.environ['postgresql_endpoint']
        postgresql_endpoint = os.environ['postgresql_endpoint']
        etl_pipeline = f"s3://{s3_bucket_name}/{filename}"
        emr_ec2_role_name     =  os.environ['emr_ec2_role_name']
        emr_service_role_name =  os.environ['emr_service_role_name']

        emr_client = boto3.client('emr', region_name=aws_region_name)

        response = emr_client.run_job_flow(
            Name=cluster_name,
            LogUri=f"s3://{s3_bucket_name}/EMRlogs",
            ReleaseLabel=emr_release,
            Instances={
                'MasterInstanceType': master_instance_type,
                'SlaveInstanceType': 'core_instance_type,
                'InstanceGroups': [
                    {
                        'Name': 'Master Node',
                        'Market': 'ON_DEMAND',
                        'InstanceRole': 'MASTER',
                        # 'BidPrice': 'string',
                        'InstanceType': master_instance_type
                    },
                    {
                        'Name': 'Core Node',
                        'Market': 'ON_DEMAND',
                        'InstanceRole': 'CORE',
                        'InstanceType': core_instance_type,
                        'InstanceCount': worker_count
                    },
                ],
                'Ec2KeyName': key_name,
                'KeepJobFlowAliveWhenNoSteps': False,
                'TerminationProtected': False,
                # 'Ec2SubnetId': 'string',
                # 'EmrManagedMasterSecurityGroup': 'string',
                # 'EmrManagedSlaveSecurityGroup': 'string',
                # 'ServiceAccessSecurityGroup': 'string',
            },
            Steps=[
                {
                    'Name': 'Setup Debugging',
                    'ActionOnFailure': 'TERMINATE_CLUSTER',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['state-pusher-script']
                    }
                },
                {
                    'Name': 'Get ETL python file from S3',
                    'ActionOnFailure': 'CANCEL_AND_WAIT',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['aws', 's3', 'cp', f"s3://{s3_bucket_name}/{filename}", '/home/hadoop/']
                    }
                },
                {
                    'Name': 'Run Spark',
                    'ActionOnFailure': 'CANCEL_AND_WAIT',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['spark-submit', f"/home/hadoop/{filename.split("/")[1]}"]
                    }
                }
                ],
            BootstrapActions=[
                {
                    'Name': 'Bootstrap action',
                    'ScriptBootstrapAction': {
                        'Path': f"s3://{s3_bucket_name}/scripts/bootstrap_actions1.sh",
                    }
                },
            ],
            Applications=[
                {
                    'Name': 'Spark'
                },
            ],
            Configurations=[
                {
                    'Classification': 'string',
                    'Configurations': {'... recursive ...'},
                    'Properties': {
                        'string': 'string'
                    }
                },
                {
                    "Classification": "spark-env",
                    "Configurations": [
                        {
                            "Classification": "export",
                            "Properties": {
                                # "PYSPARK_DRIVER_PYTHON": "python3",
                                "PYSPARK_PYTHON": "/usr/bin/python3"
                            }
                        }
                    ]
                }
            ],
            ],
            VisibleToAllUsers=True,
            JobFlowRole=emr_ec2_role_name,
            ServiceRole=emr_service_role_name,
            # CustomAmiId='string'
        )

         print(f"Created EMR cluster {repoonse['JobFlowId']} with {response['ClusterArn']}", end='')

    except Exception as e:
        print(e)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

def lambda_handler(event, context):
    try:
        # pprint(event)

        s3_bucket_name = event['Records'][0]['s3']['bucket']['name']
        filename =  event['Records'][0]['s3']['object']['key']

        create_emr_cluster(os.environ, s3_bucket_name, filename)

    except Exception as e:
        print(e)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
