import streamlit as st
import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Terminal K97 - Painel LED",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILIZAÇÃO CUSTOMIZADA (CSS) - Foco no Escudo e nova distribuição inferior
st.markdown("""
    <style>
    /* Fundo geral do terminal */
    .stApp {
        background-color: #030712;
    }
    
    h2, h3, label, .stMarkdown p {
        color: #E2E8F0 !important;
        font-family: 'Courier New', monospace;
    }
    
    /* Container principal centralizado */
    .main-display-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 2px solid #0B2545;
        border-radius: 12px;
        padding: 30px;
        background-color: #050E1E;
        box-shadow: 0 0 25px rgba(0, 102, 204, 0.2);
    }
    
    /* Moldura da matriz de LED - Destaque Central Máximo */
    .led-matrix-frame {
        width: 100%;
        max-width: 600px; /* Aumentado para dar mais destaque */
        height: 420px; /* Aumentado para dar mais destaque */
        background-color: #010409;
        border: 3px solid #134074;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: inset 0 0 40px rgba(0, 210, 255, 0.35), 0 0 15px rgba(19, 64, 116, 0.5);
        margin-bottom: 20px;
    }
    
    .led-placeholder-text {
        color: #134074;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        letter-spacing: 3px;
    }
    
    /* Bloco de dados logo abaixo do escudo */
    .game-status-bar {
        width: 100%;
        max-width: 600px;
        font-family: 'Courier New', monospace;
        margin-bottom: 20px;
    }
    
    /* LETREIRO DE LED FÍSICO NO RODAPÉ */
    .led-ticker-container {
        width: 100%;
        overflow: hidden;
        background-color: #000000;
        border: 3px solid #134074;
        border-radius: 4px;
        padding: 12px 0;
        margin-top: 10px;
        position: relative;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
    }

    /* Máscara de grade física do letreiro de LED */
    .led-ticker-container::before {
        content: " ";
        display: block;
        position: absolute;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.4) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0), rgba(0, 0, 0, 0.6));
        background-size: 100% 3px, 3px 100%;
        z-index: 10;
        pointer-events: none;
    }

    .led-ticker-text {
        display: flex;
        white-space: nowrap;
        padding-left: 100%;
        animation: led-scroll 25s linear infinite;
    }

    .led-game {
        display: inline-block;
        padding: 0 3rem;
        font-size: 1.6rem;
        font-family: 'Lucida Console', 'Courier New', monospace; 
        font-weight: 900;
        color: #00D2FF;
        text-shadow: 0 0 8px #00D2FF, 0 0 20px #134074;
        letter-spacing: 4px;
    }

    @keyframes led-scroll {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }

    .stButton>button {
        background-color: #134074 !important;
        color: #FFFFFF !important;
        border: 1px solid #00D2FF !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #00D2FF;'>CLUB CRESTS</h2>", unsafe_allow_html=True)
    search_query = st.text_input("Search...", placeholder="Filtrar clube...")
    st.markdown("<hr style='border-color: #0B2545;'>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #FFFFFF;'>CAMPEONATO</h3>", unsafe_allow_html=True)
    campeonatos = ["Brasileirão Série A", "Brasileirão Série B", "Copa do Brasil", "Conmebol Libertadores"]
    selected_championship = st.selectbox("Escolha a competição:", campeonatos, label_visibility="collapsed")
    
    st.markdown("<hr style='border-color: #0B2545;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #FFFFFF;'>SELECTABLE</h3>", unsafe_allow_html=True)
    mock_clubs = ["Clube de Regatas do Flamengo", "Fluminense Football Club", "Sport Club Corinthians Paulista"]
    selected_club = st.radio("Disponíveis:", mock_clubs, label_visibility="collapsed")

# ==========================================
# CORPO PRINCIPAL
# ==========================================
st.markdown("<h1 style='color: #00D2FF; font-family: monospace; font-size: 24px;'>TERMINAL K97 // LED MATRIX DISPLAY</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-display-container">', unsafe_allow_html=True)
    
    # 1. ESCUDO CENTRAL EM DESTAQUE MÁXIMO
    st.markdown('<div class="led-matrix-frame">', unsafe_allow_html=True)
    st.markdown('<span class="led-placeholder-text">[ DESTACADO: SHIELD LED MATRIX ]</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. BLOCO DE DADOS DISTRIBUÍDO LOGO ABAIXO DO ESCUDO
    st.markdown('<div class="game-status-bar">', unsafe_allow_html=True)
    status_cols = st.columns([1.2, 1.6, 1.2]) # Pesos para equilibrar o placar ao vivo no meio
    
    with status_cols[0]:
        # Lado Esquerdo: Próximo Jogo
        st.markdown("<p style='color: #8892B0; font-size: 11px; margin-bottom: 2px; text-align: left;'>◀ PRÓXIMO JOGO</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #FFFFFF; font-size: 14px; font-weight: bold; text-align: left;'>COR vs FLA</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #00D2FF; font-size: 12px; text-align: left;'>Dom - 16:00</p>", unsafe_allow_html=True)
        
    with status_cols[1]:
        # Centro: Se estiver jogando, exibe o Placar Ao Vivo
        st.markdown("<p style='color: #FF9F00; font-size: 11px; margin-bottom: 2px; text-align: center;'>• EM ANDAMENTO •</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #00D2FF; font-size: 20px; font-weight: bold; text-align: center; letter-spacing: 2px;'>FLA 2 x 0 PAL</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #FF9F00; font-size: 12px; text-align: center;'>2º Tempo - 22'</p>", unsafe_allow_html=True)
        
    with status_cols[2]:
        # Lado Direito: Último Jogo
        st.markdown("<p style='color: #8892B0; font-size: 11px; margin-bottom: 2px; text-align: right;'>ÚLTIMO JOGO ▶</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #FFFFFF; font-size: 14px; font-weight: bold; text-align: right;'>VIZ 1 x 2 FLA</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #00D2FF; font-size: 12px; text-align: right;'>03/06 - FIM</p>", unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botão de Comando do Módulo Front
    if st.button("ATUALIZAR DISPLAY", use_container_width=False):
        pass
        
    # 3. LETREIRO DE LED EM MATRIZ DE PONTOS NO RODAPÉ DO PAINEL
    st.markdown('<div class="led-ticker-container">', unsafe_allow_html=True)
    st.markdown('<div class="led-ticker-text">', unsafe_allow_html=True)
    
    st.markdown('<div class="led-game">FLA 2 . 0 PAL [AO VIVO]</div>', unsafe_allow_html=True)
    st.markdown('<div class="led-game">FLU 1 . 1 COR [AO VIVO]</div>', unsafe_allow_html=True)
    st.markdown('<div class="led-game">SÃO 0 . 0 INT [PROX JOGO]</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Rodapé de Status do Terminal
st.markdown("<br><hr style='border-color: #0B2545;'>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #00D2FF; font-family: monospace; margin-bottom: 2px;'>PAINEL DIGITAL DE ESCUDOS - {selected_club.upper()} | {selected_championship.upper()}</p>", unsafe_allow_html=True)
