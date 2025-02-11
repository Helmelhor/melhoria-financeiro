import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# Configurar API do Gemini
def configurar_api_gemini():
    api_key = os.getenv("GEMINI_API_KEY")  # Pegando da variável de ambiente

    if not api_key:
        st.error("API Key do Gemini não encontrada. Configure a variável de ambiente 'GEMINI_API_KEY'.")
        return None

    genai.configure(api_key=api_key)  # Configurando API corretamente
    return genai

# Função para gerar resposta do chatbot
def gerar_resposta(pergunta, historico):
    if not genai.api_key:
        return "Erro: API do Gemini não está configurada corretamente."

    contexto = "\n".join(historico[-5:])  # Pegando as últimas 5 mensagens do histórico
    prompt = f"Histórico da conversa:\n{contexto}\nUsuário: {pergunta}\nChatbot:"

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Usando modelo correto
        response = model.generate_content(prompt)
        return response.text if response and response.text else "Não recebi uma resposta."
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"

# Função para carregar CSV
def carregar_csv(file):
    df = pd.read_csv(file)
    st.session_state.csv_data = df
    return df.describe(include="all")

# Página de análise de investimentos
def exibir_pagina_analise_investimentos():
    st.header("Valer.ia 🤖 - Agente especializada em finanças")

    st.subheader("📂 Envie um arquivo CSV")
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=["csv"])

    if uploaded_file:
        resumo = carregar_csv(uploaded_file)
        st.write("**Resumo do Arquivo CSV:**")
        st.write(resumo)

    st.subheader("💬 Converse com a IA")
    user_input = st.chat_input("Digite sua pergunta:")

    if user_input:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        st.session_state.chat_history.append(f"Usuário: {user_input}")

        if st.session_state.csv_data is not None:
            dados_csv = st.session_state.csv_data.head(5).to_string()
            user_input = f"{user_input}\n\nAqui estão os primeiros dados do CSV:\n{dados_csv}"

        resposta = gerar_resposta(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append(f"Chatbot: {resposta}")

        st.write("🤖", resposta)