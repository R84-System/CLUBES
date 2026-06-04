import streamlit as st
import datetime
import os
from PIL import Image, ImageDraw

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Terminal K97 - Painel LED",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# MOTOR GRÁFICO LOCAL
# ==========================================
def gerar_imagem_led_matrix_local(nome_arquivo, tamanho_matriz=64):
    try:
        caminho_imagem = os.path.join("escudos", nome_arquivo)
        if not os.path.exists(caminho_imagem):
            return None
            
        img = Image.open(caminho_imagem).convert("RGBA")
        img_led = img.resize((tamanho_matriz, tamanho_matriz), Image.Resampling.NEAREST)
        
        fator_escala = 6  
        dimensao = tamanho_matriz * fator_escala
        painel_led = Image.new("RGBA", (dimensao, dimensao), (1, 4, 9, 255)) 
        draw = ImageDraw.Draw(painel_led)
        
        for y in range(tamanho_matriz):
            for x in range(tamanho_matriz):
                r, g, b, a = img_led.getpixel((x, y))
                
                x0 = x * fator_escala
                y0 = y * fator_escala
                x1 = x0 + fator_escala - 1
                y1 = y0 + fator_escala - 1
                
                if a < 50:
                    draw.ellipse([x0+1, y0+1, x1-1, y1-1], fill=(13, 26, 45, 40))
                else:
                    draw.ellipse([x0+1, y0+1, x1-1, y1-1], fill=(r, g, b, 255))
                    
        return painel_led
    except Exception:
        return None

# ==========================================
# ESTILIZAÇÃO CUSTOMIZADA (CSS) - ALINHAMENTO DO ESCUDO
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #030712; }
    
    /* Prepara o container principal sem margens fantasmas */
    .block-container { padding-top: 1.5rem !important; padding-bottom: 0rem !important; padding-left: 0rem !important; padding-right: 0rem !important; max-width: 100% !important; }
    .painel-wrapper { padding-left: 3rem; padding-right: 3rem; width: 100%; }
    
    h2, h3, label, .stMarkdown p { color: #E2E8F0 !important; font-family: 'Courier New', monospace; }
    
    [data-testid="stHorizontalBlock"] {
        align-items: flex-end !important;
    }
    
    /* CONTAINER DO ESCUDO COM DESLOCAMENTO CONTROLADO PARA A ESQUERDA */
    .shield-display-container {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 0 auto 15px auto;
    }
    
    /* Alvo cirúrgico: empurra o elemento interno do Streamlit um pouco para a esquerda */
    .shield-display-container [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        margin: 0 auto !important;
        transform: translateX(-18px) !important; /* Deslocamento milimétrico para centralizar com o texto */
    }
    .shield-display-container img { max-width: 260px !important; width: 100% !important; height: auto !important; }
    
    /* LETREIRO DE LED INFERIOR (PONTA A PONTA COMPLETO) */
    .led-ticker-edge-to-edge {
        width: 100vw !important;
        background-color: #000000; 
        border-top: 4px solid #134074; 
        border-bottom: 4px solid #134074; 
        padding: 22px 0; 
        margin-top: 50px; 
        overflow: hidden;
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.3);
    }
    .led-ticker-edge-to-edge::before {
        content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.4) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0), rgba(0, 0, 0, 0.6));
        background-size: 100% 4px, 4px 100%; z-index: 10; pointer-events: none;
    }
    .led-ticker-text-scroll { display: flex; white-space: nowrap; padding-left: 100%; animation: led-scroll 24s linear infinite; }
    .led-item-style {
        display: inline-block; padding: 0 5rem; font-size: 2.4rem; 
        font-family: 'Lucida Console', 'Courier New', monospace; font-weight: 900;
        color: #00D2FF; text-shadow: 0 0 12px #00D2FF, 0 0 25px #134074; letter-spacing: 6px;
    }
    @keyframes led-scroll { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# MAPA DE ARQUIVOS LOCAIS
# ==========================================
arquivos_escudos = {
    "Clube de Regatas do Flamengo": "flamengo.png",
    "Fluminense Football Club": "fluminense.png",
    "Sport Club Corinthians Paulista": "corinthians.png"
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
    
    mock_clubs = list(arquivos_escudos.keys())
    selected_club = st.radio("Disponíveis:", mock_clubs, label_visibility="collapsed")

# ==========================================
# PAINEL DE CONTEÚDO SUPERIOR
# ==========================================
st.markdown('<div class="painel-wrapper">', unsafe_allow_html=True)

arquivo_alvo = arquivos_escudos.get(selected_club)
imagem_matriz = gerar_imagem_led_matrix_local(arquivo_alvo, tamanho_matriz=64)

# Grid proporcional mantendo as laterais estáveis
status_cols = st.columns([1.3, 1.4, 1.3])

# COLUNA 1: Próximo Jogo (Esquerda)
with status_cols[0]:
    st.markdown("<p style='color: #8892B0; font-size: 11px; margin-bottom: 4px; text-align: left;'>◀ PRÓXIMO JOGO</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFFFFF; font-size: 15px; font-weight: bold; margin-bottom: 2px; text-align: left;'>COR vs FLA</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00D2FF; font-size: 12px; text-align: left;'>Dom - 16:00</p>", unsafe_allow_html=True)

# COLUNA 2: Centro Absoluto Alinhado
with status_cols[1]:
    st.markdown('<div class="shield-display-container">', unsafe_allow_html=True)
    if imagem_matriz is not None:
        st.image(imagem_matriz, use_container_width=False, output_format="PNG")
    else:
        st.markdown(f'<div style="color: #FF9F00; font-family: monospace; font-size: 12px;">[ AGUARDANDO: {arquivo_alvo} ]</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Textos perfeitamente alinhados abaixo do escudo centralizado
    st.markdown("<p style='color: #FF9F00; font-size: 11px; margin-bottom: 4px; text-align: center; font-weight: bold;'>• EM ANDAMENTO •</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00D2FF; font-size: 26px; font-weight: bold; text-align: center; letter-spacing: 2px; margin-bottom: 4px;'>FLA 2 x 0 PAL</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FF9F00; font-size: 12px; text-align: center;'>2º Tempo - 22'</p>", unsafe_allow_html=True)

# COLUNA 3: Último Jogo (Direita)
with status_cols[2]:
    st.markdown("<p style='color: #8892B0; font-size: 11px; margin-bottom: 4px; text-align: right;'>ÚLTIMO JOGO ▶</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFFFFF; font-size: 15px; font-weight: bold; margin-bottom: 2px; text-align: right;'>VIZ 1 x 2 FLA</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00D2FF; font-size: 12px; text-align: right;'>03/06 - FIM</p>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# LED TICKER RODAPÉ PONTA A PONTA
# ==========================================
st.markdown("""
<div class="led-ticker-edge-to-edge">
    <div class="led-ticker-text-scroll">
        <div class="led-item-style">FLA 2 . 0 PAL [AO VIVO]</div>
        <div class="led-item-style">FLU 1 . 1 COR [AO VIVO]</div>
        <div class="led-item-style">SÃO 0 . 0 INT [PROX JOGO]</div>
    </div>
</div>
""", unsafe_allow_html=True)
