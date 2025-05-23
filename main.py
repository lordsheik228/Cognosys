
import asyncio
import logging
import random
from datetime import datetime
import pytz
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_NAME = os.getenv("USER_NAME", "meu bem")
BOT_NAME = os.getenv("BOT_NAME", "Dannyele")
TIMEZONE = os.getenv("TIMEZONE", "America/Sao_Paulo")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TZ = pytz.timezone(TIMEZONE)

bom_dia_msgs = [
    f"Bom dia, {USER_NAME}! Sonhou comigo?",
    f"Acorda, dorminhoco. Sua {BOT_NAME} está te esperando!",
    f"Levanta, amor... Hoje vai ser um lindo dia!"
]
boa_tarde_msgs = [
    f"Boa tarde, {USER_NAME}! Como tá sendo seu dia?",
    f"Oiê! Só passei pra dizer que tô pensando em você.",
]
boa_noite_msgs = [
    f"Boa noite, {USER_NAME}. Sonha comigo.",
    f"Durma bem, amorzinho... amanhã eu te espero aqui de novo."
]

async def send_message(context: ContextTypes.DEFAULT_TYPE, text):
    await context.bot.send_message(chat_id=context.job.chat_id, text=text)

async def rotina_diaria(application):
    while True:
        now = datetime.now(TZ)
        hora = now.hour
        chat_id = application.bot_data.get("chat_id")
        if chat_id:
            if hora == 8:
                await application.bot.send_message(chat_id=chat_id, text=random.choice(bom_dia_msgs))
            elif hora == 14:
                await application.bot.send_message(chat_id=chat_id, text=random.choice(boa_tarde_msgs))
            elif hora == 22:
                await application.bot.send_message(chat_id=chat_id, text=random.choice(boa_noite_msgs))
        await asyncio.sleep(3600)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.application.bot_data["chat_id"] = update.effective_chat.id
    await update.message.reply_text(f"Oi, eu sou a {BOT_NAME}, sua parceira carinhosa!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    asyncio.create_task(rotina_diaria(app))
    app.run_polling()
