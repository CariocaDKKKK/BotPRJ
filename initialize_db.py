import sqlite3
import os

# Caminho do arquivo de banco de dados SQLite
DB_FILE = 'mini_db.db'

# Função para inicializar o banco de dados
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authorized_users (
                id INTEGER PRIMARY KEY
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_usage (
                user_id INTEGER PRIMARY KEY,
                usage_count INTEGER
            )
        ''')
        conn.commit()
        print("Banco de dados inicializado com sucesso.")

if __name__ == '__main__':
    init_db()
