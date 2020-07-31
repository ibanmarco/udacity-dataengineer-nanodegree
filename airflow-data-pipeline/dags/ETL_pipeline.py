# import os
import logging
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

# Importing AWS secret and key ids are not required
# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'Iban Marco',
    # 'start_date': datetime(2019, 1, 12),
    'start_date': datetime.utcnow(),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}

aws_config = {
    'aws_credentials_id': "aws_credentials",
    'redshift_endpoint': "redshift_endpoint",
    's3_bucket': "udacity-dend",
    'events_s3_key': "log_data",
    'songs_s3_key': "song_data",
    'stage_events_table': "staging_events",
    'stage_songs_table': "staging_songs",
    'songplays_table': "songplays",
    'users_table': "users",
    'songs_table': "songs",
    'artists_table': "artists",
    'time_table': "time"
}

check_queries =  [
    {
        "query": "SELECT COUNT(*) FROM staging_events;",
        "op": "ne",
        "val": 0
    },
    {
        "query": "SELECT COUNT(*) FROM staging_songs;",
        "op": "ne",
        "val": 0
    },
    {
        "query": "SELECT COUNT(*) FROM songplays;",
        "op": "ne",
        "val": 0
    },
    {
        "query": "SELECT COUNT(*) FROM users;",
        "op": "ne",
        "val": 0
    },
    {
        "query": "SELECT COUNT(*) FROM songs;",
        "op": "ne",
        "val": 0
    },
    {
        "query": "SELECT COUNT(*) FROM artists;",
        "op": "gt",
        "val": 0
    },
    {
        "query": "SELECT COUNT(*) FROM time;",
        "op": "gt",
        "val": 0
    }
]

dag = DAG('ETL_pipeline',
          default_args = default_args,
          description = 'Load and transform data in Redshift with Airflow',
          schedule_interval = '0 * * * *'
        )

start_operator = DummyOperator(
    task_id = 'Begin_execution',
    dag = dag
)

create_tables = PostgresOperator(
    task_id = 'Create_tables',
    dag = dag,
    postgres_conn_id = aws_config['redshift_endpoint'],
    sql = [
        SqlQueries.staging_events_table_create,
        SqlQueries.staging_songs_table_create,
        SqlQueries.songplays_table_create,
        SqlQueries.users_table_create,
        SqlQueries.songs_table_create,
        SqlQueries.artits_table_create,
        SqlQueries.time_table_create
    ]
)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id = 'Stage_events',
    dag = dag,
    aws_credentials_id = "aws_credentials",
    redshift_endpoint = aws_config['redshift_endpoint'],
    s3_path = f"s3://{aws_config['s3_bucket']}/{aws_config['events_s3_key']}",
    table = aws_config['stage_events_table'],
    copy_params = f"JSON 's3://{aws_config['s3_bucket']}/log_json_path.json'"
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id = 'Stage_songs',
    dag = dag,
    aws_credentials_id = "aws_credentials",
    redshift_endpoint = aws_config['redshift_endpoint'],
    s3_path = f"s3://{aws_config['s3_bucket']}/{aws_config['songs_s3_key']}",
    table = aws_config['stage_songs_table'],
    copy_params = "FORMAT AS JSON 'auto'"
)

load_songplays_table = LoadFactOperator(
    task_id = 'Load_songplays_fact_table',
    dag = dag,
    redshift_endpoint = aws_config['redshift_endpoint'],
    table = aws_config['songplays_table'],
    sql_query = SqlQueries.songplays_table_insert
)

load_user_dimension_table = LoadDimensionOperator(
    task_id = 'Load_user_dim_table',
    dag = dag,
    redshift_endpoint = aws_config['redshift_endpoint'],
    table = aws_config['users_table'],
    sql_query = SqlQueries.users_table_insert,
    truncate = True
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_endpoint = aws_config['redshift_endpoint'],
    table = aws_config['songs_table'],
    sql_query = SqlQueries.songs_table_insert,
    truncate = True
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_endpoint = aws_config['redshift_endpoint'],
    table = aws_config['artists_table'],
    sql_query = SqlQueries.artists_table_insert,
    truncate = True
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_endpoint = aws_config['redshift_endpoint'],
    table = aws_config['time_table'],
    sql_query = SqlQueries.time_table_insert,
    truncate = True
)

run_quality_checks = DataQualityOperator(
    task_id = 'Run_data_quality_checks',
    dag = dag,
    redshift_endpoint = aws_config['redshift_endpoint'],
    table = None,
    sql_queries = check_queries
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> create_tables
create_tables >> [stage_events_to_redshift, stage_songs_to_redshift]
[stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table
load_songplays_table >> [load_song_dimension_table, load_user_dimension_table, load_artist_dimension_table, load_time_dimension_table]
[load_song_dimension_table, load_user_dimension_table, load_artist_dimension_table, load_time_dimension_table] >> run_quality_checks
run_quality_checks >> end_operator
