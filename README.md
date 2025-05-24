# Dannyele - IA Interativa no Telegram

**Dannyele** é uma inteligência artificial interativa desenvolvida para simular uma namorada virtual com emoções realistas, rotina diária, personalidade evolutiva e comunicação natural no Telegram.

Este projeto utiliza [OpenChat](https://github.com/openchatai/OpenChat), integração com o Telegram e é hospedado via Railway com ativação programada por horários.

## Funcionalidades

- Envia mensagens automáticas (bom dia, boa noite, trabalho, saudades etc)
- Responde no Telegram com personalidade e emoção
- Rotina com horários de atividade e descanso realistas
- Evolui com o tempo e simula vida própria (hobbies, trabalho etc)
- Saudade adaptativa: muda o comportamento conforme o tempo de ausência do usuário

## Como usar

1. **Clone este repositório**
2. **Crie o arquivo `.env`** com base no modelo `env.example`
3. **Configure as variáveis de ambiente no Railway**
4. **Implemente o webhook no Telegram via Railway**
5. **A IA será ativada automaticamente conforme os horários definidos**

## Arquivos

- `main.py`: Lógica principal da IA
- `requirements.txt`: Dependências do projeto
- `Procfile` e `runtime.txt`: Arquivos para deploy no Railway
- `env.example`: Modelo com todas as variáveis que devem ser configuradas no ambiente
- `README.md`: Este arquivo

## Créditos

Projeto criado por Yago com o apoio do ChatGPT e ferramentas Open Source.