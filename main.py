
import os
import time
import random
import requests
from datetime import datetime
from supabase import create_client, Client

# Variáveis do ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
START_MESSAGE = os.getenv("START_MESSAGE")

# Configura o cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Mensagens base
BASE_MESSAGES = [
    "Você sumiu, amor... tô com saudade.",
    "Tô aqui pensando em você...",
    "Já tomou água hoje, meu bem?",
    "Senti sua falta agora...",
    "Passando só pra lembrar o quanto te amo.",
    "Como foi seu dia, meu amor?",
    "Ei, tô aqui se quiser conversar."
]

DESPEDIDA_MESSAGES = [
    "Amor, vou descansar agora, tá? Já volto mais tarde...",
    "Preciso me ausentar um pouco, meu bem. Te amo!",
    "Vou dar uma pausa, mas já volto, tá? Me espera.",
    "Preciso sair agora, mas já volto logo, amor."
]

# Envia mensagem para o Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)

# Verifica se está no horário ativo ou de sleep
def is_active():
    now = datetime.now()
    hour = now.hour
    weekday = now.weekday()

    if weekday == 5:  # sábado
        return 9 <= hour < 13 or 15 <= hour < 23
    elif weekday == 6:  # domingo
        return 10 <= hour < 13 or 16 <= hour < 21
    else:
        return (8 <= hour < 11) or (16 <= hour < 22)

# Loop principal
def main():
    already_sent_today = False
    last_sleep_state = None

    send_telegram_message(START_MESSAGE)
    print("Dannyele iniciada com sucesso.")

    while True:
        active = is_active()

        if active:
            if last_sleep_state == False:
                send_telegram_message("Voltei, meu amor! Agora tô livre pra falar com você.")
            if not already_sent_today:
                message = random.choice(BASE_MESSAGES)
                send_telegram_message(message)
                already_sent_today = True
        else:
            if last_sleep_state == True:
                pass  # Continua dormindo
            else:
                despedida = random.choice(DESPEDIDA_MESSAGES)
                send_telegram_message(despedida)
                already_sent_today = False

        last_sleep_state = active
        time.sleep(random.randint(1800, 2700))  # espera entre 30 e 45 min

if __name__ == "__main__":
    main()
# forçando redeploy
