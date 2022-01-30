# Lucerne Musical Events Pipeline

Python ETL pipeline to scrawl Lucerne music events in Switzerland and save them up in a Postgres DB.

#### docker compose for python etl, postgres  and pgadmin4
Run it:

```bash
docker-compose up
```

Run in detached mode (what I recommend):

```bash
docker-compose up -d
```

Shutting it down:

```bash
docker-compose down
```


#### To run without docker you need to set up the variables in the main method

You can set up a virtual environment , activate and then run this command.

```bash
pip install beautifulsoup4 pandas lxml requests sqlalchemy psycopg2
```

Run it:

```bash

python3 music_events_pipeline.py 

```


#### Hosted DB: building and running image for the pipeline, passing in relevant params
Assuming you have hosted postgres, you can change the parameters
Build the image

```bash
docker build -t lucerne_music_pipeline:v0.0.1 .
```

Run the python script as a standalone with Docker

```bash
URL="https://www.lucernefestival.ch/en/program/summer-festival-22"

YEAR="2022"
HOST=""
PORT=""

docker run -it \
  lucerne_music_pipeline:v0.0.1 \
    --user=root \
    --password=root \
    --host=${HOST} \
    --port=${PORT} \
    --db=music_events \
    --table_name=ch_lucerne_festival \
    --url=${URL}  \
    --year=${YEAR}
```


##### Docker-Compose  commands

Run it:

```bash
docker-compose up
```

Run in detached mode:

```bash
docker-compose up -d
```

Shutting it down:

```bash
docker-compose down
```


Force restart  and rebuild:

```bash
docker-compose up --build --force-recreate --no-deps -d
```

