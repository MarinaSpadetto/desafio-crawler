import requests
import random
import json
import logging
import re
import time
import pandas as pd
import os
from datetime import datetime
from db.database import DatabaseManager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


USER_AGENTS_LIST = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

logging.basicConfig(
    filename='logs/crawler_log.txt',
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

db_config = {
    'host': os.environ.get('DATABASE_HOST'),
    'port': os.environ.get('DATABASE_PORT'),
    'database': os.environ.get('DATABASE'),
    'user': os.environ.get('DATABASE_USER'),
    'password': os.environ.get('DATABASE_PASSWORD'),
}


def get_page():
    # fetch URL
    url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    headers = {
        'User-Agent': random.choice(USER_AGENTS_LIST)
    }
    page = requests.get(url, headers=headers)
    logging.info(f'Crawling: {page.url}')
    return page


def get_main_content(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    attrs = {
        'data-testid': 'chart-layout-main-column'
    }
    content = soup.find("div", attrs=attrs).findChild(
        'ul', class_='ipc-metadata-list')
    return content


def save_movie_database(data_movie):
    logging.info('saving data movie in database')
    db_manager = DatabaseManager(db_config)
    movies_table = 'movies'
    fields_table = ['title VARCHAR', 'year VARCHAR',
                    'duration VARCHAR', 'rating VARCHAR']
    try:
        db_manager.create_table(movies_table, fields_table)
        logging.info(f'created table {movies_table}')
    except Exception as e:
        logging.error(
            f"Failed to create the table {movies_table} in database: {str(e)}", exc_info=True)
    try:
        db_manager.insert_data(movies_table, data_movie)
        logging.info(
            f'inserted data movie {data_movie} in database {movies_table}')
    except Exception as e:
        logging.error(
            f"Failed to inserting the data movie {data_movie} in table {movies_table}: {str(e)}", exc_info=True)
    db_manager.close_connection()
    return db_manager


def get_movies_list(content_page):
    movies = {
        'movies': []
    }

    for content in content_page:
        # retorna o conteudo da div com os dados do filme
        div_content_movie = content.find(
            'div', class_='ipc-metadata-list-summary-item__tc')
        logging.info(f'Crawling div content movie: {div_content_movie}')

        # retorna o titulo do filme
        title_movie = div_content_movie.find(
            'div', 'cli-children').find('h3').get_text()

        # retorna infos adicionais do filme
        div_info_movie = div_content_movie.find(
            'div', 'cli-title-metadata').findAll('span', class_='cli-title-metadata-item')
        try:
            year, duration, rating = div_info_movie
        except ValueError as ve:
            logging.error(
                f"Failed to unpack div_info_movie: {str(ve)}", exc_info=True)
            year, duration, rating = div_info_movie + \
                [None] * (3 - len(div_info_movie))

        if title_movie not in movies['movies']:
            movies['movies'].append({
                'title': re.sub(r'^\d+\.\s*', '', title_movie),
                'year': year.get_text() if year else '',
                'duration': duration.get_text() if duration else '',
                'rating': rating.get_text() if rating else ''
            })

        dict_movies = {
            'title': re.sub(r'^\d+\.\s*', '', title_movie),
            'year': year.get_text() if year else '',
            'duration': duration.get_text() if duration else '',
            'rating': rating.get_text() if rating else ''
        }
        save_movie_database(dict_movies)

    return movies


def create_json(movies):
    logging.info('creating json file: movies.json')
    try:
        with open('movies.json', 'w', encoding='utf-8') as json_file:
            json.dump(movies, json_file, ensure_ascii=False, indent=2)
            logging.info('created json file: movies.json')
    except Exception as e:
        logging.error(f"Failed to create the file: {str(e)}", exc_info=True)


def create_screenshot(url):
    logging.info('creating screenshot file')
    screenshot_date = datetime.now().strftime('%d-%m-%Y_%H:%M')
    screenshot_path = f'images/screenshot_{screenshot_date}.png'

    options = Options()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f'--user-agent={random.choice(USER_AGENTS_LIST)}')

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    driver.get(url)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(5)

    required_width = driver.execute_script(
        'return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script(
        'return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)

    try:
        body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))
        body.screenshot(screenshot_path)
    except Exception as e:
        logging.error(
            f"Failed to create the screenshot file: {str(e)}", exc_info=True)
    finally:
        logging.info(f'created screenshot: {screenshot_path}')
        driver.quit()


def create_dataframe_imdb():
    logging.info('creating the dataframe')
    try:
        with open('movies.json') as f:
            data = json.load(f)
        df = pd.json_normalize(data['movies'],
                               meta=['title', 'year', 'duration', 'rating'])
        df.index.name = 'id'
        df.to_csv('movies.csv', encoding='utf-8')
        logging.info(f'dataframe: \n {df.to_string()}')
    except Exception as e:
        logging.error(
            f"Failed to create the dataframe: {str(e)}", exc_info=True)


def main():

    try:
        page = get_page()
        content_page = get_main_content(page)
        movies_list = get_movies_list(content_page)
        create_json(movies_list)
        create_screenshot(page.url)
        create_dataframe_imdb()

    except Exception as e:
        logging.error(f"Failed to crawl: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()
