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

st.title("🤖 ChatBot da Paty")
st.caption("Converse com a IA — powered by Groq")
st.divider()

st.chat_message("assistant", avatar="🤖").write(texto_resposta_ia)
st.chat_message("user", avatar="👩‍💻").write(texto_usuario)

with st.sidebar:
    st.header("Sobre")
    st.write("Chatbot feito em Python com Streamlit + Groq")
    if st.button("🗑️ Limpar conversa"):
        st.session_state.lista_mensagens = []
        st.rerun()

if not "lista_mensagens" in st.session_state:
    st.session_state.lista_mensagens = []



texto_usuario =st.chat_input("Escreva sua mensagem aqui") # input do chat

for mensagem in st.session_state.lista_mensagens:
    role = mensagem["role"]
    content = mensagem["content"]    
    st.chat_message(mensagem["role"]).write(mensagem["content"]) # exibir no chat a mensagem que o usuario digitou e a resposta da IA

if texto_usuario:
    st.chat_message("user").write(texto_usuario)
    mensagem_usuario = {"role": "user", "content": texto_usuario}
    st.session_state.lista_mensagens.append(mensagem_usuario)

    resposta_ia = modelo_ia.chat.completions.create(
        messages=st.session_state.lista_mensagens,
        model="llama-3.3-70b-versatile"
    )

    texto_resposta_ia = resposta_ia.choices[0].message.content   # ← extrai só o texto

    st.chat_message("assistant").write(texto_resposta_ia)        # ← usa o texto
    mensagem_ia = {"role": "assistant", "content": texto_resposta_ia}  # ← usa o texto
    st.session_state.lista_mensagens.append(mensagem_ia)
