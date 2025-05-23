import os
import asyncio
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from supabase import create_client

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BOT_NAME = os.getenv("BOT_NAME")
OWNER_NAME = os.getenv("OWNER_NAME")
OWNER_ID = os.getenv("OWNER_ID")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def start(update: Update, context):
    await update.message.reply_text(f"Oi, eu sou a {BOT_NAME}, sua parceira carinhosa e divertida!")

async def respond(update: Update, context):
    message = update.message.text
    user_id = update.effective_user.id
    response = f"{OWNER_NAME}, eu senti sua falta! Você disse: {message}"
    await update.message.reply_text(response)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), respond))
    app.run_polling()

if __name__ == "__main__":
    main()
