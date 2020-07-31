from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self, aws_credentials_id, redshift_endpoint,
                 s3_path, table, copy_params, *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.aws_credentials_id = aws_credentials_id
        self.redshift_endpoint = redshift_endpoint
        self.s3_path = s3_path
        self.table = table
        self.copy_params = copy_params

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift_hook = PostgresHook(self.redshift_endpoint)

        copy_data = f"""
                    COPY {self.table}
                    FROM '{self.s3_path}'
                    ACCESS_KEY_ID '{credentials.access_key}'
                    SECRET_ACCESS_KEY '{credentials.secret_key}'
                    {self.copy_params};
                """

        self.log.info(f'StageToRedshiftOperator: Copying datasets from {self.s3_path} to {self.table} table.')
        redshift_hook.run(copy_data)
