import requests
import random
import json
import logging
from bs4 import BeautifulSoup

USER_AGENTS_LIST = [
  'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

logging.basicConfig(
    filename='crawler_log.txt',
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)


def get_page():
  # fetch URL
  url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
  headers = {
    'User-Agent': random.choice(USER_AGENTS_LIST)
  }
  page = requests.get(url, headers=headers)
  logging.info(f'Crawling: {page.url}')
  return page

def get_content_page(page):
  soup = BeautifulSoup(page.content, 'html.parser')
  attrs = {
    'data-testid': 'chart-layout-main-column'
  }
  content = soup.find("div", attrs=attrs).findChild('ul', class_='ipc-metadata-list')
  return content

def create_json(movies):
  try:
    with open('movies.json', 'w', encoding='utf-8') as json_file:
      json.dump(movies, json_file, ensure_ascii=False, indent=2)
      logging.info('create json file: movies.json')
  except Exception as e:
        logging.error(f"Failed to create the file: {str(e)}", exc_info=True)

def main():

  movies = {
    'movies': []
  }

  try:
    page = get_page()
    content_page = get_content_page(page)

    for content in content_page:

      # retorna o conteudo da div com os dados do filme
      div_content_movie = content.find('div', class_='ipc-metadata-list-summary-item__tc')
      logging.info(f'Crawling div content movie: {div_content_movie}')

      # retorna o titulo do filme
      title_movie = div_content_movie.find('div', 'cli-children').find('h3').get_text()

      # retorna infos adicionais do filme
      div_info_movie = div_content_movie.find('div', 'cli-title-metadata')
      year, duration, rating = div_info_movie

      if title_movie not in movies['movies']:
        movies['movies'].append({
          'title': title_movie,
          'year': year.get_text(),
          'duration': duration.get_text(),
          'rating': rating.get_text()
        })

    create_json(movies)

  except Exception as e:
        logging.error(f"Failed to crawl: {str(e)}", exc_info=True)


if __name__ == "__main__":
  main()
