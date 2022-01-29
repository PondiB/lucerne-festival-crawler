# Lucerne Musical Events Pipeline

Python ETL pipeline to scrawl Lucerne music events in Switzerland and save them up in a Postgres DB.


#### To run without docker you need to set up the variables in the main method

You can set up a virtual environment , activate and then run this command.

```bash
pip install beautifulsoup4 pandas lxml requests sqlalchemy psycopg2
```

Run it:


```bash
URL="https://www.lucernefestival.ch/en/program/summer-festival-22"

YEAR="2022"

python3 music_events_pipeline.py \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5439 \
    --db=music_events \
    --table_name=ch_lucerne_festival \
    --url=${URL}  \
    --year=${YEAR}
```

#### docker compose for postgres  and pgadmin4
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
#### Finally building and running image for the pipeline, passing in relevant params
Build the image

```bash
docker build -t lucerne_music_pipeline:v0.0.1 .
```

Run the python script with Docker
NB: No spaces when assigning URL and YEAR variables

```bash
URL="https://www.lucernefestival.ch/en/program/summer-festival-22"

YEAR="2022"

docker run -it \
  lucerne_music_pipeline:v0.0.1 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5439 \
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

