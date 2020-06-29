# Data Modeling with SQL: PostgreSQL

## Introduction:

* A startup wants to analyze the data they've been collecting on songs and user activity on their new music streaming app.

* The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## Datasets:

Two datasets were used:

* Song dataset: It is really a subset that contains metadata about a song and the artist of that song.
* Log dataset: Log files simulating activity logs from a music streaming app.


## HowTo: Database, Jupyter Notebook and Python

### Requirements:

The following Python packages were used:
```
ipython-sql
psycopg2
glob
pandas
```

### PostgreSQL:

Docker-composed is used to build the database up:

* Pull down and run the container in the background:
```
docker-compose up -d
```

* Access to the container if it is required:
```
docker-compose exec postgres_db bash
```

* Stops running the container without removing it:
```
docker-compose down
```

### Jupyter Notebook and Python files:

Once the PostgreSQL is up and reachable, follow these steps to run this project:

* Run the `main.ipynb` notebook or alternatively, run `create_tables.py` manually. This process will create the fact and dimension tables for the star schema.

* Run the `etl.ipynb` notebook. This notebook has two parts:
  * The first part will read and process a single file from each dataset and will load the data into the tables previously created.
  * The second part, just at the end of the notebook, will read and process all files from both datasets and will load them into the tables. Alternatively, you can run `etl.py` manually.

* Verify the content of the tables using `test.ipynb`.
