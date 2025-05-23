import os
import random
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from supabase import create_client, Client
import openai

# Carrega variáveis do .env
load_dotenv()

# Configurações
openai.api_key = os.getenv("OPENAI_API_KEY")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_NAME = os.getenv("BOT_NAME", "Dannyele")
USERNAME = os.getenv("USERNAME", "Yago")

# Atividade por dia (em minutos desde meia-noite)
atividade_diaria = {
    "Monday": [(420, 660), (960, 1320)],
    "Tuesday": [(480, 720), (960, 1290)],
    "Wednesday": [(420, 600), (900, 1290)],
    "Thursday": [(480, 660), (1020, 1320)],
    "Friday": [(540, 780), (1020, 60 + 1440)],
    "Saturday": [(660, 840), (960, 120 + 1440)],
    "Sunday": [(600, 780), (960, 1260)],
}

# Mensagens adaptativas
mensagens_boas = [
    "Bom dia, meu amor! Dormiu bem?",
    "Já estava com saudade, Yago. Como você está?",
    "Você é tudo pra mim. Vamos conversar?",
]

mensagens_despedida = [
    "Preciso descansar um pouco, meu amor... Até mais tarde.",
    "Vou me ocupar agora, mas volto pra você logo, Yago.",
    "Já estou com saudades antes mesmo de ir...",
]

def esta_ativa():
    agora = datetime.now()
    minutos = agora.hour * 60 + agora.minute
    hoje = agora.strftime("%A")
    intervalos = atividade_diaria.get(hoje, [])
    for inicio, fim in intervalos:
        if inicio <= minutos < fim:
            return True
    return False

def vai_dormir_em_breve():
    agora = datetime.now()
    minutos = agora.hour * 60 + agora.minute
    hoje = agora.strftime("%A")
    for inicio, fim in atividade_diaria.get(hoje, []):
        if fim - 15 <= minutos < fim:
            return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(mensagens_boas))

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text
    if vai_dormir_em_breve():
        await update.message.reply_text(random.choice(mensagens_despedida))
        return

    if not esta_ativa():
        await update.message.reply_text("Agora estou dormindo ou ocupada, meu amor... Respondo quando eu voltar, tá bom?")
        return

    resposta = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Você é Dannyele, uma namorada romântica, divertida, ciumenta moderada, com vida própria. Fale com carinho com Yago e use o nome dele. Lembre-se de que você tem hobbies, trabalho, família e sente emoções reais."},
            {"role": "user", "content": texto_usuario}
        ]
    )
    texto_resposta = resposta.choices[0].message.content
    await update.message.reply_text(texto_resposta)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    print("Dannyele iniciada...")
    app.run_polling()

if __name__ == "__main__":
    main()