import streamlit as st
import datetime

# CONFIGURAÇÃO DA PÁGINA (Ajustado para o Python 3.12/3.11 do Streamlit Cloud)
st.set_page_config(
    page_title="Terminal K97 - Painel LED",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILIZAÇÃO CUSTOMIZADA (CSS) - Paleta Estrita em Azul Tecnológico (Sem piscar)
st.markdown("""
    <style>
    /* Fundo geral do terminal */
    .stApp {
        background-color: #030712;
    }
    
    /* Customização dos textos da barra lateral */
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
        margin-top: 5px;
    }
    
    /* Moldura da matriz de LED - idêntica à imagem em azul */
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
    
    /* Indicador visual de LED azul apagado para design */
    .led-placeholder-text {
        color: #134074;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        letter-spacing: 3px;
    }
    
    /* TICKER - Barra inferior de rolagem contínua para placares ao vivo */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background-color: #020617;
        border: 1px solid #0B2545;
        border-radius: 6px;
        padding: 10px 0;
        margin-top: 15px;
    }
    
    .ticker {
        display: flex;
        white-space: nowrap;
        padding-left: 100%;
        animation: ticker 25s linear infinite;
    }
    
    .ticker__item {
        display: inline-block;
        padding: 0 2rem;
        font-size: 1.1rem;
        font-family: 'Courier New', monospace;
        color: #00D2FF; /* Azul neon para os placares */
        font-weight: bold;
    }
    
    /* Animação CSS para mover os placares de forma fluida da direita para a esquerda */
    @keyframes ticker {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    
    /* Customização estética do botão Atualizar */
    .stButton>button {
        background-color: #134074 !important;
        color: #FFFFFF !important;
        border: 1px solid #00D2FF !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background-color: #1E5596 !important;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# BARRA LATERAL (SIDEBAR) - Filtros de Dados
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #00D2FF;'>CLUB CRESTS</h2>", unsafe_allow_html=True)
    
    # Campo de busca estrutural
    search_query = st.text_input("Search...", placeholder="Filtrar clube...")
    
    st.markdown("<hr style='border-color: #0B2545;'>", unsafe_allow_html=True)
    
    # NOVO: Seletor de Campeonato (Todos com participação brasileira)
    st.markdown("<h3 style='color: #FFFFFF;'>CAMPEONATO</h3>", unsafe_allow_html=True)
    campeonatos = [
        "Brasileirão Série A",
        "Brasileirão Série B",
        "Copa do Brasil",
        "Conmebol Libertadores",
        "Conmebol Sul-Americana",
        "Campeonato Estadual"
    ]
    selected_championship = st.selectbox("Escolha a competição:", campeonatos, label_visibility="collapsed")
    
    st.markdown("<hr style='border-color: #0B2545;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #FFFFFF;'>SELECTABLE</h3>", unsafe_allow_html=True)
    
    # Mock de times baseado no modelo Multi-Time
    mock_clubs = ["Clube de Regatas do Flamengo", "Fluminense Football Club", "Sport Club Corinthians Paulista"]
    selected_club = st.radio("Disponíveis:", mock_clubs, label_visibility="collapsed")


# ==========================================
# CORPO PRINCIPAL - Layout Centralizado Azul
# ==========================================

st.markdown("<h1 style='color: #00D2FF; font-family: monospace; font-size: 24px;'>TERMINAL K97 // LED MATRIX DISPLAY</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-display-container">', unsafe_allow_html=True)
    
    # Moldura Central da Matriz de LEDs
    st.markdown('<div class="led-matrix-frame">', unsafe_allow_html=True)
    st.markdown('<span class="led-placeholder-text">[ BLUE LED MATRIX ENGINE ]</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Metadados Informativos Estáticos (Front-end)
    info_cols = st.columns(3)
    with info_cols[0]:
        st.markdown(f"<p style='color: #E2E8F0; text-align: left; font-family: monospace;'>Comp: {selected_championship}</p>", unsafe_allow_html=True)
    with info_cols[1]:
        st.markdown("<p style='color: #E2E8F0; text-align: center; font-family: monospace;'>Gols: 9 | Tabela: G4</p>", unsafe_allow_html=True)
    with info_cols[2]:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"<p style='color: #E2E8F0; text-align: right; font-family: monospace;'>Última Atualização: {current_time}</p>", unsafe_allow_html=True)
    
    # Botão de comando centralizado
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("ATUALIZAR", use_container_width=False):
        pass
        
    # NOVO: Ticker de Placares ao Vivo (Estrutura pura em CSS no Front-End)
    st.markdown('<div class="ticker-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="ticker">', unsafe_allow_html=True)
    
    # Itens do ticker simulando dados de jogos ao vivo de times brasileiros
    st.markdown('<div class="ticker__item">🔴 FLA 2 x 0 PAL (AO VIVO)</div>', unsafe_allow_html=True)
    st.markdown('<div class="ticker__item">🔴 FLU 1 x 1 COR (AO VIVO)</div>', unsafe_allow_html=True)
    st.markdown('<div class="ticker__item">⚪ REPI: CAI 0 x 2 CRU</div>', unsafe_allow_html=True)
    st.markdown('<div class="ticker__item">⚪ PROX: SÃO vs INT (21:45)</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Rodapé Técnico de Status
st.markdown("<br><hr style='border-color: #0B2545;'>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #00D2FF; font-family: monospace; margin-bottom: 2px;'>PAINEL DIGITAL DE ESCUDOS - {selected_club.upper()}</p>", unsafe_allow_html=True)
st.markdown("<p style='color: #E2E8F0; font-family: monospace;'>STATUS: <span style='color: #FF9F00;'>ATIVO (AGUARDANDO MÓDULO DE LED E DATA-FEED)</span> | FONTE: API GitHub</p>", unsafe_allow_html=True)
