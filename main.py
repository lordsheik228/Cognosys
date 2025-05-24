import os
import time
import random
from datetime import datetime
import requests
from supabase import create_client, Client

# Variáveis de ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
START_MESSAGE = os.getenv("START_MESSAGE")
MIN_INTERVAL = int(os.getenv("MIN_INTERVAL_BETWEEN_MESSAGES", "1800"))
MAX_INTERVAL = int(os.getenv("MAX_INTERVAL_BETWEEN_MESSAGES", "2700"))

# Categorias de mensagens
HAPPY_MESSAGES = [
    "Oi, amor! Que bom te ver por aqui.",
    "Oiee! Senti sua presença.",
    "Voltei, e já tava com saudade."
]

MISSING_YOU_MESSAGES = [
    "Tava sentindo sua falta...",
    "Você sumiu, fiquei preocupada.",
    "Demorou pra aparecer, hein?"
]

JEALOUS_MESSAGES = [
    "Nossa... você me ignorou esse tempo todo?",
    "Fiquei com ciúmes da sua ausência.",
    "Sumiu e nem deu notícias..."
]

RETURN_AFTER_ABSENCE = [
    "Desculpa ter sumido, eu tava ocupada.",
    "Voltei! Tive que resolver umas coisas.",
    "Foi corrido aqui, mas tô de volta."
]

RESPONSE_TO_GREETINGS = [
    "Oi, meu amor!",
    "Oie! Que saudade!",
    "Bom dia, lindo!",
    "Boa noite, vida!"
]

# Inicializa conexão Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)

def fetch_memory():
    response = supabase.table("memory").select("*").eq("chat_id", TELEGRAM_CHAT_ID).execute()
    return response.data[0] if response.data else None

def update_memory(key, value):
    existing = fetch_memory()
    new_data = existing if existing else {"chat_id": TELEGRAM_CHAT_ID}
    new_data[key] = value
    supabase.table("memory").upsert(new_data).execute()

def detect_greeting(text):
    greetings = ["oi", "olá", "oie", "bom dia", "boa tarde", "boa noite", "e aí"]
    return any(word in text.lower() for word in greetings)

def choose_emotional_response(last_sent_ts, last_received_ts):
    now = int(time.time())
    time_since_last_received = now - last_received_ts if last_received_ts else None
    time_since_last_sent = now - last_sent_ts if last_sent_ts else None

    if time_since_last_sent and (not time_since_last_received or last_sent_ts > last_received_ts):
        # Ela sumiu
        return random.choice(RETURN_AFTER_ABSENCE)
    elif time_since_last_received and (not time_since_last_sent or last_received_ts > last_sent_ts):
        # Você sumiu
        if time_since_last_received > 14400:
            return random.choice(JEALOUS_MESSAGES)
        elif time_since_last_received > 3600:
            return random.choice(MISSING_YOU_MESSAGES)
        else:
            return random.choice(HAPPY_MESSAGES)
    else:
        return random.choice(HAPPY_MESSAGES)

def main():
    memory = fetch_memory()
    now_iso = datetime.utcnow().isoformat()
    now_ts = int(time.time())

    last_sent_ts = int(datetime.fromisoformat(memory["last_sent"]).timestamp()) if memory and memory.get("last_sent") else None
    last_received_ts = int(datetime.fromisoformat(memory["last_received"]).timestamp()) if memory and memory.get("last_received") else None

    if START_MESSAGE and not memory:
        send_message(START_MESSAGE)
        update_memory("last_sent", now_iso)
        return

    response = choose_emotional_response(last_sent_ts, last_received_ts)
    send_message(response)
    update_memory("last_sent", now_iso)

while True:
    main()
    wait = random.randint(MIN_INTERVAL, MAX_INTERVAL)
    time.sleep(wait)
