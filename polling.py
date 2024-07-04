import time
import threading
import logging
from db import load_data

# Intervalo de verificação (em segundos)
POLL_INTERVAL = 5  # Verificar a cada 5 segundos

def poll_updates():
    while True:
        logging.info("Verificação periódica realizada")
        authorized_users, user_usage = load_data()
        logging.info(f'Estágio após polling: IDs - {authorized_users}, Dados - {user_usage}')
        time.sleep(POLL_INTERVAL)

def start_polling():
    poll_thread = threading.Thread(target=poll_updates)
    poll_thread.daemon = True  # Permite que o programa termine mesmo com o thread rodando
    poll_thread.start()
