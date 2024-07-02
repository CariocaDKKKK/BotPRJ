import os
import json
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from func.start import start
from func.addid import addid
from func.cpf import cpf, reset_daily_usage
from func.cep import cep, reset_daily_usage
from func.nome import nome, reset_daily_usage
from func.telefone import telefone, reset_daily_usage
from func.email import email, reset_daily_usage
from func.mae import mae, reset_daily_usage


# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Caminho do arquivo de backup
BACKUP_FILE = 'bot_backup.bak'

# Lista de usuários autorizados
authorized_users = set()

# Dicionário para armazenar o número de consultas diárias de cada usuário
user_usage = {}

# Limite diário de consultas por usuário
DAILY_LIMIT = 90

# ID do administrador
ADMIN_ID = 5045936267

# Função para carregar os dados do arquivo de backup
def load_backup():
    global authorized_users, user_usage
    if os.path.exists(BACKUP_FILE):
        with open(BACKUP_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            authorized_users = set(data['authorized_users'])
            user_usage = {int(k): v for k, v in data['user_usage'].items()}

def main():
    load_backup()

    app = ApplicationBuilder().token("6361700021:AAFMSDmrihkTk4koad542YklYEJNoSxUjQo").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addid", lambda update, context: addid(update, context, ADMIN_ID)))
    app.add_handler(CommandHandler("cpf", lambda update, context: cpf(update, context, authorized_users, user_usage, DAILY_LIMIT, ADMIN_ID)))
    app.add_handler(CommandHandler("cep", lambda update, context: cep(update, context, authorized_users, user_usage, DAILY_LIMIT, ADMIN_ID)))
    app.add_handler(CommandHandler("nome", lambda update, context: nome(update, context, authorized_users, user_usage, DAILY_LIMIT, ADMIN_ID)))
    app.add_handler(CommandHandler("telefone", lambda update, context: telefone(update, context, authorized_users, user_usage, DAILY_LIMIT, ADMIN_ID)))
    app.add_handler(CommandHandler("email", lambda update, context: email(update, context, authorized_users, user_usage, DAILY_LIMIT, ADMIN_ID)))
    app.add_handler(CommandHandler("mae", lambda update, context: mae(update, context, authorized_users, user_usage, DAILY_LIMIT, ADMIN_ID)))

    # Configura o agendador para resetar a contagem de uso diariamente às 00:00
    scheduler = AsyncIOScheduler()
    scheduler.add_job(reset_daily_usage, trigger='cron', hour=0, minute=0)
    scheduler.start()

    logging.info("Bot iniciado e aguardando comandos")

    app.run_polling()

if __name__ == '__main__':
    main()
