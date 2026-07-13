# titulo
# input do chat
# a cada mensagem enviada:
    # mostrar a mensagem que o usuario enviou no chat
    # enviar essa mensagem para a IA responder
    # aparece na tela a resposta da IA

# Streamlit -> apenas com Python criar o frontend e o backend
# a IA que vamos usar: OpenAI
# pip install openai streamlit

import streamlit as st
from openai import OpenAI
st.set_page_config(
    page_title="ChatBot da Paty",
    page_icon="🤖",
    layout="centered"      # ou "wide" pra ocupar a tela toda
)

modelo_ia = OpenAI(api_key=st.secrets["GROQ_API_KEY"],base_url="https://api.groq.com/openai/v1") # criar uma instancia da IA

# ── item 5: SIDEBAR ───────────────────────────────────
with st.sidebar:                          # ← antes do conteúdo principal
    st.header("Sobre")
    st.write("ChatBot em Python com Streamlit + Groq")
    if st.button("🗑️ Limpar conversa"):
        st.session_state.lista_mensagens = []
        st.rerun()

st.title("🤖 ChatBot da Paty")
st.caption("Converse com a IA — powered by Groq")
st.divider()


if not "lista_mensagens" in st.session_state:
    st.session_state.lista_mensagens = []

texto_usuario =st.chat_input("Escreva sua mensagem aqui") # input do chat

for mensagem in st.session_state.lista_mensagens:
  avatar = "🤖" if mensagem["role"] == "assistant" else "👩‍💻"
    st.chat_message(mensagem["role"], avatar=avatar).write(mensagem["content"])

if texto_usuario:
    # ── item 4: AVATAR do usuário ─────────────────────
    st.chat_message("user", avatar="👩‍💻").write(texto_usuario)
    st.session_state.lista_mensagens.append({"role": "user", "content": texto_usuario})

    resposta_ia = modelo_ia.chat.completions.create(
        messages=st.session_state.lista_mensagens,
        model="llama-3.3-70b-versatile"
    )
    texto_resposta_ia = resposta_ia.choices[0].message.content

    # ── item 4: AVATAR da IA ──────────────────────────
    st.chat_message("assistant", avatar="🤖").write(texto_resposta_ia)
    st.session_state.lista_mensagens.append({"role": "assistant", "content": texto_resposta_ia}
