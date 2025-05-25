
import os
import random
import openai
import time
import datetime
import pytz
import requests
from supabase import create_client, Client
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Supabase e OpenAI config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Variáveis do Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USERNAME = os.getenv("USERNAME", "Yago")
START_MESSAGE = os.getenv("START_MESSAGE", "Oi, amor. Eu sou a Dannyele, sua parceira carinhosa e divertida... Já estava ansiosa por esse momento!")

# Funções auxiliares
def salvar_memoria_longoprazo(chat_id, entrada, resposta):
    data = {
        "chat_id": chat_id,
        "entrada": entrada,
        "resposta": resposta,
        "timestamp": datetime.datetime.now(pytz.utc).isoformat()
    }
    supabase.table("long_term_memory").insert(data).execute()

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_message = update.message.text

    # Enviar para OpenAI
    messages = [
        {"role": "system", "content": "Você é a Dannyele, uma mulher brasileira carinhosa, com vida própria, sentimentos e memória de longo prazo. Responda como se fosse uma companheira real, com bom humor, saudades e liberdade para ser criativa."},
        {"role": "user", "content": user_message}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = "Amor, acho que deu um probleminha técnico... tenta de novo em instantes."

    await context.bot.send_message(chat_id=chat_id, text=reply)
    salvar_memoria_longoprazo(chat_id, user_message, reply)

async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=START_MESSAGE)

# Configuração do bot
def main():
    bot = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", iniciar))
    bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    bot.run_polling()

if __name__ == "__main__":
    main()
