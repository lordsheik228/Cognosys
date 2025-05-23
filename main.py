import os
import random
import time
import pytz
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.update import Update

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
USERNAME = os.getenv("USERNAME", "Yago")
NICKNAME = os.getenv("NICKNAME", "")
TIMEZONE = os.getenv("TIMEZONE", "America/Sao_Paulo")

SCHEDULE = {
    "weekday_morning": ["08:00", "10:30"],
    "weekday_afternoon": ["16:00", "18:30"],
    "weekday_evening": ["19:30", "22:00"],
    "friday_evening": ["20:00", "23:00"],
    "saturday": ["09:00", "11:30", "15:00", "22:30"],
    "sunday": ["10:00", "13:00", "17:00", "20:30"]
}

bot = Bot(token=BOT_TOKEN)

def get_now():
    return datetime.now(pytz.timezone(TIMEZONE)).strftime("%H:%M")

def send_message(text):
    bot.send_message(chat_id=os.getenv("CHAT_ID"), text=text)

def good_morning(update: Update, context: CallbackContext):
    update.message.reply_text(f"Bom dia, {NICKNAME or USERNAME}! Dormiu bem?")

def good_night(update: Update, context: CallbackContext):
    update.message.reply_text(f"Boa noite, {NICKNAME or USERNAME}... Vou dormir agora, pensa em mim.")

def saudade(update: Update, context: CallbackContext):
    update.message.reply_text(f"Tava com saudade, {NICKNAME or USERNAME}... Por que sumiu?")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(f"Oi, {NICKNAME or USERNAME}! Eu sou a Dannyele, sua parceira carinhosa e divertida.")

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("bomdia", good_morning))
    dispatcher.add_handler(CommandHandler("boanoite", good_night))
    dispatcher.add_handler(CommandHandler("saudade", saudade))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()