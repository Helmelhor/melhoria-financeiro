import streamlit as st
import pandas as pd

# Configuração inicial da página
st.set_page_config(
    page_title="Gerenciador Financeiro com Python",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded",
)
#definindo a existencia do dataframe
df = None

if "df" not in st.session_state: 
    st.session_state.df = None


# Adicionando a logo na sidebar
with st.sidebar:
    try:
        st.image("imagens/logo melhoria.png", use_column_width=True)
    except FileNotFoundError:
        st.error("Logo não encontrada. Verifique o caminho do arquivo.")

    # Navegação nas páginas
    selected_page = st.radio(
        "Navegação",
        ["Home", "Dashboard", "Metas financeiras", "Análise de investimentos"]
    )


if selected_page == "Home":
    st.image("imagens/header dollar.jpg", use_column_width=True)
    st.title("Bem-vindo ao MELHOR gerenciador de finanças do mercado")
    st.write("Controle suas finanças de forma prática e eficiente!")
    if st.button("Já tenho meu arquivo"):
        csv_upado = st.file_uploader("Carregue seu arquivo aqui ⬇️", type=["CSV","XLSX"])
        if csv_upado is not None:
            df = pd.read_csv(csv_upado)
            if not df.empty:
                st.write(df)
                st.session_state.df = df
            else:
                st.warning('Tem algo de errado com o arquivo carregado.')
elif selected_page == "Dashboard":
    st.header("Painel de acompanhamento financeiro")
    