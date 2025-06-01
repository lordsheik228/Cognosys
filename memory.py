import os
from datetime import datetime
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_MEMORIA_TABELA = os.getenv("SUPABASE_MEMORIA_TABELA")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Função para salvar memória no Supabase
def salvar_memoria(usuario: str, tipo: str, conteudo: str, emocao: str = "neutra"):
    agora = datetime.now().isoformat()
    dados = {
        "usuario": usuario,
        "tipo": tipo,
        "conteudo": conteudo,
        "emocao": emocao,
        "data": agora
    }
    try:
        resposta = supabase.table(SUPABASE_MEMORIA_TABELA).insert(dados).execute()
        print("💾 Memória salva com sucesso.")
        return resposta
    except Exception as e:
        print(f"Erro ao salvar memória: {e}")
        return None

# Função para buscar as últimas memórias de um usuário
def buscar_memorias(usuario: str, limite: int = 10):
    try:
        resposta = supabase.table(SUPABASE_MEMORIA_TABELA)\
            .select("conteudo, tipo, emocao, data")\
            .eq("usuario", usuario)\
            .order("data", desc=True)\
            .limit(limite)\
            .execute()
        memorias = resposta.data
        print(f"📚 Memórias recuperadas: {len(memorias)}")
        return memorias
    except Exception as e:
        print(f"Erro ao buscar memórias: {e}")
        return []

# Função para atualizar a emoção da última memória registrada
def atualizar_emocao_ultima_memoria(usuario: str, nova_emocao: str):
    try:
        resposta = supabase.table(SUPABASE_MEMORIA_TABELA)\
            .select("id")\
            .eq("usuario", usuario)\
            .order("data", desc=True)\
            .limit(1)\
            .execute()

        if resposta.data:
            ultima_id = resposta.data[0]["id"]
            supabase.table(SUPABASE_MEMORIA_TABELA)\
                .update({"emocao": nova_emocao})\
                .eq("id", ultima_id)\
                .execute()
            print("🧠 Emoção da última memória atualizada.")
        else:
            print("Nenhuma memória encontrada para atualizar.")
    except Exception as e:
        print(f"Erro ao atualizar emoção: {e}")
