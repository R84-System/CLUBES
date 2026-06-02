import streamlit as st

# 1. Configuração de Tela Cheia
st.set_page_config(
    page_title="K97 - Imortal Real Glow", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Configura o fundo da página principal para Black Total
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stApp {
            background-color: #000000;
            margin: 0;
            padding: 0;
        }
        iframe {
            display: block;
            margin: auto;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Desenho Vetorial com as Calotas Azuis que corrigem o formato das listras
escudo_ajustado = """
<div style="background-color: #000000; display: flex; justify-content: center; align-items: center; height: 95vh; overflow: hidden;">
    <style>
        .gremio-neon-perfeito {
            width: 380px;
            height: auto;
            filter: drop-shadow(0 0 15px #00a8ff) drop-shadow(0 0 45px #0055ff);
            animation: pulse 2.5s infinite alternate;
        }
        @keyframes pulse {
            0% { transform: scale(1); filter: drop-shadow(0 0 15px #00a8ff) drop-shadow(0 0 45px #0055ff); }
            100% { transform: scale(1.02); filter: drop-shadow(0 0 25px #00a8ff) drop-shadow(0 0 70px #00a8ff); }
        }
    </style>
    
    <svg class="gremio-neon-perfeito" viewBox="0 0 491 507" xmlns="http://www.w3.org/2000/svg">
        <path d="M245.5,12 C365.5,12 473.5,108 473.5,253.5 C473.5,399 365.5,495 245.5,495 C125.5,495 17.5,399 17.5,253.5 C17.5,108 125.5,12 245.5,12 Z" fill="#ffffff"/>
        
        <path d="M245.5,22 C355.5,22 453.5,115 453.5,253.5 C453.5,392 355.5,485 245.5,485 C135.5,485 37.5,392 37.5,253.5 C37.5,115 135.5,22 245.5,22 Z" fill="#000000"/>
        
        <g id="miolo">
            <path d="M245.5,32 C345.5,32 433.5,122 433.5,253.5 C433.5,385 345.5,475 245.5,475 C145.5,475 57.5,385 57.5,253.5 C57.5,122 145.5,32 245.5,32 Z" fill="#00a8ff"/>
            
            <path d="M120,70 L120,437 C100,390 85,330 85,253 C85,177 100,117 120,70 Z" fill="#000000"/>
            <rect x="150" y="45" width="35" height="417" fill="#000000"/>
            <rect x="215" y="35" width="60" height="437" fill="#000000"/>
            <rect x="306" y="45" width="35" height="417" fill="#000000"/>
            <path d="M371,70 L371,437 C391,390 406,330 406,253 C406,177 391,117 371,70 Z" fill="#000000"/>

            <rect x="147" y="45" width="3" height="417" fill="#ffffff"/>
            <rect x="185" y="45" width="3" height="417" fill="#ffffff"/>
            <rect x="212" y="35" width="3" height="437" fill="#ffffff"/>
            <rect x="275" y="35" width="3" height="437" fill="#ffffff"/>
            <rect x="303" y="45" width="3" height="417" fill="#ffffff"/>
            <rect x="341" y="45" width="3" height="417" fill="#ffffff"/>

            <path d="M115,105 C150,55 340,55 375,105 C330,135 160,135 115,105 Z" fill="#00a8ff"/>
            <path d="M115,400 C160,370 330,370 375,400 C340,450 150,450 115,400 Z" fill="#00a8ff"/>
        </g>

        <path d="M41.5,225 C145.5,190 345.5,190 449.5,225 L445.5,285 C345.5,250 145.5,250 45.5,285 Z" fill="#ffffff" stroke="#000000" stroke-width="4"/>

        <path id="caminho-texto" d="M 60,250 Q 245,195 430,250" fill="none" />
        <text font-family="'Arial Black', Impact, sans-serif" font-size="42" font-weight="900" fill="#000000" text-anchor="middle">
            <textPath href="#caminho-texto" startOffset="50%">GRÊMIO</textPath>
        </text>

        <text x="245" y="115" font-family="'Arial Black', sans-serif" font-size="36" font-weight="bold" fill="#ffffff" text-anchor="middle">1903</text>
        
        <text x="245" y="425" font-family="'Arial Black', sans-serif" font-size="30" font-weight="bold" fill="#ffffff" text-anchor="middle">FBPA</text>
    </svg>
</div>
"""

# 4. Injeta a fiação limpa sem vazar texto
st.components.v1.html(escudo_ajustado, height=800)
