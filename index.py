import streamlit as st
import importlib

# Configuração inicial da página
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

    # Navegação nas páginas
    selected_page = st.radio(
        "Navegação",
        ["Home", "Dashboard", "Metas financeiras", "Análise de investimentos"]
    )

# Adicionando o cabeçalho na página principal
try:
    st.image("imagens/header dollar.jpg", use_column_width=True)
except FileNotFoundError:
    st.error("Imagem de cabeçalho não encontrada. Verifique o caminho do arquivo.")

# Função para carregar páginas com mapeamento explícito
def load_page(page_name):
    # Mapeamento entre o nome das abas e os arquivos correspondentes
    page_map = {
        "Home": None,  # A Home não tem um arquivo específico
        "Dashboard": "dashboard",
        "Metas financeiras": "metas_financeiras",
        "Análise de investimentos": "analise_investimentos",  # Nome correto do arquivo
    }

    if page_name == "Home":
        st.title("Bem-vindo ao MELHOR gerenciador de finanças do mercado")
        st.write("Controle suas finanças de forma prática e eficiente!")
        if st.button("Já tenho meu arquivo"):
            st.file_uploader("Carregue seu arquivo aqui", type="CSV")
        st.button('Inserir dados manualmente')
    else:
        module_name = page_map.get(page_name)
        if module_name:
            try:
                # Importa dinamicamente o módulo da página selecionada
                module = importlib.import_module(f"paginas.{module_name}")
                module.run()  # Executa a função `run` do módulo
            except ModuleNotFoundError:
                st.error(f"A página '{page_name}' não foi encontrada. Verifique os arquivos.")
            except AttributeError:
                st.error(f"A página '{page_name}' não possui a função `run`. Verifique o arquivo.")
        else:
            st.error("Página não encontrada.")

# Carrega a página selecionada
load_page(selected_page)