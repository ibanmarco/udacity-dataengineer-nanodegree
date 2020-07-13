
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofmonth, hour, weekofyear, dayofweek,date_format, to_timestamp, monotonically_increasing_id


def create_spark_session():
    """
    Creates the Spark session supporting S3 bucket
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Gets log_data dataset from S3 bucket, extracts data and creates songs_table and artists_table by using Spark Core
    and save the dataframes in parquet format in the S3 bucket
    """
    # read song data file
    df = spark.read.json(f"{input_data}song_data/*/*/*/*.json")

    # extract columns to create songs table
    songs_table = df.select('song_id', 'title', 'artist_id', 'year', 'duration').where(df.song_id.isNotNull()).drop_duplicates()

    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode('overwrite').partitionBy("year", "artist_id").parquet(f"{output_data}/songs_table/")

    # extract columns to create artists table
    artists_table = df.select('artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude').where(df.artist_id.isNotNull()). \
        drop_duplicates()

    # write artists table to parquet files
    artists_table.write.mode('overwrite').parquet(f"{output_data}/artists_table/")


def process_log_data(spark, input_data, output_data):
    """
    Gets log_data dataset from S3 bucket, extracts data and creates users_table, time_table and songplays_table by using Spark Core
    and save the dataframes in parquet format in the S3 bucket
    """
    # read log data file
    df = spark.read.json(f"{input_data}log_data/*/*/*.json")

    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table
    users_table = df.select(col('userId').alias('user_id'), col('firstName').alias('first_name'), col('lastName').alias('last_name'), 'gender', 'level'). \
        where(df.userId.isNotNull()).drop_duplicates(subset=['user_id'])

    # write users table to parquet files
    users_table.write.mode('overwrite').parquet(f"{output_data}/users_table/")

    # extract columns to create time table
    tdf = df.withColumn('start_time', to_timestamp(df.ts/1000)).select('start_time').where(df.ts.isNotNull())
    time_table = tdf.select('start_time', hour(tdf.start_time).alias('hour'), dayofmonth(tdf.start_time).alias('day'), \
        weekofyear(tdf.start_time).alias('week'), month(tdf.start_time).alias('month'), year(tdf.start_time).alias('year'), dayofweek(tdf.start_time).alias('weekday')). \
        drop_duplicates()

    # write time table to parquet files partitioned by year and month
    time_table.write.mode('overwrite').partitionBy("year", "month").parquet(f"{output_data}/time_table/")

    # read in song data to use for songplays table
    song_df = spark.read.json(f"{input_data}song_data/*/*/*/*.json")

    # extract columns from joined song and log datasets to create songplays table
    songplays_table = df.join(song_df, df.song == song_df.title, 'inner'). \
        select(monotonically_increasing_id().alias('songplay_id'), to_timestamp(df.ts/1000).alias('start_time'), \
        df.userId.alias('user_id'), df.level, song_df.song_id, song_df.artist_id, df.sessionId.alias('session_id'), \
        df.location, df.userAgent.alias('user_agent'), year(to_timestamp(df.ts/1000)).alias('year'), month(to_timestamp(df.ts/1000)).alias('month')). \
        drop_duplicates()

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy('year', 'month').parquet(f"{output_data}/songplays_table/")


def main():
    """
    Main function where other functions are called.
    """
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://etl-analysis-bucket/outputs/"

    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
