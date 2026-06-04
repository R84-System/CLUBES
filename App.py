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
# MOTOR GRÁFICO LOCAL: ULTRA RÁPIDO E BLINDADO
# ==========================================
def gerar_imagem_led_matrix_local(nome_arquivo, tamanho_matriz=64):
    """
    Carrega a imagem direto da pasta local do repositório, garantindo
    velocidade máxima e zero travamentos externos.
    """
    try:
        # Caminho relativo para a pasta de escudos dentro do GitHub
        caminho_imagem = os.path.join("escudos", nome_arquivo)
        
        if not os.path.exists(caminho_imagem):
            return None
            
        img = Image.open(caminho_imagem).convert("RGBA")
        
        # Reduz para a resolução da matriz de LED
        img_led = img.resize((tamanho_matriz, tamanho_matriz), Image.Resampling.NEAREST)
        
        # Cria a imagem física que simula o painel eletrônico
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
                    # LED apagado (azul escuro de fundo)
                    draw.ellipse([x0+2, y0+2, x1-2, y1-2], fill=(13, 26, 45, 40))
                else:
                    # LED aceso com a cor exata do time
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
# MAPEAMENTO LOCAL DE ARQUIVOS (DENTRO DO GITHUB)
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
# CORPO PRINCIPAL
# ==========================================
st.markdown("<h1 style='color: #00D2FF; font-family: monospace; font-size: 24px;'>TERMINAL K97 // LED MATRIX DISPLAY</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-display-container">', unsafe_allow_html=True)
    
    # Busca o nome do arquivo mapeado localmente
    arquivo_alvo = arquivos_escudos.get(selected_club)
    
    # Roda o motor puxando o arquivo direto do HD do servidor do GitHub
    imagem_matriz = gerar_imagem_led_matrix_local(arquivo_alvo, tamanho_matriz=64)
    
    if imagem_matriz is not None:
        st.image(imagem_matriz, width=420, output_format="PNG")
    else:
        # Mensagem intuitiva caso você ainda não tenha subido o arquivo PNG na pasta escudos
        st.markdown(f'<div style="color: #FF9F00; font-family: monospace; height: 420px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;">'
                    f'<span>[ AGUARDANDO ARQUIVO LOCAL ]</span><br>'
                    f'<span style="font-size:11px; color:#8892B0;">Insira o arquivo "{arquivo_alvo}" dentro da pasta "escudos" no seu GitHub para acender o painel.</span>'
                    f'</div>', unsafe_allow_html=True)
        
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
