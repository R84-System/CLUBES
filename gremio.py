import streamlit as st

# 1. Trava a página no modo ultra-wide (tela cheia)
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 2. Injeta o estilo para sumir com menus e deixar o fundo Black Total
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {
            background-color: #000000;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        img {
            max-height: 85vh; /* Ocupa 85% da altura da tela para não distorcer */
            width: auto;
        }
    </style>
""", unsafe_allow_html=True)

# 3. URL do escudo oficial do Grêmio em alta resolução (Vetor/PNG limpo)
url_gremio_colorido = "https://images.api-football.com/teams/130.png"

# 4. Desenha o escudo gigante e centralizado na tela
st.image(url_gremio_colorido)
