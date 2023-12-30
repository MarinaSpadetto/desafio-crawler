import requests
import random
import json
from bs4 import BeautifulSoup

def main():
  # trazer o conteudo da pagina
  user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
  ]
  url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
  headers = {'User-Agent': random.choice(user_agents_list)}
  page = requests.get(url, headers=headers)
  soup = BeautifulSoup(page.content, 'html.parser')
  # pegar as tag li`s
  tag_lis = soup.find("div", attrs={'data-testid': 'chart-layout-main-column'}).findChild('ul', class_='ipc-metadata-list')

  name_movies = {
    'filmes': []
  }
  for content in tag_lis:

    # retorna o conteudo da div com os dados do filme
    div_conteudo_filme = content.find('div', class_='ipc-metadata-list-summary-item__tc')

    # retorna o titulo do filme
    div_titulo = div_conteudo_filme.find('div', 'cli-children').find('h3').get_text()

    # retorna infos adicionais do filme
    div_info_filme = div_conteudo_filme.find('div', 'cli-title-metadata')
    ano, duracao, classificao = div_info_filme


    if div_titulo not in name_movies['filmes']:
      name_movies['filmes'].append({
        'nome': div_titulo,
        'ano': ano.get_text(),
        'duracao': duracao.get_text(),
        'classificacao': classificao.get_text()
      })

  # cria arquivo json
  json_obj = json.dumps(name_movies)
  file = open('filmes.json', 'w')
  file.write(json_obj)
  file.close()

if __name__ == "__main__":
  main()
