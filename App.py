import streamlit as st
import datetime
import os
import base64
from io import BytesIO
from PIL import Image, ImageDraw

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Terminal K97 - Painel LED",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# MOTOR GRÁFICO LOCAL - AJUSTADO PARA MATRIZ INDEPENDENTE
# ==========================================
def gerar_imagem_led_matrix_local(nome_arquivo, tamanho_matriz=64):
    try:
        caminho_imagem = os.path.join("escudos", nome_arquivo)
        if not os.path.exists(caminho_imagem):
            return None
            
        img = Image.open(caminho_imagem).convert("RGBA")
        img_led = img.resize((tamanho_matriz, tamanho_matriz), Image.Resampling.NEAREST)
        
        # Fator 8 para dar destaque máximo ao escudo central
        fator_escala = 8  
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

def imagem_para_base64(img):
    if img is None:
        return ""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ==========================================
# ESTILIZAÇÃO CSS GLOBAL (SEM CONFLITOS DE GRID)
# ==========================================
st.markdown("""
    <style>
    /* Reset de Fundo e Containers */
    .stApp { background-color: #030712; overflow: hidden; }
    .block-container { padding: 0rem !important; max-width: 100% !important; }
    
    /* Esconde elementos desnecessários do Streamlit em modo de monitoramento */
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    h2, h3, label { color: #E2E8F0 !important; font-family: 'Courier New', monospace; }
    
    /* ESTRUTURA CENTRALIZADORA TOTALMENTE INDEPENDENTE */
    .terminal-container-full {
        width: 100%;
        max-width: 100vw;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        padding-top: 2rem;
        font-family: 'Courier New', monospace;
    }

    /* Box isolada para o Escudo de Destaque */
    .shield-standalone-box {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 25px;
    }
    .shield-standalone-box img {
        max-width: 300px;
        width: 100%;
        height: auto;
        filter: drop-shadow(0 0 30px rgba(0,0,0,0.8));
    }

    /* Linha de Dados de Grid - Totalmente Desvinculada do Eixo do Escudo */
    .dashboard-text-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        width: 100%;
        padding: 0 4rem;
        box-sizing: border-box;
    }

    .panel-side-block {
        width: 30%;
    }
    
    .panel-center-block {
        width: 40%;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .t-raw { font-family: 'Courier New', monospace; margin: 0 !important; padding: 0 !important; }

    /* TICKER FIXO NO RODAPÉ DA TELA */
    .led-ticker-fixed-bottom {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        background-color: #000000 !important; 
        border-top: 4px solid #134074 !important; 
        padding: 22px 0 !important; 
        overflow: hidden !important;
        z-index: 99999 !important;
        box-shadow: 0 -10px 30px rgba(0, 210, 255, 0.2);
    }
    .led-ticker-fixed-bottom::before {
        content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.4) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0), rgba(0, 0, 0, 0.6));
        background-size: 100% 4px, 4px 100%; z-index: 10; pointer-events: none;
    }
    .led-ticker-movement { display: flex; white-space: nowrap; padding-left: 100%; animation: led-scroll 24s linear infinite; }
    .led-ticker-item-box {
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
# PROCESSAMENTO GRÁFICO DINÂMICO
# ==========================================
arquivo_alvo = arquivos_escudos.get(selected_club)
imagem_objeto = gerar_imagem_led_matrix_local(arquivo_alvo, tamanho_matriz=64)
base64_imagem = imagem_para_base64(imagem_objeto)

# ==========================================
# RENDERIZAÇÃO UNIFICADA DO PAINEL CENTRAL
# ==========================================
# Montamos um único container HTML com o escudo no topo e a linha de textos embaixo
painel_html = f"""
<div class="terminal-container-full">
    
    <div class="shield-standalone-box">
        {"<img src='data:image/png;base64," + base64_imagem + "' />" if base64_imagem else "<div style='color:#FF9F00;'>[AGUARDANDO ESCUDO]</div>"}
    </div>
    
    <div class="dashboard-text-row">
        
        <div class="panel-side-block" style="text-align: left;">
            <p class="t-raw" style="color: #8892B0; font-size: 11px; letter-spacing: 1px; margin-bottom: 2px;">◀ PRÓXIMO JOGO</p>
            <p class="t-raw" style="color: #FFFFFF; font-size: 14px; font-weight: bold; margin-bottom: 1px;">COR vs FLA</p>
            <p class="t-raw" style="color: #00D2FF; font-size: 11px;">Dom - 16:00</p>
        </div>
        
        <div class="panel-center-block">
            <p class="t-raw" style="color: #FF9F00; font-size: 11px; letter-spacing: 2px; margin-bottom: 3px; font-weight: bold;">• EM ANDAMENTO •</p>
            <p class="t-raw" style="color: #00D2FF; font-size: 26px; font-weight: bold; letter-spacing: 2px; margin-bottom: 3px;">FLA 2 x 0 PAL</p>
            <p class="t-raw" style="color: #FF9F00; font-size: 12px;">2º Tempo - 22'</p>
        </div>
        
        <div class="panel-side-block" style="text-align: right;">
            <p class="t-raw" style="color: #8892B0; font-size: 11px; letter-spacing: 1px; margin-bottom: 2px;">ÚLTIMO JOGO ▶</p>
            <p class="t-raw" style="color: #FFFFFF; font-size: 14px; font-weight: bold; margin-bottom: 1px;">VIZ 1 x 2 FLA</p>
            <p class="t-raw" style="color: #00D2FF; font-size: 11px;">03/06 - FIM</p>
        </div>
        
    </div>
</div>
"""

# Renderização segura via markdown do Streamlit
st.markdown(painel_html, unsafe_allow_html=True)

# ==========================================
# 3. LETREIRO DE LED FIXADO NO RODAPÉ ABSOLUTO
# ==========================================
st.markdown("""
<div class="led-ticker-fixed-bottom">
    <div class="led-ticker-movement">
        <div class="led-ticker-item-box">FLA 2 . 0 PAL [AO VIVO]</div>
        <div class="led-ticker-item-box">FLU 1 . 1 COR [AO VIVO]</div>
        <div class="led-ticker-item-box">SÃO 0 . 0 INT [PROX JOGO]</div>
    </div>
</div>
""", unsafe_allow_html=True)
