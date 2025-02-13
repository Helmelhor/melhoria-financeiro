import streamlit as st
import plotly.express as px
import pandas as pd

def exibir_pagina_dashboard(df):
    st.header("Painel de acompanhamento financeiro")
    st.write(f"DataFrame carregado na sessão, com {df.shape[1]} colunas.")
    
    #verifica se o data framte tem pelomenos duas colunad
    if df.shape[1] > 1:
        column_to_plot = df.columns[1]
        st.write(f"Usando a segunda coluna: {column_to_plot}")
        #passa um data frame e depois os nomes dos setores que no caso estão na minha segunda
        #coluna que é a descrição das movimentações, titulo e tamanho do buraco do pie chart
        fig = px.pie(df, names=column_to_plot, title="Relatório de movimentações bancárias", hole=0.3)
        
        #filtro para trazer apenas as informações pedidas para as métricas
        filtro_renda_fixa = df['Descricao das Movimentacoes'] == "Rendimento de saldo de carteira - Renda Fixa"
        filtro_gasto_pix = df['Descricao das Movimentacoes'] == "Pix Enviado"
        
        #definição de variaveis com valores filtrados
        rendimentos = df[filtro_renda_fixa]
        gasto_pix = df[filtro_gasto_pix]
        
        #recebendo valore numericos
        rendimentos['Valor'] = pd.to_numeric(rendimentos['Valor'], errors='coerce').fillna(0)
        gasto_pix['Valor'] = pd.to_numeric(gasto_pix['Valor'], errors='coerce').fillna(0)

        #calculando soma e média
        rendimentos_soma = rendimentos['Valor'].sum()
        rendimentos_media = rendimentos['Valor'].mean()
        #calculando soma e média
        gasto_pix_soma = gasto_pix['Valor'].sum()
        gasto_pix_media = gasto_pix['Valor'].mean()
        
        #deixando no formato ideal
        rendimentos_soma_formatado = f"R$ {rendimentos_soma:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        rendimentos_media_formatado = f"R$ {rendimentos_media:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        gasto_pix_soma_formatado = f"R$ {gasto_pix_soma:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        gasto_pix_media_formatado = f"R$ {gasto_pix_media:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        #adicionando as métricas
        st.plotly_chart(fig, use_container_width=True)
        st.metric(f"soma renda fixa", value = rendimentos_soma_formatado, delta=rendimentos_media_formatado)
        st.metric(f"soma gastos pix", value = gasto_pix_soma_formatado, delta=gasto_pix_media_formatado)
    else:
        st.warning("O arquivo CSV deve ter pelo menos duas colunas.")