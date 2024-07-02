import os
import json
import logging
from telegram import Update
from telegram.ext import ContextTypes

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Caminho do arquivo de backup
BACKUP_FILE = 'bot_backup.bak'

# Função para carregar os dados do arquivo de backup
def load_backup():
    authorized_users = set()
    if os.path.exists(BACKUP_FILE):
        with open(BACKUP_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            authorized_users = set(data.get('authorized_users', []))
    return authorized_users

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    authorized_users = load_backup()

    if user_id in authorized_users:
        await update.message.reply_text(
            f'Olá {update.effective_user.first_name}, você já está habilitado para usar o bot.\n\n'
            'Comandos disponíveis:\n'
            '/cpf - Consultar informações por CPF\n'
        )
    else:
        await update.message.reply_text(
            f'{update.effective_user.first_name}, Este é um bot de consulta exclusivo para membros da Panela. '
            f'Seu ID de usuário é {user_id}. Por favor, envie seu ID para @MestreSplinterOFC para ser cadastrado.'
        )
        logging.info(f'Comando /start usado por {update.effective_user.first_name} (ID: {user_id})')

