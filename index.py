import streamlit as st
import importlib
import os

st.set_page_config(
    page_title="Gerenciador Financeiro com Python",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Adicionando a logo na sidebar
with st.sidebar:
    try:
        st.image("imagens/logo melhoria.png", use_column_width=True)
    except FileNotFoundError:
        st.error("Logo não encontrada. Verifique o caminho do arquivo.")

    selected_page = st.radio(
        "Navegação",
        ["Home", "Dashboard", "Metas financeiras", "Análise de investimentos"]
    )

# Adicionando o cabeçalho na página principal
try:
    st.image("imagens/header dollar.jpg", use_column_width=True)
except FileNotFoundError:
    st.error("Imagem de cabeçalho não encontrada. Verifique o caminho do arquivo.")

# Função para carregar páginas
def load_page(page_name):
    if page_name == "Home":
        st.title("Bem-vindo ao MELHOR gerenciador de finanças do mercado")
        st.write("Controle suas finanças de forma prática e eficiente!")
        if st.button("Já tenho meu arquivo"):
            st.file_uploader("Carregue seu arquivo aqui", type="CSV")
        st.button('Inserir dados manualmente')
    else:
        try:
            # Importa dinamicamente o módulo da página selecionada
            module = importlib.import_module(f"paginas.{page_name.lower().replace(' ', '_')}")
            module.run()  # Executa a função `run` do módulo
        except ModuleNotFoundError:
            st.error("Página não encontrada.")
        except AttributeError:
            st.error("A página selecionada não possui a função `run`.")

# Carrega a página selecionada
load_page(selected_page)