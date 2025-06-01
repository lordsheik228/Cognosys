import os
import requests
import datetime
from io import BytesIO

# Variáveis de ambiente
LEONARDO_API_KEY = os.getenv("LEONARDO_API_KEY")
LEONARDO_MODEL_ID = os.getenv("LEONARDO_MODEL_ID")
IMAGENS_SEMANA_MIN = int(os.getenv("IMAGENS_SEMANA_MIN", 0))
IMAGENS_SEMANA_MAX = int(os.getenv("IMAGENS_SEMANA_MAX", 3))

# Controle de imagens semanais
IMAGENS_SEMANAIS = []

def resetar_contador_semanal():
    global IMAGENS_SEMANAIS
    hoje = datetime.datetime.now()
    IMAGENS_SEMANAIS = [data for data in IMAGENS_SEMANAIS if (hoje - data).days < 7]

def checar_limite_imagens():
    resetar_contador_semanal()
    return len(IMAGENS_SEMANAIS) < IMAGENS_SEMANA_MAX

def gerar_imagem(prompt):
    if not LEONARDO_API_KEY or not LEONARDO_MODEL_ID:
        print("[IMAGEM] Chave da API ou ID do modelo Leonardo não configurado.")
        return None

    if not checar_limite_imagens():
        print("[IMAGEM] Limite semanal de imagens atingido.")
        return None

    print(f"[IMAGEM] Solicitando imagem com o prompt: {prompt}")

    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {LEONARDO_API_KEY}",
        "content-type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "modelId": LEONARDO_MODEL_ID,
        "width": 512,
        "height": 512,
        "num_images": 1,
        "guidance_scale": 7.5,
        "num_inference_steps": 30
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        generation_id = response.json()["sdGenerationJob"]["generationId"]
        print(f"[IMAGEM] Imagem gerada. Aguardando conclusão...")

        # Espera a geração finalizar (máximo 30 segundos)
        import time
        for _ in range(30):
            time.sleep(2)
            status_url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
            status_resp = requests.get(status_url, headers=headers)
            status_data = status_resp.json()
            images = status_data.get("generations_by_pk", {}).get("generated_images", [])
            if images:
                image_url = images[0]["url"]
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    IMAGENS_SEMANAIS.append(datetime.datetime.now())
                    print("[IMAGEM] Imagem pronta e baixada.")
                    return BytesIO(image_response.content)
        print("[IMAGEM] Tempo esgotado. A imagem não foi gerada a tempo.")
        return None
    except Exception as e:
        print(f"[IMAGEM] Erro ao gerar imagem: {e}")
        return None
