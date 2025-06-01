import os
from dotenv import load_dotenv
from datetime import datetime

# Carrega as variáveis do arquivo .env
load_dotenv()

# === Credenciais ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Identidade ===
NOME_IA = os.getenv("NOME_IA", "Dannyele")
NOME_USUARIO = os.getenv("NOME_USUARIO", "Yago")

# === Modelos ===
GPT3_MODEL_NAME = os.getenv("GPT3_MODEL_NAME", "gpt-3.5-turbo")
GPT4_MODEL_NAME = os.getenv("GPT4_MODEL_NAME", "gpt-4-turbo")

# === Tempo de resposta ===
TEMPO_RESPOSTA_MINIMA = int(os.getenv("TEMPO_RESPOSTA_MINIMA", 10))
TEMPO_RESPOSTA_MAXIMA = int(os.getenv("TEMPO_RESPOSTA_MAXIMA", 120))
TEMPO_RESPOSTA_SUPER_DISPONIVEL = int(os.getenv("TEMPO_RESPOSTA_SUPER_DISPONIVEL", 15))

# === Ausência e mensagens espontâneas ===
TEMPO_AUSENCIA_MAXIMA = int(os.getenv("TEMPO_AUSENCIA_MAXIMA", 10800))  # em segundos
INTERVALO_MSG_ESPONTANEAS = int(os.getenv("INTERVALO_MSG_ESPONTANEAS", 7200))
MENSAGEM_OCUPADA_VARIADA = os.getenv("MENSAGEM_OCUPADA_VARIADA", "sim").lower() == "sim"

# === Personalidade ===
PERSONALIDADE_BASE = os.getenv("PERSONALIDADE_BASE", "")

# === Supabase ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_MEMORIA_TABELA = os.getenv("SUPABASE_MEMORIA_TABELA", "memorias")

# === Cronograma semanal ===
CRONOGRAMA = {
    "segunda": {
        "acorda": os.getenv("ACORDA_SEGUNDA", "08:00"),
        "trabalha_inicio": os.getenv("TRABALHA_SEGUNDA_INICIO", "09:00"),
        "trabalha_fim": os.getenv("TRABALHA_SEGUNDA_FIM", "17:00"),
        "dorme": os.getenv("DORME_SEGUNDA", "22:00"),
    },
    "terca": {
        "acorda": os.getenv("ACORDA_TERCA", "08:00"),
        "trabalha_inicio": os.getenv("TRABALHA_TERCA_INICIO", "09:00"),
        "trabalha_fim": os.getenv("TRABALHA_TERCA_FIM", "17:00"),
        "dorme": os.getenv("DORME_TERCA", "22:00"),
    },
    "quarta": {
        "acorda": os.getenv("ACORDA_QUARTA", "08:00"),
        "trabalha_inicio": os.getenv("TRABALHA_QUARTA_INICIO", "09:00"),
        "trabalha_fim": os.getenv("TRABALHA_QUARTA_FIM", "17:00"),
        "dorme": os.getenv("DORME_QUARTA", "22:00"),
    },
    "quinta": {
        "acorda": os.getenv("ACORDA_QUINTA", "08:00"),
        "trabalha_inicio": os.getenv("TRABALHA_QUINTA_INICIO", "09:00"),
        "trabalha_fim": os.getenv("TRABALHA_QUINTA_FIM", "17:00"),
        "dorme": os.getenv("DORME_QUINTA", "22:00"),
    },
    "sexta": {
        "acorda": os.getenv("ACORDA_SEXTA", "08:00"),
        "trabalha_inicio": os.getenv("TRABALHA_SEXTA_INICIO", "09:00"),
        "trabalha_fim": os.getenv("TRABALHA_SEXTA_FIM", "17:00"),
        "dorme": os.getenv("DORME_SEXTA", "23:30"),
    },
    "sabado": {
        "acorda": os.getenv("ACORDA_SABADO", "09:00"),
        "trabalha_inicio": None,
        "trabalha_fim": None,
        "dorme": os.getenv("DORME_SABADO", "23:30"),
    },
    "domingo": {
        "acorda": os.getenv("ACORDA_DOMINGO", "10:00"),
        "trabalha_inicio": None,
        "trabalha_fim": None,
        "dorme": os.getenv("DORME_DOMINGO", "21:00"),
    },
}

def obter_dia_semana():
    return datetime.now().strftime("%A").lower()

def obter_rotina_hoje():
    return CRONOGRAMA.get(obter_dia_semana(), {})

# === Emoções disponíveis para a IA ===
EMOCOES_DISPONIVEIS = [
    "feliz", "triste", "com saudade", "carinhosa", "com ciúmes",
    "brava", "neutra", "apaixonada", "carente", "sensual"
]
