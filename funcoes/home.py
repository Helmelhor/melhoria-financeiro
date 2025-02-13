import streamlit as st
import pandas as pd

def exibir_pagina_home():
    st.image("imagens/header dollar.jpg", use_column_width=True)
    st.title("Bem-vindo ao MELHOR gerenciador de finanças do mercado")
    st.write("Controle suas finanças de forma prática e eficiente!")
    
    csv_upado = st.file_uploader("Carregue seu arquivo aqui ⬇️", type=["CSV", "XLSX"])
    #se o csv upado não for vazio, defina um data frame, se o df não estiver vazio, exiba ele...
    if csv_upado is not None:
        try:
            df = pd.read_csv(csv_upado, encoding='ISO-8859-1')
            if not df.empty:
                st.write("Pré-visualização do DataFrame:")
                st.write(df)
                st.write(f"Colunas do DataFrame: {df.columns.tolist()}")
                st.session_state.df = df  # Armazenar o DataFrame no estado da sessão
            else:
                st.warning('Tem algo de errado com o arquivo carregado.')
        except UnicodeDecodeError:
            st.error("Erro ao ler o arquivo. Tente usar uma codificação diferente.")