import time
import random
import mysql.connector
import requests
from PIL import Image
import io
import base64
import re
import logging
from bs4 import BeautifulSoup
from tqdm import tqdm
import datetime
import cloudscraper


class Scraper:
    RETRY_TIMES = 5

    def __init__(self, db_config):
        self.session = cloudscraper.create_scraper()
        self.db_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool", pool_size=10, **db_config)
        self.existing_cars = set()

    def get_db_connection(self):
        return self.db_pool.get_connection()

    def handle_request(self, url):
        for _ in range(self.RETRY_TIMES):
            try:
                return self.session.get(url, timeout=20).text
            except requests.exceptions.RequestException:
                time.sleep(random.randint(1, 5))
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                time.sleep(random.randint(1, 5))
        logging.warning(
            f"Unable to get {url} after {self.RETRY_TIMES} attempts.")
        return None

    def get_tags(self, soup):
        tags_element = soup.select_one('h5.tags.h6-md')
        if tags_element is None:
            return ""
        tags = [a.text for a in tags_element.find_all('a')]
        return ",".join(tags)

    def get_actor(self, soup):
        spans = soup.select(
            'div.models > a.model > span.placeholder.rounded-circle, div.models > a.model > img.avatar.rounded-circle'
        )
        titles = [span['title'] for span in spans]
        result = ', '.join(titles)
        return result

    def get_date(self, soup):
        info_header = soup.find('div', {'class': 'info-header'})
        if info_header is None:
            return datetime.date(1970, 1, 1)
        date_span = info_header.find('span', {'class': 'inactive-color'})
        if date_span is None:
            return datetime.date(1970, 1, 1)
        date_str = date_span.text.split(' ')[-1]
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            logging.error(f"Invalid date format: {date_str}")
            date = datetime.date(1970, 1, 1)
        return date

    def update_record(self, csr, car, new_tags):
        csr.execute('UPDATE avdb_images SET tags = %s WHERE car = %s',
                    (new_tags, car))
        logging.info(f"Tags for car {car} have been updated.")

    def process_item(self, item, csr, conn):
        title = item.select_one('div.detail > h6.title > a').text
        match = re.match(r'([a-zA-Z0-9-_]+)', title)
        if match:
            car = match.group(1)
        else:
            logging.error("No car matched")

        if car in self.existing_cars:
            logging.info(
                f"Car {car} already exists in cache, skipping this item.")
            return

        csr.execute('SELECT tags FROM avdb_images WHERE car = %s', (car, ))
        result = csr.fetchone()
        if result is not None:
            existing_tags = result[0]
            logging.info(
                f"Car {car} already exists in the database, checking if tags need to be updated."
            )
            self.existing_cars.add(car)
            details_url = item.select_one('div.detail > h6.title > a')['href']
            details_contents = self.handle_request(details_url)
            if details_contents is not None:
                soup2 = BeautifulSoup(details_contents, 'lxml')
                new_tags = self.get_tags(soup2)
                if new_tags != existing_tags:
                    self.update_record(csr, car, new_tags)
            else:
                logging.warning("details_contents is not defined.")
            return

        imgUrl = "/".join(
            item.select_one('img.lazyload')['data-src'].split("/")
            [:-2]) + "/preview.jpg"
        for _ in range(self.RETRY_TIMES):
            try:
                response = requests.get(imgUrl)
                if response.status_code == 200 and 'image' in response.headers[
                        'Content-Type']:
                    image = Image.open(io.BytesIO(response.content))
                    buffered = io.BytesIO()
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    details_url = item.select_one(
                        'div.detail > h6.title > a')['href']
                    details_contents = self.handle_request(details_url)
                    if details_contents is not None:
                        soup2 = BeautifulSoup(details_contents, 'lxml')
                        tags = self.get_tags(soup2)
                        actors = self.get_actor(soup2)
                        date = self.get_date(soup2)
                        create_time = datetime.datetime.now()
                        csr.execute(
                            'INSERT INTO avdb_images (car, title, actor, date, url, img, img_base64, tags, create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            [
                                car, title, actors, date,
                                item.select_one('div.detail > h6.title > a')
                                ['href'], imgUrl, img_str, tags, create_time
                            ])
                        conn.commit()
                        self.existing_cars.add(car)
                        break
                    else:
                        logging.warning("details_contents is not defined.")
                else:
                    logging.warning(
                        f"Invalid response for image URL: {imgUrl}")
                    continue
            except (mysql.connector.IntegrityError,
                    requests.exceptions.RequestException):
                time.sleep(random.randint(1, 5))
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                break

    def process_content(self, content):
        soup = BeautifulSoup(content, 'lxml')
        with self.get_db_connection() as conn:
            csr = conn.cursor()
            items = soup.select('div.col-6.col-sm-4.col-lg-3')
            for item in tqdm(items, desc="Processing: ", leave=False):
                self.process_item(item, csr, conn)

    def scrape(self, url):
        time.sleep(random.randint(1, 5))
        content = self.handle_request(url)
        self.process_content(content)


if __name__ == '__main__':
    logging.basicConfig(filename='app.log',
                        filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    db_config = {
        "user": "root",
        "password": "password",
        "host": "localhost",
        "database": "jable",
    }
    scraper = Scraper(db_config)
    with scraper.get_db_connection() as conn:
        csr = conn.cursor()
        csr.execute('SELECT car FROM avdb_images')
        scraper.existing_cars.update(car for (car, ) in csr.fetchall())
    for i in tqdm(range(1, 966), colour='green', desc='Progress: '):
        time.sleep(1)
        url = f"https://fs1.app/new-release/?mode=async&function=get_block&block_id=list_videos_common_videos_list&sort_by=release_year&from={str(i)}"
        scraper.scrape(url)
