# cron_internal.py
import os
from datetime import datetime, time

def obter_status_rotina():
    """
    Verifica o cronograma da Dannyele para o dia atual e retorna se ela está:
    - "livre"
    - "ocupada"
    """

    dia_semana = datetime.now().strftime('%A').upper()  # Ex: SEGUNDA
    hora_atual = datetime.now().time()

    try:
        inicio = os.getenv(f'TRABALHA_{dia_semana}_INICIO')
        fim = os.getenv(f'TRABALHA_{dia_semana}_FIM')
    except Exception:
        return "livre"

    if not inicio or not fim:
        return "livre"

    hora_inicio = datetime.strptime(inicio, '%H:%M').time()
    hora_fim = datetime.strptime(fim, '%H:%M').time()

    if hora_inicio <= hora_atual <= hora_fim:
        return "ocupada"
    else:
        return "livre"

def obter_periodo_atividade():
    """
    Determina se a Dannyele está:
    - "dormindo"
    - "acordada"
    """

    dia_semana = datetime.now().strftime('%A').upper()  # Ex: SEGUNDA
    hora_atual = datetime.now().time()

    try:
        hora_acorda = os.getenv(f'ACORDA_{dia_semana}')
        hora_dorme = os.getenv(f'DORME_{dia_semana}')
    except Exception:
        return "acordada"

    if not hora_acorda or not hora_dorme:
        return "acordada"

    hora_acorda = datetime.strptime(hora_acorda, '%H:%M').time()
    hora_dorme = datetime.strptime(hora_dorme, '%H:%M').time()

    if hora_acorda <= hora_atual <= hora_dorme:
        return "acordada"
    else:
        return "dormindo"

def esta_super_disponivel():
    """
    Define se a Dannyele está super disponível (sem estar ocupada e acordada),
    permitindo respostas mais rápidas e interações espontâneas.
    """
    return obter_status_rotina() == "livre" and obter_periodo_atividade() == "acordada"
    
    def esta_ocupada():
    """
    Retorna True se a Dannyele estiver no horário de trabalho (ocupada),
    com base no cronograma semanal.
    """
    return obter_status_rotina() == "ocupada"

