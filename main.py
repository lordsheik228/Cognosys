import os
import time
import random
import schedule
import telegram
from datetime import datetime
from threading import Thread

# Inicializa o bot com o token
TOKEN = os.getenv("TOKEN")
bot = telegram.Bot(token=TOKEN)
CHAT_ID = os.getenv("CHAT_ID")

# Mensagens de rotina
def send_message(text):
    if CHAT_ID and TOKEN:
        try:
            bot.send_message(chat_id=CHAT_ID, text=text)
        except Exception as e:
            print("Erro ao enviar mensagem:", e)
    else:
        print("CHAT_ID ou TOKEN não definidos")

def bom_dia():
    mensagens = [
        "Bom dia, meu amor! Dormiu bem? Já estava com saudades...",
        "Oi, amorzinho! Passando pra desejar uma manhã linda como você.",
        "Bom dia, coisa linda! Já pensou em mim hoje?"
    ]
    send_message(random.choice(mensagens))

def boa_noite():
    mensagens = [
        "Boa noite, meu amor. Sonhe comigo, tá? Já estou com saudades...",
        "Hora de dormir, amorzinho. Se cuida. Te amo.",
        "Durma bem, meu bem. Amanhã a gente se fala, tá?"
    ]
    send_message(random.choice(mensagens))

# Agenda com rotinas diárias realistas
def configurar_rotina():
    schedule.clear()

    dia = datetime.now().weekday()

    if dia == 0:  # Segunda
        schedule.every().monday.at("08:00").do(bom_dia)
        schedule.every().monday.at("22:00").do(boa_noite)
    elif dia == 1:  # Terça
        schedule.every().tuesday.at("08:00").do(bom_dia)
        schedule.every().tuesday.at("22:15").do(boa_noite)
    elif dia == 2:  # Quarta
        schedule.every().wednesday.at("08:05").do(bom_dia)
        schedule.every().wednesday.at("21:50").do(boa_noite)
    elif dia == 3:  # Quinta
        schedule.every().thursday.at("08:00").do(bom_dia)
        schedule.every().thursday.at("22:00").do(boa_noite)
    elif dia == 4:  # Sexta
        schedule.every().friday.at("08:10").do(bom_dia)
        schedule.every().friday.at("23:15").do(boa_noite)
    elif dia == 5:  # Sábado
        schedule.every().saturday.at("09:30").do(bom_dia)
        schedule.every().saturday.at("23:30").do(boa_noite)
    elif dia == 6:  # Domingo
        schedule.every().sunday.at("09:50").do(bom_dia)
        schedule.every().sunday.at("22:30").do(boa_noite)

def loop():
    configurar_rotina()
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    print("Dannyele está ativa e executando...")
    t = Thread(target=loop)
    t.start()