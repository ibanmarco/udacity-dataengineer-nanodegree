import configparser
import psycopg2
import boto3
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    print(f"Loading Staging tables...")
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    print(f"Inserting Staging tables...")
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

        
def get_redshift_password():
    ssm_client = boto3.client('ssm', region_name='us-west-2')
    
    response = ssm_client.get_parameter(
        Name='ETL-Analysis-redshift_dbpassword',
        WithDecryption=True
    )['Parameter']
    
    return response['Value']
    
    
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} port={} password={}".format(*config['CLUSTER'].values(), get_redshift_password()))
    
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()