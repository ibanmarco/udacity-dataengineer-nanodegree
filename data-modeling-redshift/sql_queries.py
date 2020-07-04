import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES
staging_events_table_create = ("""
CREATE TABLE staging_events (
    artist VARCHAR,
    auth VARCHAR,
    first_name VARCHAR,
    gender CHAR,
    session_item INT,
    last_name VARCHAR,
    length FLOAT,
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration BIGINT,
    session_id INT,
    song VARCHAR ,
    status INT,
    ts BIGINT,
    user_agent VARCHAR,
    user_id INT
);
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs (
    artist_id VARCHAR,
    artist_location VARCHAR,
    artist_latitude FLOAT,
    artist_longitude FLOAT,
    artist_name VARCHAR,
    duration FLOAT,
    num_songs INT,
    song_id VARCHAR,
    title VARCHAR,
    year INT
);
""")

songplay_table_create = ("""
CREATE TABLE songplays (
    songplay_id INT IDENTITY(0, 1) NOT NULL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    user_id VARCHAR NOT NULL,
    level VARCHAR NOT NULL,
    song_id VARCHAR NOT NULL,
    artist_id VARCHAR NOT NULL,
    session_id INT,
    location VARCHAR,
    user_agent VARCHAR
);
""")

user_table_create = ("""
CREATE TABLE users (
    user_id VARCHAR NOT NULL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    gender CHAR,
    level VARCHAR NOT NULL
);
""")

song_table_create = ("""
CREATE TABLE songs (
    song_id VARCHAR NOT NULL PRIMARY KEY,
    title VARCHAR NOT NULL,
    artist_id VARCHAR NOT NULL,
    year INT,
    duration INT
);
""")

artist_table_create = ("""
CREATE TABLE artists (
    artist_id VARCHAR NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL,
    location VARCHAR,
    latitude FLOAT,
    longitude FLOAT
);
""")

time_table_create = ("""
CREATE TABLE time (
    start_time TIMESTAMP NOT NULL PRIMARY KEY,
    hour INT NOT NULL,
    day INT NOT NULL,
    week INT NOT NULL,
    month INT NOT NULL,
    year INT NOT NULL,
    weekday INT NOT NULL
);
""")

# STAGING TABLES
staging_events_copy = (f"""
    COPY staging_events
    FROM {config.get('S3', 'LOG_DATA')}
    IAM_ROLE {config.get('IAM_SEC', 'REDSHIFT_ROLE_ARN')}
    JSON {config.get('S3', 'LOG_JSONPATH')};
""")

staging_songs_copy = (f"""
    COPY staging_songs
    FROM {config.get('S3', 'SONG_DATA')}
    IAM_ROLE {config.get('IAM_SEC', 'REDSHIFT_ROLE_ARN')}
    FORMAT AS JSON 'auto';
""")


# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT TIMESTAMP 'epoch' + (ts / 1000) * INTERVAL '1 Second ',
    user_id,
    level,
    song_id,
    artist_id,
    session_id,
    location,
    user_agent
FROM staging_events se
JOIN staging_songs ss ON (se.song = ss.title AND se.artist = ss.artist_name)
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT (user_id),
    first_name,
    last_name,
    gender,
    level
FROM staging_events
WHERE user_id IS NOT NULL;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT DISTINCT(song_id),
    title,
    artist_id,
    year,
    duration
FROM staging_songs;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT DISTINCT (artist_id),
    artist_name,
    artist_location,
    artist_latitude,
    artist_longitude
FROM staging_songs
WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT (TIMESTAMP 'epoch' + (ts / 1000) * INTERVAL '1 Second ') as ts_timestamp,
    EXTRACT(HOUR FROM ts_timestamp),
    EXTRACT(DAY FROM ts_timestamp),
    EXTRACT(WEEK FROM ts_timestamp),
    EXTRACT(MONTH FROM ts_timestamp),
    EXTRACT(YEAR FROM ts_timestamp),
    EXTRACT(DOW FROM ts_timestamp)
FROM staging_events;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
