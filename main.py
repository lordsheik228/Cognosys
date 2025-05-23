import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from supabase import create_client, Client
import os

# Configurações da Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Comando inicial
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Oi, eu sou a Dannyele, sua namorada virtual!")

# Inicialização
def main():
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()