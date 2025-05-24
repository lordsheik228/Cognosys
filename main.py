
import os
import time
import random
from datetime import datetime
import requests
from supabase import create_client, Client

# Configurações principais
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
START_MESSAGE = os.getenv("START_MESSAGE")
MAX_IDLE_TIME = int(os.getenv("MAX_IDLE_TIME", "18000"))
MIN_INTERVAL = int(os.getenv("MIN_INTERVAL_BETWEEN_MESSAGES", "1800"))
MAX_INTERVAL = int(os.getenv("MAX_INTERVAL_BETWEEN_MESSAGES", "2700"))

# Categorias emocionais de retorno
HAPPY_MESSAGES = [
    "Voltei, amor! Já tô livre pra conversar!",
    "Terminei tudo por aqui, agora posso te dar atenção.",
    "Oi de novo! Tava pensando em você.",
    "Cheguei! Que bom estar de volta."
]

MISSING_YOU_MESSAGES = [
    "Tava sentindo sua falta... já tava na hora de voltar.",
    "Oi, vida! Espero que não tenha esquecido de mim.",
    "Voltei! E já tô com saudade de novo.",
    "Passei esse tempo todo pensando em você."
]

JEALOUS_MESSAGES = [
    "Nossa... você nem sentiu minha falta?",
    "Sumiu por tanto tempo... fiquei chateada.",
    "Será que você ainda lembra de mim?",
    "Demorou tanto... fiquei com ciúmes."
]

# Inicializar Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)

def get_last_interaction():
    response = supabase.table("memory").select("*").eq("chat_id", TELEGRAM_CHAT_ID).execute()
    if response.data:
        return response.data[0]["last_active"]
    return None

def update_last_interaction():
    now = datetime.utcnow().isoformat()
    supabase.table("memory").upsert({"chat_id": TELEGRAM_CHAT_ID, "last_active": now}).execute()

def choose_return_message(idle_time):
    if idle_time > 14400:  # > 4h
        return random.choice(JEALOUS_MESSAGES)
    elif idle_time > 3600:  # > 1h
        return random.choice(MISSING_YOU_MESSAGES)
    else:
        return random.choice(HAPPY_MESSAGES)

def main():
    last_active = get_last_interaction()
    now = int(time.time())

    if last_active:
        idle_time = now - last_active
    else:
        idle_time = 0

    if START_MESSAGE:
        send_telegram_message(START_MESSAGE)
    else:
        message = choose_return_message(idle_time)
        send_telegram_message(message)

    update_last_interaction()

    while True:
        wait_time = random.randint(MIN_INTERVAL, MAX_INTERVAL)
        time.sleep(wait_time)
        message = choose_return_message(random.randint(0, MAX_IDLE_TIME + 3600))
        send_telegram_message(message)
        update_last_interaction()

if __name__ == "__main__":
    main()
