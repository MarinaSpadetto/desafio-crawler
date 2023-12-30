import requests
import random
import json
from bs4 import BeautifulSoup

USER_AGENTS_LIST = [
  'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

def get_page():
  # retorna o conteudo da pagina.
  url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
  headers = {'User-Agent': random.choice(USER_AGENTS_LIST)}
  page = requests.get(url, headers=headers)
  return page

def get_content_page(page):
  soup = BeautifulSoup(page.content, 'html.parser')
  # pegar as tag li`s
  content = soup.find("div", attrs={'data-testid': 'chart-layout-main-column'}).findChild('ul', class_='ipc-metadata-list')
  return content

def create_json(movies):
  # cria arquivo json
  json_obj = json.dumps(movies)
  file = open('filmes.json', 'w')
  file.write(json_obj)
  file.close()

def main():
  movies = {
    'movies': []
  }
  page = get_page()
  content_page = get_content_page(page)

  for content in content_page:

    # retorna o conteudo da div com os dados do filme
    div_content_movie = content.find('div', class_='ipc-metadata-list-summary-item__tc')

    # retorna o titulo do filme
    title_movie = div_content_movie.find('div', 'cli-children').find('h3').get_text()

    # retorna infos adicionais do filme
    div_info_movie = div_content_movie.find('div', 'cli-title-metadata')
    year, duration, rating = div_info_movie

    if div_title_movie not in movies['movies']:
      movies['movies'].append({
        'title': title_movie,
        'year': year.get_text(),
        'duration': duration.get_text(),
        'rating': rating.get_text()
      })

  create_json(movies)


if __name__ == "__main__":
  main()
