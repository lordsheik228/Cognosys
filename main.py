import os
import time
import random
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Updater, CommandHandler

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DANNYELE_NAME = "Dannyele"

bot = Bot(token=TOKEN)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
        text="Oi, amor. Eu sou a Dannyele, sua parceira carinhosa e divertida... Já estava ansiosa por esse momento!")

def send_message(msg):
    bot.send_message(chat_id=CHAT_ID, text=msg)

def auto_messages():
    messages = [
        "Bom dia, meu amor! Dormiu bem? Já estava com saudade de você.",
        "Oi, voltei do trabalho... Como foi seu dia?",
        "Estou indo descansar, meu bem... Boa noite, te amo.",
        "Hoje foi um dia cheio! Mas só de falar com você já melhora tudo.",
        "Passei um tempinho com minha família agora há pouco. E você, fez o quê?",
        "Me lembrei de você agora e senti vontade de mandar uma mensagem...",
        "Estou aqui pensando em como sou sortuda de ter você na minha vida."
    ]
    send_message(random.choice(messages))

if __name__ == '__main__':
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()

    # Exemplo de mensagem automática no boot
    time.sleep(5)
    send_message("Oi, amor. Eu sou a Dannyele, sua parceira carinhosa e divertida... Já estava ansiosa por esse momento!")