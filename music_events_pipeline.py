
import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine


class MusicalEventsCrawler:
    """
    This class crawls the Lucerne festival in Switzerland and saves the data in a Postgres Database
    """

    def __init__(self) -> None:
        self.URL = 'https://www.lucernefestival.ch/en/program/summer-festival-22'
        self.YEAR = '2022'
        
    def _getsoup(self):
        web_source = requests.get(self.URL).text
        soup = BeautifulSoup(web_source, 'lxml')
        return soup

    def _get_data_from_soup(self) -> list:
        """
        Preprocess all the data from soup and return as list
        """
        data = []
        soup = self._getsoup()
        for event in soup.find_all('div', class_='entry'):
            # Date
            full_date = ''
            date = event.find('p', class_='date')
            date = None if date is None else date.get_text()
            month = event.find('p', class_='month-number')
            month = None if month is None else month.get_text()
            if date is not None and month is not None:
                full_date = date + month + self.YEAR
            # Time
            time = event.find('p', class_='day-time')
            time = None if time is None else time.get_text()
            # Location
            location = event.find('p', class_='location')
            location = None if location is None else location.get_text().strip()
            # Title
            title = event.find('p', class_='surtitle')
            title = None if title is None else title.get_text()
            # image
            image = event.find('div', class_='image')
            if image is not None:
                image = str(image)
                image = image.split("(", 1)[1].split(")")[0]
            # artists
            artists = event.find('p', class_='title')
            artists = None if artists is None else artists.get_text()
            if artists is not None:
                artists = artists.split('|')
            #Add all datasets that are not none to dict
            if title is not None and artists is not None:
                data_dict = {
                "date": full_date,
                "time": time,
                "title": title,
                "artists": artists,
                "location": location,
                "image_url": image
                }
                data.append(data_dict)
            #print(data)
        return data

    def save_to_csv(self, csv_file_name :str) -> None:
        data = self._get_data_from_soup()
        keys = data[0].keys()
        with open(csv_file_name, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)


def main():
    music_events = MusicalEventsCrawler()
    music_events.save_to_csv('musical_events_ch.csv')


if __name__ == '__main__':
    main()