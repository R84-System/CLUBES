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
# ESTILIZAÇÃO CUSTOMIZADA (CSS) - ALINHAMENTO ABSOLUTO
# ==========================================
st.markdown("""
    <style>
    /* Configurações Globais de Fundo e Reset */
    .stApp { background-color: #030712; }
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; max-width: 100% !important; padding-left: 2rem !important; padding-right: 2rem !important; }
    
    /* Força os containers do Streamlit a aceitarem largura total */
    [data-testid="stVerticalBlock"] { width: 100% !important; gap: 0rem !important; }
    
    /* ESTRUTURA DO CORPO PRINCIPAL TRILATERAL SEM QUEBRAR O EIXO */
    .terminal-main-grid {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        font-family: 'Courier New', monospace;
    }
    
    .terminal-side-column {
        width: 25%;
        padding-bottom: 25px;
    }
    
    .terminal-center-column {
        width: 45%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    
    /* Caixa do Escudo Centralizado */
    .terminal-shield-box {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 25px;
    }
    .terminal-shield-box img { max-width: 280px; width: 100%; height: auto; display: block; }
    
    /* LETREIRO DE LED INFERIOR (PONTA A PONTA COMPLETO) */
    .led-ticker-fullwidth {
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        background-color: #000000; 
        border-top: 4px solid #134074; 
        border-bottom: 4px solid #134074; 
        padding: 20px 0; 
        margin-top: 40px; 
        overflow: hidden;
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.3);
    }
    .led-ticker-fullwidth::before {
        content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.4) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0), rgba(0, 0, 0, 0.6));
        background-size: 100% 4px, 4px 100%; z-index: 10; pointer-events: none;
    }
    .led-ticker-text-move { display: flex; white-space: nowrap; padding-left: 100%; animation: led-scroll 25s linear infinite; }
    .led-game-item {
        display: inline-block; padding: 0 5rem; font-size: 2.6rem; 
        font-family: 'Lucida Console', 'Courier New', monospace; font-weight: 900;
        color: #00D2FF; text-shadow: 0 0 12px #00D2FF, 0 0 25px #134074; letter-spacing: 6px;
    }
    @keyframes led-scroll { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
    
    /* Reset de estilos de texto */
    .term-p { font-family: 'Courier New', monospace; margin: 0; padding: 0; }
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
    st.markdown("<h2 style='color: #00D2FF; font-family: monospace;'>CLUB CRESTS</h2>", unsafe_allow_html=True)
    search_query = st.text_input("Search...", placeholder="Filtrar clube...")
    st.markdown("<hr style='border-color: #0B2545;'>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #FFFFFF; font-family: monospace;'>CAMPEONATO</h3>", unsafe_allow_html=True)
    campeonatos = ["Brasileirão Série A", "Brasileirão Série B", "Copa do Brasil", "Conmebol Libertadores"]
    selected_championship = st.selectbox("Escolha a competição:", campeonatos, label_visibility="collapsed")
    
    st.markdown("<hr style='border-color: #0B2545;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #FFFFFF; font-family: monospace;'>SELECTABLE</h3>", unsafe_allow_html=True)
    
    mock_clubs = list(arquivos_escudos.keys())
    selected_club = st.radio("Disponíveis:", mock_clubs, label_visibility="collapsed")

# ==========================================
# PROCESSAMENTO DO ESCUDO ATUAL
# ==========================================
arquivo_alvo = arquivos_escudos.get(selected_club)
imagem_matriz = gerar_imagem_led_matrix_local(arquivo_alvo, tamanho_matriz=64)

# Convertendo imagem para exibição direta dentro do bloco estruturado HTML
url_imagem = ""
if imagem_matriz is not None:
    # Salva temporariamente na pasta para o HTML ler o caminho absoluto local estável
    caminho_cache = os.path.join("escudos", "current_display.png")
    imagem_matriz.save(caminho_cache, "PNG")
    url_imagem = f"app/static/{arquivo_alvo}" 
    # Fallback caso o local estático varie no cloud: usando renderizador nativo injetado
    import base64
    from io import BytesIO
    buffered = BytesIO()
    imagem_matriz.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    src_data = f"data:image/png;base64,{img_str}"
else:
    src_data = ""

# ==========================================
# RENDERIZAÇÃO DO PAINEL DE DADOS UNIFICADO
# ==========================================

# 1. MONTAGE DA ESTRUTURA TRILATERAL FIXA (Evita desalinhamentos do tablet)
html_painel = f"""
<div class="terminal-main-grid">
    <div class="terminal-side-column" style="text-align: left;">
        <p class="term-p" style="color: #8892B0; font-size: 12px; letter-spacing: 1px; margin-bottom: 4px;">◀ PRÓXIMO JOGO</p>
        <p class="term-p" style="color: #FFFFFF; font-size: 16px; font-weight: bold; margin-bottom: 2px;">COR vs FLA</p>
        <p class="term-p" style="color: #00D2FF; font-size: 13px;">Dom - 16:00</p>
    </div>
    
    <div class="terminal-center-column">
        <div class="terminal-shield-box">
            {"<img src='" + src_data + "' />" if src_data else "<div style='color:#FF9F00;'>[ARQUIVO NÃO ENCONTRADO]</div>"}
        </div>
        <p class="term-p" style="color: #FF9F00; font-size: 12px; letter-spacing: 2px; margin-bottom: 6px; font-weight: bold;">• EM ANDAMENTO •</p>
        <p class="term-p" style="color: #00D2FF; font-size: 28px; font-weight: bold; letter-spacing: 3px; margin-bottom: 6px;">FLA 2 x 0 PAL</p>
        <p class="term-p" style="color: #FF9F00; font-size: 13px;">2º Tempo - 22'</p>
    </div>
    
    <div class="terminal-side-column" style="text-align: right;">
        <p class="term-p" style="color: #8892B0; font-size: 12px; letter-spacing: 1px; margin-bottom: 4px;">ÚLTIMO JOGO ▶</p>
        <p class="term-p" style="color: #FFFFFF; font-size: 16px; font-weight: bold; margin-bottom: 2px;">VIZ 1 x 2 FLA</p>
        <p class="term-p" style="color: #00D2FF; font-size: 13px;">03/06 - FIM</p>
    </div>
</div>
"""

st.markdown(html_painel, unsafe_allow_html=True)

# 2. LETREIRO DE LED INFERIOR (TICKER) - PONTA A PONTA REAL DA TELA
st.markdown("""
<div class="led-ticker-fullwidth">
    <div class="led-ticker-text-move">
        <div class="led-game-item">FLA 2 . 0 PAL [AO VIVO]</div>
        <div class="led-game-item">FLU 1 . 1 COR [AO VIVO]</div>
        <div class="led-game-item">SÃO 0 . 0 INT [PROX JOGO]</div>
    </div>
</div>
""", unsafe_allow_html=True)
