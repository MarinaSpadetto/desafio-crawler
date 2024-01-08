# Desafio Beemon

Esta aplicação foi desenvolvida para o criar um [crawler](https://github.com/beemontech/desafio-crawler) pela empresa
Beemôn. Neste README, você encontrará informações essenciais sobre como configurar e executar este projeto.

## Descrição

Este projeto consiste em um web crawler desenvolvido em Python para extrair informações sobre os 250 filmes mais bem avaliados do IMDb. O crawler percorre a página do IMDb, coletando dados e armazenando-os em um formato JSON. Além disso, os dados são persistidos em um banco de dados PostgreSQL.

## Recursos:

- Extração de dados dos 250 filmes principais do IMDb.
- Armazenamento em JSON e persistência em um banco de dados PostgreSQL.
- Utilização de um dataframe para visualização dos dados e exportação para um arquivo CSV.
- Sistema de logs que registra informações relevantes em um arquivo TXT.
- Captura uma screenshot da lista de filmes na página do IMDb, fornecendo informações do conteúdo no momento da extração.

## Configurações do Projeto

Esta aplicação pode ser executada via docker-compose.

### Configuração e Execução com Docker Compose

Para executar a aplicação usando Docker Compose, siga estas etapas:

1. Clone este repositório em sua máquina local:

   ```
   git clone https://github.com/MarinaSpadetto/desafio-crawler
   ```

2. Acesse o diretório da aplicação:

   ```
   cd desafio-crawler
   ```

3. Construa e inicie o contêiner Docker usando Docker Compose:

    ```
    docker-compose up -d --build
    ```

4. Acesse o `bash` do container, execute este comando:

   ```
   docker exec -it bm-crawler bash
   ```

5. Execute o seguinte comando na raiz, para iniciar o crawler:

   ```
   python3 crawler_imdb.py
   ```

6. Para rodar os testes execute este comando:

   ```
   python3 -m datatest test/test_crawler_imbd.py
   ```

### Acessar o banco de dados

Lembre-se de verificar se o container do PostgreSQL está em execução.

1. Acesse http://localhost:15432/browser/.
2. Faça login com as credenciais.

### Observações

1. Lembre-se de parar os contêineres Docker (usando `docker-compose down`).


---
Desenvolvido por Marina Spadetto
