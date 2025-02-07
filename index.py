import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from google import genai
from database import criar_tabela_metas, adicionar_meta, buscar_metas, atualizar_progresso

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
elif selected_page == "Metas financeiras":
    #função para calular objetivos
    def calcular_tempo_para_meta(quanto_tenho, valor_meta, contribuicao_mensal):
        if contribuicao_mensal > 0:
            meses_necessarios = (valor_meta - quanto_tenho) / contribuicao_mensal
            return max(0, meses_necessarios)
        else:
            return None
    
    #função excluir meta (caso usuario digite algo errado)
    def excluir_meta(metas):
        banco = sqlite3.connect("banco_melhoria.db")
        cursor = banco.cursor()
        cursor.execute("DELETE FROM Metas_Financeiras WHERE metas = ?", (metas,))
        banco.commit()
        banco.close()


    st.header("Metas Financeiras")
    
    criar_tabela_metas()  # Criar tabela se não existir
    with st.form(key='form_metas'):
        metas = st.text_input("Meta")
        quanto_tenho = st.number_input("Quanto tenho", min_value=0)
        valor_meta = st.number_input("Valor da Meta", min_value=0)
        contribuicao_mensal = st.number_input("Contribuição Mensal", min_value=0)
        submit_button = st.form_submit_button(label='Adicionar Meta')

    if submit_button:
        adicionar_meta(metas, quanto_tenho, valor_meta, contribuicao_mensal)
        st.success("Meta adicionada com sucesso!")

    st.subheader("Suas Metas")
    metas_existentes = buscar_metas()
    
    if not metas_existentes:
        st.info("Nenhuma meta encontrada. Adicione uma meta para começar.")
    else:
        for meta in metas_existentes:
            st.write(f"**Meta:** {meta[0]}")
            st.write(f"**Quanto Tenho:** R$ {meta[1]:,.2f}")
            st.write(f"**Valor da Meta:** R$ {meta[2]:,.2f}")
            st.write(f"**Contribuição Mensal:** R$ {meta[3]:,.2f}")
            meses_necessarios = calcular_tempo_para_meta(meta[1], meta[2], meta[3])
            progresso = meta[1] / meta[2] if meta[2] > 0 else 0
            if meses_necessarios is not None:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Tempo Necessário para Alcançar a Meta:** {meses_necessarios:.1f} meses")
                with col2:
                    st.progress(progresso)
            else:
                st.write("Contribuição mensal não é suficiente para atingir a meta.")
                st.progress(0)
            
            nova_contribuicao = st.number_input(f"Adicionar Contribuição para {meta[0]}", min_value=0)
            if st.button(f"Atualizar Meta {meta[0]}"):
                novo_valor = meta[1] + nova_contribuicao
                atualizar_progresso(meta[0], novo_valor)
                st.success("Progresso atualizado com sucesso!")
            
            if st.button(f"Excluir Meta {meta[0]}"):
                excluir_meta(meta[0])
                st.success("Meta excluída com sucesso!")

elif selected_page == "Análise de investimentos":

    # Configurando a API do Gemini
    client = genai.Client(api_key="AIzaSyBI2z3lHl9mdRLYZnKUum9Hrc5PL4kt-Q0")  # Substitua pela sua chave

    # Inicializando a memória da sessão
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # Histórico de conversa
    if "csv_data" not in st.session_state:
        st.session_state.csv_data = None  # Dados do CSV armazenado

    # Função para gerar respostas com contexto
    def gerar_resposta(pergunta, historico):
        contexto = "\n".join(historico[-5:])  # Usar as últimas 5 mensagens para contexto
        prompt = f"Histórico da conversa:\n{contexto}\nUsuário: {pergunta}\nChatbot:"
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text

    # Função para ler e armazenar o CSV
    def carregar_csv(file):
        df = pd.read_csv(file)
        st.session_state.csv_data = df  # Armazena os dados do CSV na sessão
        return df.describe(include="all")  # Retorna um resumo do CSV

    # Interface do chatbot
    st.header("Valer.ia 🤖 - Chatbot de Análise de Investimentos")

    # Caixa de upload de arquivo
    st.subheader("📂 Envie um arquivo CSV")
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=["csv"])

    if uploaded_file:
        resumo = carregar_csv(uploaded_file)
        st.write("**Resumo do Arquivo CSV:**")
        st.write(resumo)

    # Entrada do usuário
    st.subheader("💬 Converse com a IA")
    user_input = st.chat_input("Digite sua pergunta:")

    if user_input:
        # Se houver um CSV armazenado, adiciona os dados ao contexto
        if st.session_state.csv_data is not None:
            dados_csv = st.session_state.csv_data.head(5).to_string()  # Pegando as 5 primeiras linhas
            user_input = f"{user_input}\n\nAqui estão os primeiros dados do CSV:\n{dados_csv}"

        resposta = gerar_resposta(user_input, st.session_state.chat_history)

        # Armazena no histórico da sessão
        st.session_state.chat_history.append(f"Usuário: {user_input}")
        st.session_state.chat_history.append(f"Chatbot: {resposta}")

        # Exibe a resposta do chatbot
        st.write(f"**Chatbot:** {resposta}")
