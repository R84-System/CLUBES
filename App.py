import streamlit as st
import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Terminal K97 - Painel LED",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILIZAÇÃO CUSTOMIZADA (CSS) - Efeito Fiel de Letreiro de LED Físico
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
        padding: 25px;
        background-color: #050E1E;
        box-shadow: 0 0 20px rgba(0, 102, 204, 0.2);
    }
    
    /* Moldura da matriz de LED */
    .led-matrix-frame {
        width: 100%;
        max-width: 550px;
        height: 380px;
        background-color: #010409;
        border: 2px solid #134074;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: inset 0 0 30px rgba(0, 210, 255, 0.3);
        margin-bottom: 15px;
    }
    
    .led-placeholder-text {
        color: #134074;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        letter-spacing: 3px;
    }
    
    /* ================================================================= */
    /* NOVO TICKER: LETREIRO DE LED EM MATRIZ DE PONTOS (RODAPÉ)        */
    /* ================================================================= */
    .led-ticker-container {
        width: 100%;
        overflow: hidden;
        background-color: #000000; /* Fundo totalmente preto do painel físico */
        border: 3px solid #134074; /* Moldura de ferro do painel */
        border-radius: 4px;
        padding: 12px 0;
        margin-top: 20px;
        position: relative;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
    }

    /* Máscara de linhas/pontos para simular a grade física dos LEDs por cima do texto */
    .led-ticker-container::before {
        content: " ";
        display: block;
        position: absolute;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.4) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0), rgba(0, 0, 0, 0.6));
        background-size: 100% 3px, 3px 100%; /* Tamanho dos "pixels" de LED */
        z-index: 10;
        pointer-events: none;
    }

    .led-ticker-text {
        display: flex;
        white-space: nowrap;
        padding-left: 100%;
        animation: led-scroll 20s linear infinite;
    }

    /* Estilização da fonte imitando lâmpadas de LED acesas */
    .led-game {
        display: inline-block;
        padding: 0 3rem;
        font-size: 1.6rem;
        /* Uso de fontes mono que lembram placas eletrônicas */
        font-family: 'Lucida Console', 'Courier New', monospace; 
        font-weight: 900;
        color: #00D2FF; /* Azul sinaleira */
        text-shadow: 0 0 8px #00D2FF, 0 0 20px #134074; /* Brilho de lâmpada acesa */
        letter-spacing: 4px;
    }

    @keyframes led-scroll {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    /* ================================================================= */

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
    
    # Painel Central
    st.markdown('<div class="led-matrix-frame">', unsafe_allow_html=True)
    st.markdown('<span class="led-placeholder-text">[ BLUE LED MATRIX ENGINE ]</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Informações de Metadados
    info_cols = st.columns(3)
    with info_cols[0]:
        st.markdown(f"<p style='color: #E2E8F0; text-align: left; font-family: monospace;'>Comp: {selected_championship}</p>", unsafe_allow_html=True)
    with info_cols[1]:
        st.markdown("<p style='color: #E2E8F0; text-align: center; font-family: monospace;'>Gols: 9 | Tabela: G4</p>", unsafe_allow_html=True)
    with info_cols[2]:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"<p style='color: #E2E8F0; text-align: right; font-family: monospace;'>Última Atualização: {current_time}</p>", unsafe_allow_html=True)
    
    # Botão Atualizar
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("ATUALIZAR", use_container_width=False):
        pass
        
    # LETREIRO DE LED FÍSICO COM TEXTURA DE PONTOS NO RODAPÉ
    st.markdown('<div class="led-ticker-container">', unsafe_allow_html=True)
    st.markdown('<div class="led-ticker-text">', unsafe_allow_html=True)
    
    st.markdown('<div class="led-game">FLA 2 . 0 PAL [AO VIVO]</div>', unsafe_allow_html=True)
    st.markdown('<div class="led-game">FLU 1 . 1 COR [AO VIVO]</div>', unsafe_allow_html=True)
    st.markdown('<div class="led-game">SÃO 0 . 0 INT [PROX JOGO]</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Status do Sistema
st.markdown("<br><hr style='border-color: #0B2545;'>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #00D2FF; font-family: monospace; margin-bottom: 2px;'>PAINEL DIGITAL DE ESCUDOS - {selected_club.upper()}</p>", unsafe_allow_html=True)
