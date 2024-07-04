import logging
from telegram import Update
from telegram.ext import ContextTypes
from db import load_backup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    # Carregar os dados do banco de dados
    authorized_users, _ = load_backup()

    if user_id in authorized_users:
        await update.message.reply_text(
            f'Olá {update.effective_user.first_name}, você já está habilitado para usar o bot.\n\n'
            'Comandos disponíveis:\n'
            '/cpf - Consultar informações por CPF\n'
            '/cep - Consultar informações por CEP\n'
            '/mae - Consultar informações por mãe\n'
            '/nome - Consultar informações por nome\n'
            '/email - Consultar informações por email\n'
            '/telefone - Consultar informações por telefone\n'
            '/titulo - EM BREVE\n'
        )
    else:
        await update.message.reply_text(
            f'{update.effective_user.first_name}, este é um bot de consulta exclusivo para membros da Panela. '
            f'Seu ID de usuário é {user_id}. Por favor, envie seu ID para @MestreSplinterOFC para ser cadastrado.'
        )
        logging.info(f'Comando /start usado por {update.effective_user.first_name} (ID: {user_id})')
