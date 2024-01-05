from datetime import datetime
from bs4 import BeautifulSoup
from crawler_imdb import crawler_imdb
import unittest
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
        self.screenshot_path = ''

    def tearDown(self):
        if os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)
        if os.path.exists(self.screenshot_path):
            os.remove(self.screenshot_path)

    def test_get_page(self):
        page = crawler_imdb.get_page()
        soup_page = BeautifulSoup(page.content, 'html.parser')
        title_page = soup_page.find('title').get_text().lower()

        self.assertEqual(title_page, self.title_page.lower())
        self.assertEqual(self.soup_page.content, soup_page.content)

    def test_get_main_content(self):
        page = crawler_imdb.get_page()
        content = crawler_imdb.get_main_content(page)

        content2 = crawler_imdb.get_main_content(self.page)

        self.assertEqual(content, content2)

    def test_create_json(self):
        main_content = crawler_imdb.get_main_content(self.page)
        movies = crawler_imdb.get_movies_list(main_content)
        crawler_imdb.create_json(movies)
        self.assertTrue(os.path.exists('movies.json'))
        with open('movies.json', 'r', encoding='utf-8') as json_file:
            created_movies = json.load(json_file)

        self.assertEqual(created_movies, movies)

    def test_create_screenshot(self):
        screenshot_date = datetime.now().strftime('%d-%m-%Y_%H:%M')
        self.screenshot_path = f'images/screenshot_{screenshot_date}.png'
        crawler_imdb.create_screenshot(self.url)
        self.assertTrue(os.path.exists(self.screenshot_path))

if __name__ == '__main__':
    unittest.main()
