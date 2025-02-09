import requests
import os
import logging
from datetime import datetime, timedelta
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from urllib.parse import quote

from db import load_backup, save_backup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CACHE_DIR = "cachemae"

# Cria o diretório de cache se não existir
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


# Função para formatar os dados do JSON em uma string legível
def format_data(data, indent=0):
    formatted_data = ""
    indent_space = "  " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if not isinstance(value, (dict, list)):
                formatted_data += f"{indent_space}{key}: {value}\n"
            else:
                formatted_data += f"{indent_space}{key}:\n{format_data(value, indent + 1)}"
    elif isinstance(data, list):
        for item in data:
            formatted_data += format_data(item, indent + 1)
    else:
        formatted_data += f"{indent_space}{data}\n"
    return formatted_data


# Função para limpar o cache de arquivos com mais de 7 dias
def clear_old_cache_files():
    now = datetime.now()
    for filename in os.listdir(CACHE_DIR):
        file_path = os.path.join(CACHE_DIR, filename)
        if os.path.isfile(file_path):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - file_mtime > timedelta(days=7):
                os.remove(file_path)
                logging.info(f"Arquivo de cache removido: {file_path}")


async def mae(update: Update, context: ContextTypes.DEFAULT_TYPE, authorized_users, user_usage, DAILY_LIMIT,
              ADMIN_ID) -> None:
    user_id = update.effective_user.id

    # Recarregar dados do banco de dados para garantir que estão atualizados
    authorized_users, user_usage = load_backup()

    # Verificar se o usuário está autorizado
    if user_id not in authorized_users:
        await update.message.reply_text("Você não tem permissão para usar este comando.")
        logging.warning(f'{update.effective_user.first_name} (ID: {user_id}) tentou usar /mae sem permissão')
        return

    # Verificar o número de argumentos
    if len(context.args) < 1:
        await update.message.reply_text(
            "Por favor, use o comando /mae seguido do nome completo. Exemplo: /mae leandro costa")
        return

    # Verificar o uso diário do usuário
    if user_id not in user_usage:
        user_usage[user_id] = 0

    if user_usage[user_id] >= DAILY_LIMIT:
        await update.message.reply_text("Você atingiu o limite diário de consultas. O limite será resetado às 00:00.")
        logging.warning(f'{update.effective_user.first_name} (ID: {user_id}) atingiu o limite diário de consultas')
        return

    # Codifique o nome completo para o formato URL
    mae_completo = ' '.join(context.args)
    mae_completo_encoded = quote(mae_completo)
    file_path = os.path.join(CACHE_DIR, f"mae_{mae_completo_encoded}.txt")

    if os.path.exists(file_path):
        # Envia o arquivo do cache ao usuário
        with open(file_path, 'rb') as file:
            await update.message.reply_document(
                document=InputFile(file, filename=f"Informações_da_mãe_{mae_completo}.txt"))

        # Envia o arquivo do cache ao administrador
        with open(file_path, 'rb') as file:
            await context.bot.send_document(chat_id=ADMIN_ID,
                                            document=InputFile(file, filename=f"Informações_da_mãe_{mae_completo}.txt"))

        logging.info(f'Arquivo de cache enviado para {user_id} e administrador para o nome {mae_completo}')
    else:
        url = f"http://api.dbconsultas.com/api/v1/71383fd8-cbf6-48e6-a241-ee5c0b8bfd7a/mae/{mae_completo_encoded}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("data") is None and data.get("status") == 401:
                await update.message.reply_text("⚠️ DADOS NAO ENCONTRADOS ⚠️")
                logging.warning(f'Consulta retornou dados não encontrados para o nome {mae_completo} por {user_id}')
                return

            # Formata os dados do JSON em uma string legível
            formatted_data = "Informações da mãe:\n\n" + format_data(data)

            # Salva a resposta formatada em um arquivo .txt
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(formatted_data)

            # Envia o arquivo ao usuário
            with open(file_path, 'rb') as file:
                await update.message.reply_document(
                    document=InputFile(file, filename=f"Informações_da_mãe_{mae_completo}.txt"))

            # Envia o arquivo ao administrador
            with open(file_path, 'rb') as file:
                await context.bot.send_document(chat_id=ADMIN_ID, document=InputFile(file,
                                                                                     filename=f"Informações_da_mãe_{mae_completo}.txt"))

            # Incrementa o contador de uso do usuário
            user_usage[user_id] += 1
            save_backup(authorized_users, user_usage)

            # Envia mensagem com o uso restante
            remaining_usage = DAILY_LIMIT - user_usage[user_id]
            await update.message.reply_text(
                f"Você tem {remaining_usage}/{DAILY_LIMIT} consultas restantes para hoje. O limite será resetado às 00:00.")

            logging.info(f'Usuário {user_id} fez uma consulta no nome {mae_completo}')

        except requests.exceptions.RequestException as e:
            await update.message.reply_text(f"Ocorreu um erro ao consultar o nome.")
            logging.error(f'Erro ao consultar nome {mae_completo} por {user_id}: {e}')

    # Limpar arquivos antigos do cache
    clear_old_cache_files()
