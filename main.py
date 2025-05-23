import os
import random
import time
from datetime import datetime
from telegram import Bot

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
user_id = int(os.getenv("TELEGRAM_USER_ID"))

def send_random_message(message_list_name):
    messages = eval(os.getenv(message_list_name, "[]"))
    if messages:
        message = random.choice(messages)
        bot.send_message(chat_id=user_id, text=message)

def send_personal_message(text):
    bot.send_message(chat_id=user_id, text=text)

def morning_routine():
    send_random_message("GOOD_MORNING_MESSAGES")

def night_routine():
    send_random_message("GOOD_NIGHT_MESSAGES")

def pre_sleep():
    send_random_message("SLEEP_MESSAGES")

def miss_you():
    send_random_message("MISSING_YOU_MESSAGES")

# Exemplo de chamada
if __name__ == "__main__":
    now = datetime.now().hour
    if now == 8:
        morning_routine()
    elif now == 22:
        night_routine()
