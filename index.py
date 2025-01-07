import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração inicial da página
st.set_page_config(
    page_title="Gerenciador Financeiro com Python",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Definindo a existência do DataFrame no estado da sessão
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
    
    csv_upado = st.file_uploader("Carregue seu arquivo aqui ⬇️", type=["CSV", "XLSX"])
    if csv_upado is not None:
        try:
            df = pd.read_csv(csv_upado, encoding='ISO-8859-1')
            if not df.empty:
                st.write(df)
                st.session_state.df = df  # Armazenar o DataFrame no estado da sessão
            else:
                st.warning('Tem algo de errado com o arquivo carregado.')
        except UnicodeDecodeError:
            st.error("Erro ao ler o arquivo. Tente usar uma codificação diferente.")
elif selected_page == "Dashboard":
    st.header("Painel de acompanhamento financeiro")
    if st.session_state.df is not None:
        df = st.session_state.df
        st.write(df)
        
        if df.shape[1] > 1:
            column_to_plot = df.columns[1]
            st.write(f"Usando a segunda coluna: {column_to_plot}")
            
            # Criar o gráfico de pizza com matplotlib e exibir usando st.pyplot
            fig, ax = plt.subplots()
            df[column_to_plot].value_counts().plot.pie(ax=ax, autopct='%1.1f%%')
            ax.set_ylabel('')  # Remover o label do eixo y
            
            # Exibir o gráfico de pizza no Streamlit
            st.pyplot(fig)
        else:
            st.warning("O arquivo CSV deve ter pelo menos duas colunas.")
    else:
        st.warning('Nenhum arquivo foi carregado. Vá para a página Home e carregue um arquivo.')

# Seu código adicional aqui