import streamlit as st
import pandas as pd
import plotly.express as px

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
                st.write("Pré-visualização do DataFrame:")
                st.write(df)
                st.write(f"Colunas do DataFrame: {df.columns.tolist()}")
                st.session_state.df = df  # Armazenar o DataFrame no estado da sessão
            else:
                st.warning('Tem algo de errado com o arquivo carregado.')
        except UnicodeDecodeError:
            st.error("Erro ao ler o arquivo. Tente usar uma codificação diferente.")

elif selected_page == "Dashboard":
    st.header("Painel de acompanhamento financeiro")
    if st.session_state.df is not None:
        df = st.session_state.df
        st.write(f"DataFrame carregado na sessão, com {df.shape[1]} colunas.")
        
        # Verifique se o DataFrame tem pelo menos duas colunas
        if df.shape[1] > 1:
            column_to_plot = df.columns[1]
            st.write(f"Usando a segunda coluna: {column_to_plot}")
            
            # Criar o gráfico de pizza com Plotly
            fig = px.pie(df, names=column_to_plot, title="Relatório de movimentações bancárias", hole=0.3)
            
            filtro_renda_fixa = df['Descricao das Movimentacoes'] == "Rendimento de saldo de carteira - Renda Fixa"
            filtro_gasto_pix = df['Descricao das Movimentacoes'] == "Pix Enviado"

            rendimentos = df[filtro_renda_fixa]
            gasto_pix = df[filtro_gasto_pix]

            # Converter a coluna 'Valor' para numérica, tratando erros
            rendimentos['Valor'] = pd.to_numeric(rendimentos['Valor'], errors='coerce').fillna(0)
            gasto_pix['Valor'] = pd.to_numeric(gasto_pix['Valor'], errors='coerce').fillna(0)

            # Somar os rendimentos
            rendimentos_soma = rendimentos['Valor'].sum()
            rendimentos_media = rendimentos['Valor'].mean()
            gasto_pix_soma = gasto_pix['Valor'].sum()
            gasto_pix_media = gasto_pix['Valor'].mean()

            rendimentos_soma_formatado = f"R$ {rendimentos_soma:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            rendimentos_media_formatado = f"R$ {rendimentos_media:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            gasto_pix_soma_formatado = f"R$ {gasto_pix_soma:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            gasto_pix_media_formatado = f"R$ {gasto_pix_media:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            # Exibir os graficos
            st.plotly_chart(fig, use_container_width=True)
            st.metric(f"soma renda fixa", value = rendimentos_soma_formatado, delta=rendimentos_media_formatado)
            st.metric(f"soma gastos pix", value = gasto_pix_soma_formatado, delta=gasto_pix_media_formatado)
        else:
            st.warning("O arquivo CSV deve ter pelo menos duas colunas.")
    else:
        st.warning('Nenhum arquivo foi carregado. Vá para a página Home e carregue um arquivo.')
    if not df.empty:
        st.balloons()