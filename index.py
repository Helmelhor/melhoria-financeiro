import streamlit as st

st.header('Bem-vindo ao Gerenciador Financeiro')
st.subheader("Gerencie suas finanças de maneira simples e eficiente")

botao_upload = st.button('Já tenho minha planilha')
botao_inputs = st.button('Quero registrar minhas informações!')

upload_csv = st.file_uploader('Escolha um Arquivo: ',type=["XLSX","CSV","PDF"])