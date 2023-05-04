import sqlite3
import time

import cloudscraper
from bs4 import BeautifulSoup
from tqdm import tqdm
session = cloudscraper.create_scraper()

db = "AV.db"

if __name__ == '__main__':

    for i in tqdm(range(1, 5), colour='green', desc='进度: '):
        time.sleep(1)
        # 最新上市

        url = f"https://fs1.app/new-release/?mode=async&function=get_block&block_id=list_videos_common_videos_list&sort_by=release_year&from={str(i)}"
        # 最近更新

        # url = f"https://fs1.app/latest-updates/?mode=async&function=get_block&block_id=list_videos_latest_videos_list&sort_by=post_date&from={str(i)}"
        content = session.get(url, timeout=20).text

        soup = BeautifulSoup(content, 'lxml')
        with sqlite3.connect(db) as conn:
            csr = conn.cursor()
            for item in soup.select('div.col-6.col-sm-4.col-lg-3'):
                title = item.select_one('div.detail > h6.title > a').text
                # print("car:", title.split()[0])
                # print("title:", title)
                # print("url:", item.select_one('div.detail > h6.title > a')['href'])
                # print("img:", "/".join(item.select_one('img.lazyload')['data-src'].split("/")[:-2]) + "/preview.jpg")
                try:
                    csr.execute('INSERT INTO AVdb (car, title, url, img) VALUES (?, ?, ?, ?)',
                                [title.split()[0], title, item.select_one('div.detail > h6.title > a')['href'],
                                 "/".join(
                                     item.select_one('img.lazyload')['data-src'].split("/")[:-2]) + "/preview.jpg"])
                except sqlite3.IntegrityError:
                    pass
            conn.commit()
