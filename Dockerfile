FROM python:3.9

RUN pip install beautifulsoup4 pandas lxml requests sqlalchemy psycopg2

WORKDIR /app

COPY music_events_pipeline.py .
