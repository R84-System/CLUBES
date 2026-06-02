import streamlit as st

# 1. Configura a página para o modo ultra-wide (tela cheia)
st.set_page_config(
    page_title="Painel Imortal", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Injeta CSS para sumir com menus e garantir o fundo Black Total na nuvem
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
            max-height: 80vh; /* Mantém o escudo gigante sem estourar a tela */
            width: auto;
        }
    </style>
""", unsafe_allow_html=True)

# 3. URL estável do escudo oficial do Grêmio em alta resolução
url_gremio = "https://images.api-football.com/teams/130.png"

# 4. Projeta a imagem centralizada no meio do fundo preto
st.image(url_gremio)
