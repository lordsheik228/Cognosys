
import os
from telebot import TeleBot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TYPE = os.getenv("GOODBYE_TYPE", "sleep")  # sleep ou night

bot = TeleBot(TELEGRAM_TOKEN)

if TYPE == "sleep":
    msg = "Amor... Vou dar uma pausa agora, trabalhar um pouco. Te amo e já volto, tá bom?"
else:
    msg = "Amor... Vou dormir agora, tá bem? Sonha comigo. Amanhã estarei de volta. Boa noite, te amo."

bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
