FROM python:3.9-slim-buster

RUN pip install beautifulsoup4 pandas lxml requests sqlalchemy psycopg2-binary

WORKDIR /app

COPY music_events_pipeline.py .
