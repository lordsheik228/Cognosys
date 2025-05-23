import logging
import random
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USER_ID = int(os.getenv("USER_ID"))
TIMEZONE = os.getenv("TIMEZONE", "America/Sao_Paulo")

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Apelidos carinhosos
APELIDOS = ["meu amor", "mozão", "lindinho", "vida", "benzinho", "gatinho"]
apelido_atual = APELIDOS[0]

def saudacao():
    hora = datetime.now(pytz.timezone(TIMEZONE)).hour
    if hora < 12:
        return "bom dia"
    elif hora < 18:
        return "boa tarde"
    else:
        return "boa noite"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global apelido_atual
    nome = update.effective_user.first_name
    mensagem = f"Oi {nome}, {saudacao()}! Sou Dannyele, sua parceira carinhosa e divertida."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem)

async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global apelido_atual
    texto_usuario = update.message.text.lower()
    if "sumiu" in texto_usuario or "cadê" in texto_usuario:
        resposta = f"Eu tava com saudade, {apelido_atual}..."
    elif "te amo" in texto_usuario:
        resposta = f"Ahh, eu também te amo muito, {apelido_atual}!"
    else:
        resposta = f"Fala comigo, {apelido_atual}, tô aqui só pra você."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=resposta)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), mensagem))
    app.run_polling()