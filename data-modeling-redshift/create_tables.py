import configparser
import psycopg2
import boto3
from sql_queries import create_table_queries, drop_table_queries


def get_redshift_password():
    ssm_client = boto3.client('ssm', region_name='us-west-2')
    
    print("Getting the authentication details from SSM...")
    
    response= ssm_client.get_parameter(
        Name='ETL-Analysis-redshift_dbpassword',
        WithDecryption=True
    )['Parameter']

    return response['Value']


def drop_tables(cur, conn):
    
    print("Dropping tables...")
    
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    print("Creating tables...")
    
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

        
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} port={} password={}".format(*config['CLUSTER'].values(), get_redshift_password()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()