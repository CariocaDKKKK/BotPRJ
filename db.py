import sqlite3
import os
import logging

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
                usage_count INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

# Função para carregar os dados do banco de dados
def load_backup():
    init_db()
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM authorized_users')
        authorized_users = {row[0] for row in cursor.fetchall()}
        cursor.execute('SELECT user_id, usage_count FROM user_usage')
        user_usage = {row[0]: row[1] for row in cursor.fetchall()}

        logging.info(f"Dados carregados: {authorized_users}, {user_usage}")  # Log dos dados carregados

        return authorized_users, user_usage

# Função para salvar os dados no banco de dados
def save_backup(authorized_users, user_usage):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM authorized_users')
        cursor.execute('DELETE FROM user_usage')
        cursor.executemany('INSERT INTO authorized_users (id) VALUES (?)', [(user,) for user in authorized_users])
        cursor.executemany('INSERT INTO user_usage (user_id, usage_count) VALUES (?, ?)', user_usage.items())
        conn.commit()

        logging.info(f"Dados salvos: {authorized_users}, {user_usage}")  # Log dos dados salvos

# Inicializar o banco de dados na primeira execução
if not os.path.exists(DB_FILE):
    init_db()

def reset_daily_usage(authorized_users, user_usage):
    for user_id in user_usage:
        user_usage[user_id] = 0
    save_backup(authorized_users, user_usage)
    logging.info("Contagem de uso diário resetada")

# Função para adicionar um usuário autorizado
def add_user(user_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authorized_users (id) VALUES (?)', (user_id,))
        cursor.execute('INSERT INTO user_usage (user_id, usage_count) VALUES (?, 0)', (user_id,))
        conn.commit()
        logging.info(f'Usuário {user_id} adicionado ao banco de dados')

# Função para carregar os dados do banco de dados com retorno
def load_data():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM authorized_users')
        authorized_users = {row[0] for row in cursor.fetchall()}
        cursor.execute('SELECT user_id, usage_count FROM user_usage')
        user_usage = {row[0]: row[1] for row in cursor.fetchall()}
        logging.info(f'Dados carregados: {authorized_users}, {user_usage}')
        return authorized_users, user_usage
