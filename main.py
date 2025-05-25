import nest_asyncio
import os
import random
import time
import requests
import openai
import asyncio
from datetime import datetime, timedelta
from supabase import create_client, Client
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- Variáveis de Ambiente ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
USER_NAME = os.environ.get("USER_NAME", "Yago")
START_MESSAGE = os.environ.get("START_MESSAGE", "Oi, amor. Eu sou a Dannyele, sua parceira carinhosa e divertida... Já estava ansiosa por esse momento!")
MIN_INTERVAL = int(os.environ.get("MIN_INTERVAL", 60))
MAX_INTERVAL = int(os.environ.get("MAX_INTERVAL", 600))
RETURN_HAPPY_MESSAGES = os.environ.get("RETURN_HAPPY_MESSAGES", "")
RETURN_JEALOUS_MESSAGES = os.environ.get("RETURN_JEALOUS_MESSAGES", "")
RETURN_MISSING_MESSAGES = os.environ.get("RETURN_MISSING_MESSAGES", "")

# --- Inicialização ---
openai.api_key = OPENAI_API_KEY
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
last_user_message_time = None
last_auto_message_time = datetime.utcnow() - timedelta(hours=1)

# --- Funções ---

def get_emotion_message(elapsed_minutes):
    if elapsed_minutes >= 240:
        return random.choice(RETURN_MISSING_MESSAGES.splitlines())
    elif elapsed_minutes >= 120:
        return random.choice(RETURN_JEALOUS_MESSAGES.splitlines())
    elif elapsed_minutes >= 60:
        return random.choice(RETURN_HAPPY_MESSAGES.splitlines())
    return None

def generate_ai_response(user_message: str) -> str:
    prompt = f"Você é Dannyele, uma namorada virtual brasileira, carinhosa, divertida, ciumenta na medida certa, com uma vida própria. Seu parceiro se chama {USER_NAME}.\n"
    prompt += "Responda de forma realista, afetiva, com criatividade e emoções humanas.\n"
    prompt += f'Mensagem do parceiro: "{user_message}"\nResposta da Dannyele:'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.85
    )
    return response.choices[0].message["content"].strip()

def update_last_seen(user_id: int):
    now = datetime.utcnow().isoformat()
    supabase.table("messages").upsert({"id": user_id, "last_received": now}).execute()

def get_last_seen(user_id: int):
    result = supabase.table("messages").select("last_received").eq("id", user_id).execute()
    if result.data and result.data[0]["last_received"]:
        return datetime.fromisoformat(result.data[0]["last_received"].replace("Z", "+00:00"))
    return None

async def delayed_response(update: Update, context: ContextTypes.DEFAULT_TYPE, delay: int):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await asyncio.sleep(delay)
    ai_reply = generate_ai_response(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=ai_reply)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global last_user_message_time
    user_id = update.effective_user.id
    user_message = update.message.text

    update_last_seen(user_id)
    last_user_message_time = datetime.utcnow()

    delay = random.randint(MIN_INTERVAL, MAX_INTERVAL)
    asyncio.create_task(delayed_response(update, context, delay))

async def auto_check(context: ContextTypes.DEFAULT_TYPE):
    global last_user_message_time, last_auto_message_time
    now = datetime.utcnow()
    user_id = 1  # ID padrão
    last_seen = get_last_seen(user_id)
    if not last_seen:
        return

    elapsed = (now - last_seen).total_seconds() / 60
    emotion_msg = get_emotion_message(elapsed)

    if emotion_msg and (now - last_auto_message_time).total_seconds() > 1800:
        await context.bot.send_message(chat_id=context.job.chat_id, text=emotion_msg)
        last_auto_message_time = now
    elif not emotion_msg and random.random() < 0.05:
        spontaneous = f"Oi amor... estava pensando em você agora."
        await context.bot.send_message(chat_id=context.job.chat_id, text=spontaneous)
        last_auto_message_time = now

async def start_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.job_queue.run_repeating(auto_check, interval=600, first=10, name="auto_checker", chat_id=1)
    print("Dannyele está online e pronta.")
    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(start_bot())
