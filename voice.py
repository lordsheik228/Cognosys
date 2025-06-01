import os
import requests
from datetime import datetime, timedelta

VOICE_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
MAX_AUDIO_POR_SEMANA = 4
MIN_AUDIO_POR_SEMANA = 1

# Controle interno de quantidade enviada
historico_envio = []

def pode_enviar_audio():
    """Verifica se a IA pode enviar áudio com base na semana"""
    agora = datetime.now()
    inicio_semana = agora - timedelta(days=agora.weekday())
    audios_atuais = [t for t in historico_envio if t >= inicio_semana]
    return len(audios_atuais) < MAX_AUDIO_POR_SEMANA

def registrar_envio_audio():
    """Registra o envio de um áudio"""
    historico_envio.append(datetime.now())

def gerar_audio(texto):
    """Gera um áudio a partir de texto usando ElevenLabs"""
    if not VOICE_API_KEY or not VOICE_VOICE_ID:
        print("🔇 Voice desativado: variáveis não configuradas.")
        return None

    if not pode_enviar_audio():
        print("⚠️ Limite semanal de áudios atingido.")
        return None

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_VOICE_ID}"
    headers = {
        "xi-api-key": VOICE_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": texto,
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.8
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            registrar_envio_audio()
            return response.content
        else:
            print(f"Erro ElevenLabs: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erro ao gerar áudio: {str(e)}")

    return None
