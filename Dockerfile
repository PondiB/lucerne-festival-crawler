FROM python:3.9

RUN apt-get install wget
RUN pip install beautifulsoup4 pandas lxml requests sqlalchemy psycopg2

WORKDIR /app

COPY music_events_pipeline.py music_events_pipeline.py

ENTRYPOINT [ "python", "music_events_pipeline.py" ]