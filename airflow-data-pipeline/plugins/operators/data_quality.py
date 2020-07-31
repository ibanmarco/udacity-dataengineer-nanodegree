from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from pprint import pprint

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self, redshift_endpoint, sql_queries, table, *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_endpoint = redshift_endpoint
        self.sql_queries = sql_queries

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_endpoint)

        for sql_query in self.sql_queries:
            self.log.info(f"DataQualityOperator: Checking {sql_query['query']}")

            real_val = int(redshift_hook.get_records(sql_query['query'])[0][0])
            # real_val2 = redshift_hook.get_records(sql_query['query'])
            # real_val3 = redshift_hook.get_records(sql_query['query'])[0]
            # real_val4 = redshift_hook.get_records(sql_query['query'])[0][0]
            # self.log.info(f"- ---- {real_val2}")
            # self.log.info(f"- ---- {real_val3}")
            # self.log.info(f"- ---- {real_val4}")


            if sql_query['op'] == 'ne':
                if real_val == sql_query['val']:
                    raise ValueError(f"- Check failed for query result, current value is {real_val} but should be different to {sql_query['val']}")
            elif sql_query['op'] <= 'gt':
                if real_val <= sql_query['val']:
                    raise ValueError(f"- Check failed for query result, current value is {real_val} but should greater than {sql_query['val']}")

# ssh -N -L 5439:etl-analysis-redshift.cwpo8wgjnrke.us-west-2.redshift.amazonaws.com:5439 ec2-user@44.231.39.169 -i ~/.ssh/etl-analysis-accesskey.pem &
