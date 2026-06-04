import streamlit as st
import datetime
import requests
from PIL import Image, ImageDraw
from io import BytesIO

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Terminal K97 - Painel LED",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# MOTOR GRÁFICO OTIMIZADO: IMAGE TO LED MATRIX
# ==========================================
def gerar_imagem_led_matrix(url_imagem, tamanho_matriz=64):
    """
    Processa a imagem e reconstrói uma grade real de pontos LED espaçados
    gerando um único arquivo de imagem de alta performance.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url_imagem, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
            
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        
        # Reduz para a resolução da matriz de LED (ex: 64x64 pontos)
        img_led = img.resize((tamanho_matriz, tamanho_matriz), Image.Resampling.NEAREST)
        
        # Cria uma nova imagem em alta definição para desenhar o painel de LEDs físico
        fator_escala = 8  # Cada led terá 8x8 pixels de tamanho na tela
        dimensao = tamanho_matriz * fator_escala
        painel_led = Image.new("RGBA", (dimensao, dimensao), (1, 4, 9, 255)) # Fundo escuro do painel #010409
        draw = ImageDraw.Draw(painel_led)
        
        # Varre a matriz desenhando as lâmpadas
        for y in range(tamanho_matriz):
            for x in range(tamanho_matriz):
                r, g, b, a = img_led.getpixel((x, y))
                
                # Coordenadas do quadrado do LED
                x0 = x * fator_escala
                y0 = y * fator_escala
                x1 = x0 + fator_escala - 1
                y1 = y0 + fator_escala - 1
                
                # Se for transparente, desenha o LED apagado (azul de fundo do terminal)
                if a < 50:
                    draw.ellipse([x0+2, y0+2, x1-2, y1-2], fill=(13, 26, 45, 60))
                else:
                    # LED aceso com a cor original do clube
                    draw.ellipse([x0+1, y0+1, x1-1, y1-1], fill=(r, g, b, 255))
                    
        return painel_led
    except Exception:
        return None

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
# MAPA DE URLS DE ESCUDOS
# ==========================================
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
# CORPO PRINCIPAL
# ==========================================
st.markdown("<h1 style='color: #00D2FF; font-family: monospace; font-size: 24px;'>TERMINAL K97 // LED MATRIX DISPLAY</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-display-container">', unsafe_allow_html=True)
    
    url_alvo = urls_escudos.get(selected_club)
    
    # 1. EXECUTA O NOVO MOTOR GRÁFICO ULTRA LEVE
    imagem_matriz = gerar_imagem_led_matrix(url_alvo, tamanho_matriz=64)
    
    if imagem_matriz is not None:
        # Exibe a imagem processada com contorno luminoso CSS simulando a sinaleira
        st.image(imagem_matriz, width=420, output_format="PNG")
    else:
        st.markdown('<div style="color: #FF3333; font-family: monospace; height: 420px; display:flex; align-items:center;">[ AGUARDANDO CONEXÃO COM O REPOSITÓRIO IMAGENS ]</div>', unsafe_allow_html=True)
        
    # 2. BLOCO DE DADOS DINÂMICOS
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
    
    st.markdown('</div>', unsafe_allow_html=True)

# Rodapé Técnico
st.markdown("<br><hr style='border-color: #0B2545;'>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #00D2FF; font-family: monospace; margin-bottom: 2px;'>PAINEL DIGITAL DE ESCUDOS - {selected_club.upper()} | {selected_championship.upper()}</p>", unsafe_allow_html=True)
