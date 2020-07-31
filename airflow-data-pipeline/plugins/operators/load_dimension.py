from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self, redshift_endpoint, table, sql_query,
                 truncate = False, *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_endpoint = redshift_endpoint
        self.table = table
        self.sql_query = sql_query
        self.truncate = truncate

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_endpoint)

        if self.truncate:
            self.log.info(f'LoadDimensionOperator: Truncating {self.table}')
            redshift_hook.run(f"DELETE FROM {self.table};")

        self.log.info(f'LoadDimensionOperator: Loading data into {self.table} table.')
        load_data = f"INSERT INTO {self.table} {self.sql_query}"
        redshift_hook.run(load_data)
