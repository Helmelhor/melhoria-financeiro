import streamlit as st
from home import exibir_pagina_home
from dashboard import exibir_pagina_dashboard
from metas_financeiras import exibir_pagina_metas_financeiras
from analise_investimentos import exibir_pagina_analise_investimentos, configurar_api_gemini

# Configuração inicial da página
st.set_page_config(
    page_title="Gerenciador Financeiro com Python",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Inicializando variáveis de sessão, guardando os dados para que não sejam esquecidos durate a utilização do usuario
if "df" not in st.session_state:
    st.session_state.df = None
if "csv_data" not in st.session_state:
    st.session_state.csv_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Configurar API do Gemini
configurar_api_gemini()

# Adicionando a logo na sidebar
with st.sidebar:
    try:
        st.image("imagens/logo melhoria.png", use_column_width=True)
    except FileNotFoundError:
        st.error("Logo não encontrada. Verifique o caminho do arquivo.")

    # Navegação nas páginas, cria as opções na side bar
    selected_page = st.radio(
        "Navegação",
        ["Home", "Dashboard", "Metas financeiras", "Análise de investimentos"]
    )

if selected_page == "Home":
    exibir_pagina_home()
elif selected_page == "Dashboard":
    if st.session_state.df is not None:
        exibir_pagina_dashboard(st.session_state.df)
    else:
        st.warning('Nenhum arquivo foi carregado. Vá para a página Home e carregue um arquivo.')
elif selected_page == "Metas financeiras":
    exibir_pagina_metas_financeiras()
elif selected_page == "Análise de investimentos":
    exibir_pagina_analise_investimentos()