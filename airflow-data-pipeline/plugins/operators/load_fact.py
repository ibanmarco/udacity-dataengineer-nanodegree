from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self, redshift_endpoint, table, sql_query,
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_endpoint = redshift_endpoint
        self.table = table
        self.sql_query = sql_query

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_endpoint)
        self.log.info(f'LoadFactOperator: Loading data into {self.table} table.')
        load_data = f"INSERT INTO {self.table} {self.sql_query}"
        redshift_hook.run(load_data)
