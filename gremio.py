import streamlit as st

# 1. Configuração de Tela Cheia
st.set_page_config(
    page_title="K97 - Imortal Led", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Toda a estrutura do símbolo e do efeito Neon gerada por código puro
st.markdown("""
    <style>
        /* Esconde menus e cabeçalhos */
        #MainMenu, footer, header {visibility: hidden;}
        
        /* Fundo Preto Total e Centralização Absoluta */
        .stApp {
            background-color: #000000;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            margin: 0;
            padding: 0;
        }

        /* Estrutura do Escudo Redondo em Código Puro */
        .gremio-cyber-shield {
            width: 320px;
            height: 320px;
            border-radius: 50%;
            background: repeating-linear-gradient(
                90deg,
                #00a8ff 0px, #00a8ff 40px,   /* Azul Celeste */
                #ffffff 40px, #ffffff 50px,   /* Listra Branca */
                #000000 50px, #000000 90px,   /* Preto */
                #ffffff 90px, #ffffff 100px   /* Listra Branca */
            );
            border: 8px solid #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            
            /* Fiação do Efeito Luminoso de LED (Glow) */
            box-shadow: 
                0 0 20px #00a8ff,
                0 0 40px #0055ff,
                inset 0 0 20px rgba(255,255,255,0.5);
            animation: pulse 2.5s infinite alternate;
        }

        /* Centro do escudo para dar profundidade */
        .shield-center {
            width: 180px;
            height: 180px;
            background-color: #000000;
            border-radius: 50%;
            border: 4px solid #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 15px #00a8ff;
        }

        /* Texto Centralizado */
        .shield-text {
            color: #ffffff;
            font-family: 'Courier New', monospace;
            font-size: 24px;
            font-weight: bold;
            letter-spacing: 3px;
            text-shadow: 0 0 10px #ffffff, 0 0 20px #00a8ff;
        }

        /* Animação de pulsação da luz */
        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 0 20px #00a8ff, 0 0 40px #0055ff; }
            100% { transform: scale(1.03); box-shadow: 0 0 35px #00a8ff, 0 0 70px #00a8ff; }
        }
    </style>

    <div class="gremio-cyber-shield">
        <div class="shield-center">
            <span class="shield-text">GREMIO</span>
        </div>
    </div>
""", unsafe_allow_html=True)
