import streamlit as st

# 1. Configuração de Tela Cheia
st.set_page_config(
    page_title="K97 - Grêmio Neon", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Fiação CSS: Remove menus e cria o Efeito de Escudo Luminoso (Neon)
st.markdown("""
    <style>
        /* Esconde toda a poluição visual do Streamlit */
        #MainMenu, footer, header {visibility: hidden;}
        
        /* Fundo Preto Absoluto e Centralização */
        .stApp {
            background-color: #000000;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
        
        /* O PULO DO GATO: Filtros de Brilho Neon (Cyan/Azul) */
        .neon-shield {
            max-height: 75vh;
            width: auto;
            filter: 
                drop-shadow(0 0 10px #00a8ff) 
                drop-shadow(0 0 30px #00a8ff) 
                drop-shadow(0 0 60px #0055ff);
            animation: pulse 3s infinite alternate;
        }

        /* Animação opcional: Deixa o brilho "pulsando" levemente na tela */
        @keyframes pulse {
            0% { transform: scale(1); filter: drop-shadow(0 0 15px #00a8ff) drop-shadow(0 0 40px #0055ff); }
            100% { transform: scale(1.02); filter: drop-shadow(0 0 25px #00a8ff) drop-shadow(0 0 70px #00a8ff); }
        }
    </style>
""", unsafe_allow_html=True)

# 3. Escudo oficial com fundo transparente (essencial para o efeito funcionar)
url_gremio_vetor = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Gremio_logo.svg/800px-Gremio_logo.svg.png"

# 4. Injeta a imagem aplicando a classe do efeito luminoso
st.markdown(f'<img src="{url_gremio_vetor}" class="neon-shield">', unsafe_allow_html=True)
