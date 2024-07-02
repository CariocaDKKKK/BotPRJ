from telegram import Update
from telegram.ext import ContextTypes
import logging
from db import load_backup, save_backup

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

    # Carregar o backup
    authorized_users, user_usage = load_backup()

    # Adicionar o novo ID e inicializar o uso como 0
    if user_id not in authorized_users:
        authorized_users.add(user_id)
        user_usage[user_id] = 0

        # Salvar o novo conteúdo no arquivo de backup
        save_backup(authorized_users, user_usage)

        await update.message.reply_text(f"ID {user_id} adicionado com sucesso!")
        logging.info(f'ID {user_id} adicionado pelo administrador')
    else:
        await update.message.reply_text(f"ID {user_id} já está autorizado.")
        logging.info(f'ID {user_id} já está na lista de autorizados')
