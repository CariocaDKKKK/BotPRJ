import os
import json
import logging

# Caminho do arquivo de backup
BACKUP_FILE = 'bot_backup.bak'

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para carregar os dados do arquivo de backup
def load_backup():
    if os.path.exists(BACKUP_FILE):
        with open(BACKUP_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            authorized_users = set(data['authorized_users'])
            user_usage = {int(k): v for k, v in data['user_usage'].items()}
            return authorized_users, user_usage
    else:
        return set(), {}

# Função para salvar os dados no arquivo de backup
def save_backup(authorized_users, user_usage):
    data = {
        'authorized_users': list(authorized_users),
        'user_usage': user_usage
    }
    with open(BACKUP_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
