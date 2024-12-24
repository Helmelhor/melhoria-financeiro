import streamlit as st

st.title('Gerenciador Financeiro')

img_botao1 = "https://e7.pngegg.com/pngimages/406/844/png-clipart-computer-icons-person-user-spark-icon-people-share-icon.png"

botao_html = f"""
<a href="https://www.example.com">
        <img src="{img_botao1}" width="200" />
    </a> 
"""

st.markdown(botao_html, unsafe_allow_html=True)