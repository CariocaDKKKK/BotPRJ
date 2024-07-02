from telegram import Update
from telegram.ext import ContextTypes
import logging
import json
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def addid(update: Update, context: ContextTypes.DEFAULT_TYPE, admin_id: int) -> None:
    if update.effective_user.id != admin_id:
        await update.message.reply_text("Você não tem permissão para usar este comando.")
        logging.warning(f'{update.effective_user.first_name} tentou usar /addid sem permissão')
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "Por favor, use o comando /addid seguido do ID do usuário. Exemplo: /addid 123456789")
        return

    user_id = int(context.args[0])

    # Ler o conteúdo do arquivo bot_backup.bak
    if os.path.exists('bot_backup.bak'):
        with open('bot_backup.bak', 'r') as file:
            data = json.load(file)
    else:
        data = {"authorized_users": [], "user_usage": {}}

    # Adicionar o novo ID e inicializar o uso como 0
    if user_id not in data["authorized_users"]:
        data["authorized_users"].append(user_id)
        data["user_usage"][str(user_id)] = 0

        # Salvar o novo conteúdo no arquivo bot_backup.bak
        with open('bot_backup.bak', 'w') as file:
            json.dump(data, file, indent=4)

        await update.message.reply_text(f"ID {user_id} adicionado com sucesso!")
        logging.info(f'ID {user_id} adicionado pelo administrador')
    else:
        await update.message.reply_text(f"ID {user_id} já está autorizado.")
        logging.info(f'ID {user_id} já está na lista de autorizados')
