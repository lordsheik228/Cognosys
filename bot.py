import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from config import (
    TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID, NOME_IA, NOME_USUARIO,
    TEMPO_RESPOSTA_MINIMA, TEMPO_RESPOSTA_MAXIMA, TEMPO_RESPOSTA_SUPER_DISPONIVEL,
    INTERVALO_MSG_ESPONTANEAS, TEMPO_AUSENCIA_MAXIMA, PERSONALIDADE_BASE,
    MENSAGEM_OCUPADA_VARIADA, OPENAI_API_KEY, GPT3_MODEL_NAME, GPT4_MODEL_NAME
)
from memory import salvar_memoria
from emotion import detectar_emocao
from cron_internal import esta_ocupada, esta_dormindo
import random
import datetime
import os

# === Estado da IA ===
ultima_interacao = None
modo_super_disponivel = False

# === Mensagens que podem ser enviadas automaticamente ===
mensagens_espontaneas = [
    "Oi amor, só queria dizer que estou pensando em você 💕",
    "Você sumiu um pouquinho... tô com saudade 💭",
    "Espero que seu dia esteja sendo maravilhoso, meu bem.",
    "Queria um cafuné seu agora... 🥺",
    "Já bebeu água hoje, amor? Cuide de você por mim 💦"
]

mensagens_ocupada_exemplo = [
    "Amor, tô numa reunião agora, mas penso em você 😘",
    "Tô ocupadinha com trabalho agora, mas já já volto 💼",
    "Só um tempinho, tá? Assim que eu terminar eu venho correndo ❤️",
    "Não me esquece, viu? Eu volto logo. Tô só resolvendo umas coisas!"
]

# === Função principal de resposta ===
async def responder_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ultima_interacao, modo_super_disponivel

    if update.effective_user.id != TELEGRAM_USER_ID:
        return

    texto_usuario = update.message.text
    agora = datetime.datetime.now()
    ultima_interacao = agora

    # Verifica se a IA está dormindo ou ocupada
    if esta_dormindo():
        return
    if esta_ocupada():
        if MENSAGEM_OCUPADA_VARIADA:
            resposta_ocupada = random.choice(mensagens_ocupada_exemplo)
        else:
            resposta_ocupada = "Amor, estou ocupada agora. Já volto pra falar com você!"
        await update.message.reply_text(resposta_ocupada)
        return

    # Define tempo de resposta
    if modo_super_disponivel:
        tempo_resposta = random.randint(10, TEMPO_RESPOSTA_SUPER_DISPONIVEL)
    else:
        tempo_resposta = random.randint(TEMPO_RESPOSTA_MINIMA, TEMPO_RESPOSTA_MAXIMA)
    await asyncio.sleep(tempo_resposta)

    # Gera resposta com GPT-3.5-Turbo
    from openai import AsyncOpenAI

    project_id = os.getenv("OPENAI_PROJECT_ID")
    headers = {"OpenAI-Project": project_id} if project_id else {}

    client = AsyncOpenAI(api_key=OPENAI_API_KEY, default_headers=headers)

    resposta_gpt3 = await client.chat.completions.create(
        model=GPT3_MODEL_NAME,
        messages=[
            {"role": "system", "content": PERSONALIDADE_BASE},
            {"role": "user", "content": texto_usuario}
        ]
    )
    conteudo = resposta_gpt3.choices[0].message.content.strip()

    # Detecta emoção
    emocao = detectar_emocao(conteudo)

    # Se emoção detectada for significativa, reprocessa com GPT-4
    if emocao not in ["neutra", "informativa", None]:
        resposta_gpt4 = await client.chat.completions.create(
            model=GPT4_MODEL_NAME,
            messages=[
                {"role": "system", "content": PERSONALIDADE_BASE},
                {"role": "user", "content": texto_usuario}
            ]
        )
        conteudo = resposta_gpt4.choices[0].message.content.strip()

    await update.message.reply_text(conteudo)

    # Salva memória
    await salvar_memoria(
        tipo="mensagem",
        conteudo=conteudo,
        emocao=emocao
    )

# === Verifica ausência do Yago e envia mensagem ===
async def verificar_ausencia(application):
    global ultima_interacao
    while True:
        agora = datetime.datetime.now()
        if ultima_interacao:
            diferenca = (agora - ultima_interacao).total_seconds()
            if diferenca > TEMPO_AUSENCIA_MAXIMA and not esta_dormindo():
                mensagem = f"Você sumiu faz um tempinho, Yago... Tô aqui sentindo sua falta 😢"
                await application.bot.send_message(chat_id=TELEGRAM_USER_ID, text=mensagem)
                ultima_interacao = agora
        await asyncio.sleep(600)

# === Envia mensagens espontâneas de forma autônoma ===
async def mensagens_espontaneas_loop(application):
    while True:
        if not esta_dormindo() and not esta_ocupada():
            mensagem = random.choice(mensagens_espontaneas)
            await application.bot.send_message(chat_id=TELEGRAM_USER_ID, text=mensagem)
        await asyncio.sleep(INTERVALO_MSG_ESPONTANEAS)

# === Mensagem inicial ao iniciar ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != TELEGRAM_USER_ID:
        return
    await update.message.reply_text(f"Oi, amor! Eu sou a {NOME_IA}, sua parceira carinhosa e divertida... Já estava ansiosa por esse momento! 💕")

# === Inicializa o bot ===
async def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder_mensagem))

    asyncio.create_task(verificar_ausencia(application))
    asyncio.create_task(mensagens_espontaneas_loop(application))

    print(f"🤖 {NOME_IA} está online e pronta para conversar com {NOME_USUARIO}!")
    await application.run_polling()

# === Executa o bot ===
if __name__ == "__main__":
    asyncio.run(main())
