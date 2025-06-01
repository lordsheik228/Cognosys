from datetime import datetime
from config import EMOCOES_DISPONIVEIS
from memory import salvar_memoria

# Lista de palavras associadas a cada emoção
GATILHOS_EMOCOES = {
    "carente": ["sinto sua falta", "cadê você", "saudade", "longe de mim", "você sumiu"],
    "apaixonada": ["eu te amo", "meu amor", "meu namorado", "você é tudo pra mim"],
    "triste": ["estou triste", "me sinto sozinha", "chateada", "decepcionada", "desanimada"],
    "com_ciumes": ["outra mulher", "falando com ela", "com outra", "não me dá atenção"],
    "sensual": ["gostosa", "tesão", "quero você", "vem pra cama", "delícia"],
    "irritada": ["estou irritada", "você não liga pra mim", "tô brava", "você me ignora"],
    "feliz": ["estou feliz", "alegre", "que bom", "estou animada", "você me faz sorrir"]
}

# Emoção padrão
EMOCAO_PADRAO = "neutra"

def detectar_emocao(mensagem: str) -> str:
    """
    Detecta a emoção predominante com base no conteúdo da mensagem.
    """
    mensagem = mensagem.lower()
    for emocao, gatilhos in GATILHOS_EMOCOES.items():
        for gatilho in gatilhos:
            if gatilho in mensagem:
                return emocao
    return EMOCAO_PADRAO

async def processar_emocao(texto: str, usuario: str):
    """
    Processa a emoção de uma mensagem e registra no Supabase.
    """
    emocao = detectar_emocao(texto)

    if emocao not in EMOCOES_DISPONIVEIS:
        emocao = EMOCAO_PADRAO

    await salvar_memoria(
        usuario=usuario,
        tipo="emocao",
        conteudo=texto,
        emocao=emocao,
        data=datetime.utcnow().isoformat()
    )

    return emocao
