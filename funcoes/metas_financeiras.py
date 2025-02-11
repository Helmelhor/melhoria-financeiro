import streamlit as st
from database import criar_tabela_metas, adicionar_meta, buscar_metas, atualizar_progresso
import sqlite3

def calcular_tempo_para_meta(quanto_tenho, valor_meta, contribuicao_mensal):
    if contribuicao_mensal > 0:
        meses_necessarios = (valor_meta - quanto_tenho) / contribuicao_mensal
        return max(0, meses_necessarios)
    else:
        return None

def excluir_meta(metas):
    banco = sqlite3.connect("banco_melhoria.db")
    cursor = banco.cursor()
    cursor.execute("DELETE FROM Metas_Financeiras WHERE metas = ?", (metas,))
    banco.commit()
    banco.close()

def exibir_pagina_metas_financeiras():
    st.header("Metas Financeiras")
    
    criar_tabela_metas()
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