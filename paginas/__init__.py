import streamlit as st

st.set_page_config(
    page_title="Gerenciador Financeiro com Python",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.image('imagens\header dollar.jpg')

st.header('Gerenciador de finanças 💰')
st.subheader("Bem-vindo ao seu MELHOR gerenciador de finanças, controle-as de maneira simples e eficiente")

#side bar para navegar entre abas
with st.sidebar: selected_page = st.radio( "Navegação", ["Home", "Dashboard", "Metas financeiras", "Análise de investimentos"])

if st.button('Já tenho minha planilha'):
    upload_csv = st.file_uploader('Escolha um Arquivo: ',type=["XLSX","CSV"])

botao_inputs = st.button('Quero registrar minhas informações!')