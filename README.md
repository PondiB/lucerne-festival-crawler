# Lucerne Musical Events Pipeline

Python ETL pipeline to scrawl Lucerne music events in Switzerland and save them up in a Postgres DB.

#### docker compose for python etl, postgres  and pgadmin4

You first need to clone the repository via this command:

```bash
git clone https://github.com/PondiB/musical-events-crawler.git
```

then you can change to that directory

```bash
$cd musical-events-crawler
```

Run in detached mode (what I recommend):

```bash
docker-compose up -d
```


Run it (Another option):

```bash
docker-compose up
```


Shutting it down:

```bash
docker-compose down
```


#### To run without docker you need to set up the variables in the main method

You can set up a virtual environment , activate and then run this command.

```bash
pip install beautifulsoup4 pandas lxml requests sqlalchemy psycopg2-binary
```
Another option will be via requirements.txt but  I did not generate the file content.

Run it:

```bash
python3 music_events_pipeline.py 
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

