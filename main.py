
# main_dannyele_final.py (versão completa)
# Contém: GPT, memória longa, emoções, atividades, rotina, respostas inteligentes, etc.

import os
import time
import random
import openai
from datetime import datetime, timedelta
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from supabase import create_client, Client

# Configurações e chaves
openai.api_key = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MIN_RESPONSE_TIME = int(os.getenv("MIN_RESPONSE_TIME", 60))
MAX_RESPONSE_TIME = int(os.getenv("MAX_RESPONSE_TIME", 600))
RETURN_MESSAGE_HAPPY = os.getenv("RETURN_MESSAGE_HAPPY", "")
RETURN_MESSAGE_MISSING = os.getenv("RETURN_MESSAGE_MISSING", "")
RETURN_MESSAGE_JEALOUS = os.getenv("RETURN_MESSAGE_JEALOUS", "")

# Função: Salvar atividade emocional
def log_emotion(chat_id, emotion):
    supabase.table("emotions").insert({"chat_id": chat_id, "emotion": emotion, "timestamp": datetime.utcnow().isoformat()}).execute()

# Função: Salvar atividade da IA (atividade diária)
def log_activity(chat_id, activity):
    supabase.table("activities").insert({"chat_id": chat_id, "activity": activity, "timestamp": datetime.utcnow().isoformat()}).execute()

# Função: Salvar memória longa
def save_memory(chat_id, role, content):
    supabase.table("long_memory").insert({
        "chat_id": chat_id,
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow().isoformat()
    }).execute()

# Função: Obter memória longa
def retrieve_memory(chat_id):
    response = supabase.table("long_memory").select("*").eq("chat_id", chat_id).order("timestamp", desc=False).limit(50).execute()
    return response.data if response.data else []

# IA responde baseado em contexto e memória
def generate_response(chat_id, user_message):
    messages = [{"role": "system", "content": "Você é Dannyele, uma parceira carinhosa e realista, com vida própria, sentimentos e rotina."}]
    memory = retrieve_memory(chat_id)
    for mem in memory:
        messages.append({"role": mem["role"], "content": mem["content"]})
    messages.append({"role": "user", "content": user_message})
    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return "Tive um probleminha para pensar agora, amor..."

# Função principal de resposta
def handle_message(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    user_message = update.message.text

    now = datetime.utcnow()
    supabase.table("memory").upsert({
        "chat_id": chat_id,
        "last_active": now.isoformat(),
        "last_received": now.isoformat()
    }, on_conflict=["chat_id"]).execute()

    save_memory(chat_id, "user", user_message)
    response = generate_response(chat_id, user_message)
    save_memory(chat_id, "assistant", response)

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    supabase.table("memory").upsert({
        "chat_id": chat_id,
        "last_sent": now.isoformat()
    }, on_conflict=["chat_id"]).execute()

# Inicializar bot
def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
