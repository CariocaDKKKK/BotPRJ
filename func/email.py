import requests
import os
import json
import logging
from datetime import datetime
from telegram import Update, InputFile
from telegram.ext import ContextTypes

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Caminho do arquivo de backup
BACKUP_FILE = 'bot_backup.bak'

# Função para carregar os dados do arquivo de backup
def load_backup():
    global authorized_users, user_usage
    if os.path.exists(BACKUP_FILE):
        with open(BACKUP_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            authorized_users = set(data['authorized_users'])
            user_usage = {int(k): v for k, v in data['user_usage'].items()}

# Função para salvar os dados no arquivo de backup
def save_backup(authorized_users, user_usage):
    data = {
        'authorized_users': list(authorized_users),
        'user_usage': user_usage
    }
    with open('bot_backup.bak', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Função para resetar a contagem de uso diário
def reset_daily_usage():
    global user_usage
    for user_id in user_usage:
        user_usage[user_id] = 0
    save_backup()
    logging.info("Contagem de uso diário resetada")

# Função para formatar os dados do JSON em uma string legível
def format_data(data, indent=0):
    formatted_data = ""
    indent_space = "  " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            formatted_data += f"{indent_space}{key}: {value}\n" if not isinstance(value, (dict, list)) else f"{indent_space}{key}:\n{format_data(value, indent + 1)}"
    elif isinstance(data, list):
        for item in data:
            formatted_data += format_data(item, indent + 1)
    else:
        formatted_data += f"{indent_space}{data}\n"
    return formatted_data

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE, authorized_users, user_usage, DAILY_LIMIT, ADMIN_ID) -> None:
    user_id = update.effective_user.id
    if user_id not in authorized_users:
        await update.message.reply_text("Você não tem permissão para usar este comando.")
        logging.warning(f'{update.effective_user.first_name} (ID: {user_id}) tentou usar /Email sem permissão')
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "Por favor, use o comando /Email seguido do número do telefone. Exemplo: /Email 21965502993")
        return

    # Verificar o uso diário do usuário
    if user_id not in user_usage:
        user_usage[user_id] = 0

    if user_usage[user_id] >= DAILY_LIMIT:
        await update.message.reply_text("Você atingiu o limite diário de consultas. O limite será resetado às 00:00.")
        return

    email = context.args[0]
    url = f"http://api.dbconsultas.com/api/v1/71383fd8-cbf6-48e6-a241-ee5c0b8bfd7a/email/{email}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("data") is None and data.get("status") == 401:
            await update.message.reply_text("⚠️ DADOS NAO ENCONTRADOS ⚠️")
            logging.warning(f'Consulta retornou dados não encontrados para o Email {email} por {user_id}')
            return

        # Formata os dados do JSON em uma string legível
        formatted_data = "Email:\n\n" + format_data(data)

        # Salva a resposta formatada em um arquivo .txt
        file_path = f"Email_{email}.txt"
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(formatted_data)

        # Envia o arquivo ao usuário
        with open(file_path, 'rb') as file:
            await update.message.reply_document(document=InputFile(file, filename=f"Email : {email}.txt"))

        # Remove o arquivo após enviar
        os.remove(file_path)

        # Incrementa o contador de uso do usuário
        user_usage[user_id] += 1
        save_backup(authorized_users, user_usage)

        # Envia mensagem com o uso restante
        remaining_usage = DAILY_LIMIT - user_usage[user_id]
        await update.message.reply_text(
            f"Você tem {remaining_usage}/{DAILY_LIMIT} consultas restantes para hoje. O limite será resetado às 00:00.")

        # Log para administrador
        await context.bot.send_message(chat_id=ADMIN_ID, text=f'Usuário {user_id} fez uma consulta no email : {email}.')
        logging.info(f'Usuário {user_id} fez uma consulta no email : {email}')

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            await update.message.reply_text("⚠️ DADOS NAO ENCONTRADOS ⚠️")
            logging.warning(f'Consulta retornou dados não encontrados para o email {email} por {user_id}')
        else:
            await update.message.reply_text(f"Ocorreu um erro ao consultar o email.")
            logging.error(f'Erro ao consultar email {email} por {user_id}: {e}')
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"Ocorreu um erro ao consultar o email.")
        logging.error(f'Erro ao consultar email {email} por {user_id}: {e}')
