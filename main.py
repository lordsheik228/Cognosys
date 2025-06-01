import os
import time
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

print("[MAIN] Iniciando a IA Dannyele...")

try:
    import bot
    bot.iniciar()
except Exception as e:
    print(f"[ERRO ao iniciar o bot.py] {e}")
    time.sleep(5)
