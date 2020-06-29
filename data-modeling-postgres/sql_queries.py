# DROP TABLES

songplay_table_drop = "DROP table IF EXISTS songplays"
user_table_drop = "DROP table IF EXISTS users"
song_table_drop = "DROP table IF EXISTS songs"
artist_table_drop = "DROP table IF EXISTS artists"
time_table_drop = "DROP table IF EXISTS time"


# CREATE TABLES
'''
Fact Table
    songplays - records in log data associated with song plays i.e. records with page NextSong
    songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

Dimension Tables
    users - users in the app
    user_id, first_name, last_name, gender, level

    songs - songs in music database
    song_id, title, artist_id, year, duration

    artists - artists in music database
    artist_id, name, location, latitude, longitude

    time - timestamps of records in songplays broken down into specific units
    start_time, hour, day, week, month, year, weekday
'''

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (
      songplay_id           INTEGER PRIMARY KEY,
      start_time            TIMESTAMP NOT NULL,
      user_id               INTEGER NOT NULL,
      level                 VARCHAR(30) NOT NULL,
      song_id               VARCHAR(30) NOT NULL,
      artist_id             VARCHAR(30) NOT NULL,
      session_id            INTEGER,
      location              VARCHAR(128) NOT NULL,
      user_agent            VARCHAR(256) NOT NULL
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    (
      user_id               INTEGER PRIMARY KEY,
      first_name            VARCHAR(30) NOT NULL,
      last_name             VARCHAR(30) NOT NULL,
      gender                VARCHAR(30) NOT NULL,
      level                 VARCHAR(30) NOT NULL
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs
    (
      song_id               VARCHAR(128) PRIMARY KEY,
      title                 VARCHAR(128) NOT NULL,
      artist_id             VARCHAR(128) NOT NULL,
      year                  SMALLINT NOT NULL,
      duration              FLOAT(12) NOT NULL
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists
    (
      artist_id            VARCHAR(128) PRIMARY KEY,
      name                 VARCHAR(128) NOT NULL,
      location             VARCHAR(128) NOT NULL,
      latitude             FLOAT(8) NOT NULL,
      longitude            FLOAT(8) NOT NULL
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time
    (
      start_time           TIMESTAMP PRIMARY KEY,
      hour                 INTEGER NOT NULL,
      day                  INTEGER NOT NULL,
      week                 INTEGER NOT NULL,
      month                INTEGER NOT NULL,
      year                 INTEGER NOT NULL,
      weekday              INTEGER NOT NULL
    );
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (songplay_id) DO UPDATE SET level=EXCLUDED.level;
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level;
""")
# ON CONFLICT (user_id) DO UPDATE SET level=excluded.level;

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO NOTHING;
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING;
""")


time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS

song_select = ("""
    SELECT song_id, artists.artist_id
    FROM songs JOIN artists ON songs.artist_id = artists.artist_id
    WHERE songs.title = %s
    AND artists.name = %s
    AND songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
