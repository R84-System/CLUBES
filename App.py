import streamlit as st
import datetime

# CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Terminal K97 - Painel Digital",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILIZAÇÃO CUSTOMIZADA (CSS) - Cores estritas do terminal e centralização
st.markdown("""
    <style>
    /* Fundo geral e fontes do terminal */
    .stApp {
        background-color: #0A0F1D;
    }
    
    /* Centralização do painel de exibição principal */
    .main-display-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 2px solid #1E293B;
        border-radius: 10px;
        padding: 30px;
        background-color: #0D1527;
        margin-top: 10px;
    }
    
    /* Moldura simulando a área da matriz de LED */
    .led-matrix-frame {
        width: 100%;
        max-width: 500px;
        height: 400px;
        background-color: #050811;
        border: 1px solid #334155;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }
    
    /* Texto simulado de LED apagado para fins de design do front */
    .led-placeholder-text {
        color: #1E293B;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        letter-spacing: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# BARRA LATERAL (SIDEBAR) - Seletor Modular
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #FFFFFF;'>CLUB CRESTS</h2>", unsafe_allow_html=True)
    
    # Campo de busca (Apenas front-end para o alinhamento)
    search_query = st.text_input("Search...", placeholder="Digite o nome do clube...")
    
    st.markdown("<hr style='border-color: #1E293B;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #FFFFFF;'>SELECTABLE</h3>", unsafe_allow_html=True)
    
    # Mock do seletor visual na barra lateral
    mock_clubs = ["Clube de Regatas do Flamengo", "Fluminense Football Club", "Outros"]
    selected_club = st.radio("Disponíveis:", mock_clubs, label_visibility="collapsed")


# ==========================================
# CORPO PRINCIPAL - Layout Centralizado
# ==========================================

# Título do Módulo / Identificação do Terminal
st.markdown("<h1 style='color: #00D2FF; font-family: monospace;'>TERMINAL K97 // DIGITAL DISPLAY</h1>", unsafe_allow_html=True)

# Container da Interface Principal
with st.container():
    st.markdown('<div class="main-display-container">', unsafe_allow_html=True)
    
    # Área reservada para a Matriz de LEDs Centralizada
    st.markdown('<div class="led-matrix-frame">', unsafe_allow_html=True)
    # Por enquanto, um placeholder indicando onde a grade de pontos se posicionará
    st.markdown('<span class="led-placeholder-text">[ LED MATRIX PLACEHOLDER ]</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Linha de Informações Secundárias (Metadados do jogo/tabela)
    info_cols = st.columns(3)
    with info_cols[0]:
        st.markdown("<p style='color: #FFFFFF; text-align: left; font-family: monospace;'>Último Jogo: VIZ 2-1</p>", unsafe_allow_html=True)
    with info_cols[1]:
        st.markdown("<p style='color: #FFFFFF; text-align: center; font-family: monospace;'>Gols: 9 | Tabela: G4</p>", unsafe_allow_html=True)
    with info_cols[2]:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"<p style='color: #FFFFFF; text-align: right; font-family: monospace;'>Última Atualização: {current_time}</p>", unsafe_allow_html=True)
    
    # Botão de Comando do Front
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("ATUALIZAR", use_container_width=False):
        pass # Ação modular JIT para ser conectada posteriormente
        
    st.markdown('</div>', unsafe_allow_html=True)

# Footer Informativo com Dados de Status
st.markdown("<br><hr style='border-color: #1E293B;'>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #00D2FF; font-family: monospace; margin-bottom: 2px;'>PAINEL DIGITAL DE ESCUDOS - {selected_club.upper()}</p>", unsafe_allow_html=True)
st.markdown("<p style='color: #FFFFFF; font-family: monospace;'>STATUS: <span style='color: #FF9F00;'>ATIVO (AGUARDANDO ENGINE DE LED)</span> | ATUALIZAÇÃO: Tempo Real (API GitHub)</p>", unsafe_allow_html=True)
