import unittest
from bs4 import BeautifulSoup
from crawler_imdb import crawler_imdb
import requests
import tempfile
import json
import os

class TestCrawlerImdb(unittest.TestCase):

    def setUp(self):
        self.url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
        }
        self.page = requests.get(self.url, headers=self.header)
        self.soup_page = BeautifulSoup(self.page.content, 'html.parser')
        self.title_page = self.soup_page.find('title').get_text()
        self.temp_filename = tempfile.mktemp(suffix=".json")

    def tearDown(self):
        if os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)

    def test_get_page(self):
        page = crawler_imdb.get_page()
        soup_page = BeautifulSoup(page.content, 'html.parser')
        title_page = soup_page.find('title').get_text().lower()

        self.assertEqual(title_page, self.title_page.lower())
        self.assertEqual(self.soup_page.content, soup_page.content)

    def test_get_main_content(self):
        page = crawler_imdb.get_page()
        soup_page = crawler_imdb.get_main_content(page)

        attrs = {
            'data-testid': 'chart-layout-main-column'
        }
        main_content = soup_page.find("div", attrs=attrs).findChild('ul', class_='ipc-metadata-list')

        maint_content2 = self.soup_page.find("div", attrs=attrs).findChild('ul', class_='ipc-metadata-list')

        self.assertEqual(main_content, maint_content2)

    # def test_create_json(self):
    #     main_content = crawler_imdb.get_main_content(self.page)
    #     movies = crawler_imdb.crawler(main_content)
    #     crawler_imdb.create_json(movies)
    #     self.assertTrue(os.path.exists('movies.json'))
    #     with open('movies.json', 'r', encoding='utf-8') as json_file:
    #         created_movies = json.load(json_file)

    #     self.assertEqual(created_movies, movies)

if __name__ == '__main__':
    unittest.main()
