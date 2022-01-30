import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from typing import List, Dict
import logging
from time import time
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(filename='pipeline.log', level=logging.INFO)

__author__  = "Brian Pondi"
__status__  = "Development"


class MusicalEventsPipeline:
    """
    This class crawls the Lucerne festival events scheduled for 2022 in Switzerland and saves the data in a Postgres Database.
    """

    def __init__(self, web_url : str, year : str) -> None:
        self.web_url = web_url 
        self.year = year
        logging.info(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
        
    def _getsoup(self):
        """
        Returns soup of the website to be crawled on.
        """
        web_source = requests.get(self.web_url).text
        soup = BeautifulSoup(web_source, 'lxml')
        logging.info('Soup is ready')
        return soup
    
    def _none_checker(self, field):
        """
        Checker that returns None for soup values are empty and returns text data if soup values have content.
        """
        return None if field is None else field.get_text().strip()

    def _get_data_from_soup(self) -> List[Dict]:
        """
        Preprocess all the needed data from soup and return as list of dictionaries.
        """
        data = []
        soup = self._getsoup()
        for event in soup.find_all('div', class_='entry'):
            # Date
            full_date = ''
            date = event.find('p', class_='date')
            date = self._none_checker(date)
            month = event.find('p', class_='month-number')
            month = self._none_checker(month)
            if date is not None and month is not None:
                full_date = date + month + self.year
            #Event Day-Time
            day_time = event.find('p', class_='day-time')
            #Event Time & Event day as separate values
            time = ''
            day = ''
            if day_time is not None:
                time = day_time.find( 'span',class_ ='time')
                time = self._none_checker(time)
                day = day_time.find( 'span',class_ ='day')
                day = self._none_checker(day)
            # Location
            location = event.find('p', class_='location')
            location = self._none_checker(location)
            # Title
            title = event.find('p', class_='surtitle')
            title = self._none_checker(title)
            # image
            image = event.find('div', class_='image')
            if self._none_checker(image)is not None:
                image = str(image)
                image = image.split("(", 1)[1].split(")")[0]
            # artists
            artists = event.find('p', class_='title')
            artists = self._none_checker(artists)
            if artists is not None:
                artists = artists.split('|')
            #Add all datasets that are not none to dict
            if title is not None:
                data_dict = {
                "date": full_date,
                "day" : day,
                "time": time,
                "title": title,
                "artists": artists,
                "location": location,
                "image_url": image
                }
                data.append(data_dict)
        logging.info('All datasets have been fetched')
        return data

    def save_to_csv(self, csv_file_name :str) -> None:
        """
        This method to save data into a csv is not a must I mainly used it to just validate things work.
        """
        data = self._get_data_from_soup()
        keys = data[0].keys()
        with open(csv_file_name, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        logging.info('saved the data to csv')

    def _data_to_pandas_df(self) -> pd.DataFrame:
        """
        Convert data list of dicts to pandas dataframe.
        """
        data = self._get_data_from_soup()
        df = pd.DataFrame(data)
        return df

    def _convert_datestring_to_date(self) -> pd.DataFrame:
        """
        The date field comes in as a string, it's ideal to have it as a timestamp.
        """
        df = self._data_to_pandas_df()
        df['date'] = pd.to_datetime(df['date'])
        logging.info('Converted string date format to datetimestamp')
        return df

    def save_to_postgres(self, user:str, password : str, host : str,
                        port: str, db: str, table_name : str) -> None:
        """
        Saves Lucerne Festival events into a postgresql DB.
        """
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
        engine.connect()
        df = self._convert_datestring_to_date()
        pd.io.sql.get_schema(df, name=table_name, con=engine)
        logging.info(pd.io.sql.get_schema(df, name=table_name, con=engine))
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        df.to_sql(name=table_name, con=engine, if_exists='append')
        logging.info('Finished inserting the data to Postgres')


def main():
    user = os.environ['PG_USER']
    password = os.environ['PG_PASSWORD']
    host = os.environ['PG_HOST']
    port = os.environ['PG_PORT']
    db = os.environ['PG_DB_NAME']
    table_name = os.environ['PG_TABLE_NAME']
    url = os.environ['WEB_URL']
    year= os.environ['YEAR']
    
    start_time = time()

    music_events = MusicalEventsPipeline(url, year)
    music_events.save_to_csv('ch_lucerne_festival_events.csv')
    music_events.save_to_postgres(user, password, host, port, db, table_name)

    end_time = time()

    time_taken = end_time - start_time
    logging.info(f'The whole process took {time_taken} seconds')

    logging.info("--------------------------------------------------------------")
    logging.info("--------------------------------------------------------------")


if __name__ == '__main__':
    main()
