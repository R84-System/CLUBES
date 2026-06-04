import streamlit as st
import datetime
import requests
from PIL import Image
from io import BytesIO

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Terminal K97 - Painel LED",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# MOTOR GRÁFICO: LÓGICA DE CONVERSÃO PARA LED
# ==========================================
def converter_para_matriz_led(url_imagem, tamanho_matriz=56):
    """
    Pega uma URL de imagem, reduz a resolução para criar os 'pixels/lâmpadas'
    e gera um código SVG composto por círculos brilhantes que imitam LEDs.
    """
    try:
        # 1. Download da imagem do escudo
        response = requests.get(url_imagem, timeout=10)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        
        # 2. Redimensiona para uma escala baixa (cada pixel vira uma lâmpada LED)
        img = img.resize((tamanho_matriz, tamanho_matriz), Image.Resampling.NEAREST)
        
        # 3. Construção do SVG (Painel de LEDs)
        largura_svg = 450
        espacamento = largura_svg / tamanho_matriz
        raio_led = (espacamento / 2) * 0.8  # Margem para ver a separação física
        
        svg_content = f'<svg width="100%" height="100%" viewBox="0 0 {largura_svg} {largura_svg}" xmlns="http://www.w3.org/2000/svg" style="background-color: #010409;">'
        
        for y in range(tamanho_matriz):
            for x in range(tamanho_matriz):
                r, g, b, a = img.getpixel((x, y))
                
                cx = x * espacamento + (espacamento / 2)
                cy = y * espacamento + (espacamento / 2)
                
                # Se o pixel for transparente, desenha o LED "apagado" (azul bem escuro de fundo)
                if a < 50:
                    svg_content += f'<circle cx="{cx}" cy="{cy}" r="{raio_led}" fill="#0D1A2D" opacity="0.3"/>'
                else:
                    # Se tiver cor, calcula a luminescência do LED aceso com filtro azul do terminal
                    # Mantém as cores originais do clube com um brilho neon
                    cor_hex = f"#{r:02x}{g:02x}{b:02x}"
                    svg_content += f'<circle cx="{cx}" cy="{cy}" r="{raio_led}" fill="{cor_hex}" style="filter: drop-shadow(0px 0px 3px {cor_hex});"/>'
        
        svg_content += '</svg>'
        return svg_content
    except Exception as e:
        # Retorna um indicador visual caso a imagem falhe ao carregar
        return f'<div style="color: #FF3333; font-family: monospace;">ERRO NO PROCESSAMENTO DO LED: {str(e)}</div>'


# ==========================================
# ESTILIZAÇÃO CUSTOMIZADA (CSS)
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #030712; }
    h2, h3, label, .stMarkdown p { color: #E2E8F0 !important; font-family: 'Courier New', monospace; }
    
    .main-display-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        border: 2px solid #0B2545; border-radius: 12px; padding: 30px;
        background-color: #050E1E; box-shadow: 0 0 25px rgba(0, 102, 204, 0.2);
    }
    
    .led-matrix-frame {
        width: 100%; max-width: 450px; height: 450px;
        background-color: #010409; border: 3px solid #134074; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        box-shadow: inset 0 0 40px rgba(0, 210, 255, 0.35), 0 0 15px rgba(19, 64, 116, 0.5);
        margin-bottom: 20px; overflow: hidden;
    }
    
    .game-status-bar { width: 100%; max-width: 600px; font-family: 'Courier New', monospace; margin-bottom: 25px; }
    
    .led-ticker-container {
        width: 100%; overflow: hidden; background-color: #000000; 
        border: 4px solid #134074; border-radius: 6px; padding: 20px 0; margin-top: 15px; position: relative;
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.5);
    }
    .led-ticker-container::before {
        content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.5) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0), rgba(0, 0, 0, 0.7));
        background-size: 100% 4px, 4px 100%; z-index: 10; pointer-events: none;
    }
    .led-ticker-text { display: flex; white-space: nowrap; padding-left: 100%; animation: led-scroll 22s linear infinite; }
    .led-game {
        display: inline-block; padding: 0 4rem; font-size: 2.3rem; 
        font-family: 'Lucida Console', 'Courier New', monospace; font-weight: 900;
        color: #00D2FF; text-shadow: 0 0 12px #00D2FF, 0 0 25px #134074; letter-spacing: 6px;
    }
    @keyframes led-scroll { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
    
    .stButton>button { background-color: #134074 !important; color: #FFFFFF !important; border: 1px solid #00D2FF !important; font-family: 'Courier New', monospace !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# DATA DIC: DICIONÁRIO DE URLS DE ESCUDOS MOCK
# ==========================================
# URLs estáticas limpas e transparentes do Wikipédia para teste do motor de LED
urls_escudos = {
    "Clube de Regatas do Flamengo": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Flamengo_brazil_crest.png",
    "Fluminense Football Club": "https://upload.wikimedia.org/wikipedia/commons/a/a3/Fluminense_crest-wm.png",
    "Sport Club Corinthians Paulista": "https://upload.wikimedia.org/wikipedia/pt/b/b4/Corinthians_sistema_2022.png"
}


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
    
    mock_clubs = list(urls_escudos.keys())
    selected_club = st.radio("Disponíveis:", mock_clubs, label_visibility="collapsed")


# ==========================================
# CORPO PRINCIPAL: PROCESSAMENTO E EXIBIÇÃO
# ==========================================
st.markdown("<h1 style='color: #00D2FF; font-family: monospace; font-size: 24px;'>TERMINAL K97 // LED MATRIX DISPLAY</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-display-container">', unsafe_allow_html=True)
    
    # Executa o motor gráfico passando a URL mapeada pelo seletor de rádio
    url_alvo = urls_escudos.get(selected_club)
    
    # 1. CONTAINER DO ESCUDO COM O MOTOR DE LED ACESO
    st.markdown('<div class="led-matrix-frame">', unsafe_allow_html=True)
    conteudo_led_svg = converter_para_matriz_led(url_alvo, tamanho_matriz=56)
    st.markdown(conteudo_led_svg, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. BLOCO DE DADOS DINÂMICOS ABAIXO DO ESCUDO
    st.markdown('<div class="game-status-bar">', unsafe_allow_html=True)
    status_cols = st.columns([1.2, 1.6, 1.2])
    
    with status_cols[0]:
        st.markdown("<p style='color: #8892B0; font-size: 11px; margin-bottom: 2px; text-align: left;'>◀ PRÓXIMO JOGO</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #FFFFFF; font-size: 14px; font-weight: bold; text-align: left;'>COR vs FLA</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #00D2FF; font-size: 12px; text-align: left;'>Dom - 16:00</p>", unsafe_allow_html=True)
        
    with status_cols[1]:
        st.markdown("<p style='color: #FF9F00; font-size: 11px; margin-bottom: 2px; text-align: center;'>• EM ANDAMENTO •</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #00D2FF; font-size: 20px; font-weight: bold; text-align: center; letter-spacing: 2px;'>FLA 2 x 0 PAL</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #FF9F00; font-size: 12px; text-align: center;'>2º Tempo - 22'</p>", unsafe_allow_html=True)
        
    with status_cols[2]:
        st.markdown("<p style='color: #8892B0; font-size: 11px; margin-bottom: 2px; text-align: right;'>ÚLTIMO JOGO ▶</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #FFFFFF; font-size: 14px; font-weight: bold; text-align: right;'>VIZ 1 x 2 FLA</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #00D2FF; font-size: 12px; text-align: right;'>03/06 - FIM</p>", unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botão de Atualização que força o recarregamento do Streamlit
    if st.button("ATUALIZAR DISPLAY", use_container_width=False):
        st.rerun()
        
    # 3. LETREIRO DE LED NO RODAPÉ
    st.markdown('<div class="led-ticker-container">', unsafe_allow_html=True)
    st.markdown('<div class="led-ticker-text">', unsafe_allow_html=True)
    st.markdown('<div class="led-game">FLA 2 . 0 PAL [AO VIVO]</div>', unsafe_allow_html=True)
    st.markdown('<div class="led-game">FLU 1 . 1 COR [AO VIVO]</div>', unsafe_allow_html=True)
    st.markdown('<div class="led-game">SÃO 0 . 0 INT [PROX JOGO]</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Status Geral do Terminal K97
st.markdown("<br><hr style='border-color: #0B2545;'>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #00D2FF; font-family: monospace; margin-bottom: 2px;'>PAINEL DIGITAL DE ESCUDOS - {selected_club.upper()} | {selected_championship.upper()}</p>", unsafe_allow_html=True)
