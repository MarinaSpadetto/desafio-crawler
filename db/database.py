import psycopg2
from psycopg2 import sql


class DatabaseManager:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, fields):
        # Crie a tabela apenas se ela ainda não existir

        create_table_query = "CREATE TABLE IF NOT EXISTS {} ({})".format(
            table_name,
            (', ').join(field for field in fields)
        )
        self.cursor.execute(sql.SQL(create_table_query))
        self.conn.commit()

    def insert_data(self, table_name, data):
        fields = ', '.join(data.keys())
        values = ', '.join('%s' for _ in data.values())
        insert_query = f"INSERT INTO {table_name} ({fields}) VALUES ({values})"
        self.cursor.execute(insert_query, tuple(data.values()))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
