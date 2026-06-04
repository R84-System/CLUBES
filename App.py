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
# ESTILIZAÇÃO CUSTOMIZADA (CSS) - ALINHAMENTO COMPACTO
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #030712; }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; }
    
    h2, h3, label, .stMarkdown p { color: #E2E8F0 !important; font-family: 'Courier New', monospace; }
    
    /* LIMITA A LARGURA GERAL DO PAINEL PARA JUNTAR AS LATERAIS */
    .game-status-bar { 
        width: 100%; 
        max-width: 780px; /* Reduzido para trazer as colunas das pontas para perto do escudo */
        font-family: 'Courier New', monospace; 
        margin: 25px auto 10px auto; 
    }
    
    /* Centralizador do Escudo na coluna do meio */
    .center-shield-box {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 15px;
    }
    .center-shield-box img { max-width: 240px; width: 100%; height: auto; display: block; margin: 0 auto; }
    
    /* LETREIRO DE LED NO RODAPÉ */
    .led-ticker-container {
        width: 100%; max-width: 780px; overflow: hidden; background-color: #000000; 
        border: 4px solid #134074; border-radius: 6px; padding: 18px 0; margin: 30px auto 10px auto; position: relative;
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.4);
    }
    .led-ticker-container::before {
        content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.5) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0), rgba(0, 0, 0, 0.7));
        background-size: 100% 4px, 4px 100%; z-index: 10; pointer-events: none;
    }
    .led-ticker-text { display: flex; white-space: nowrap; padding-left: 100%; animation: led-scroll 22s linear infinite; }
    .led-game {
        display: inline-block; padding: 0 4rem; font-size: 2.2rem; 
        font-family: 'Lucida Console', 'Courier New', monospace; font-weight: 900;
        color: #00D2FF; text-shadow: 0 0 12px #00D2FF, 0 0 25px #134074; letter-spacing: 5px;
    }
    @keyframes led-scroll { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
    
    /* Botão de atualizar centralizado */
    .stButton { display: flex; justify-content: center; margin: 20px auto; }
    .stButton>button { 
        background-color: #134074 !important; color: #FFFFFF !important; 
        border: 1px solid #00D2FF !important; font-family: 'Courier New', monospace !important; 
        font-weight: bold !important; padding: 6px 22px !important;
    }
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
# PAINEL DE DADOS TRILATERAL PRINCIPAL
# ==========================================
arquivo_alvo = archivos_escudos.get(selected_club)
imagem_matriz = gerar_imagem_led_matrix_local(arquivo_alvo, tamanho_matriz=64)

st.markdown('<div class="game-status-bar">', unsafe_allow_html=True)

# Definição de proporção ajustada para manter os textos próximos
status_cols = st.columns([1.1, 1.8, 1.1])

# COLUNA 1: Próximo Jogo (Esquerda)
with status_cols[0]:
    st.markdown("<div style='margin-top: 100px;'>", unsafe_allow_html=True) # Empurra o texto para alinhar com o placar
    st.markdown("<p style='color: #8892B0; font-size: 11px; margin-bottom: 2px; text-align: left;'>◀ PRÓXIMO JOGO</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFFFFF; font-size: 14px; font-weight: bold; text-align: left;'>COR vs FLA</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00D2FF; font-size: 12px; text-align: left;'>Dom - 16:00</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# COLUNA 2: CENTRO (Escudo + Placar)
with status_cols[1]:
    if imagem_matriz is not None:
        st.markdown('<div class="center-shield-box">', unsafe_allow_html=True)
        st.image(imagem_matriz, output_format="PNG")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="color: #FF9F00; font-family: monospace; font-size: 12px; text-align: center; margin-bottom: 15px;">[ AGUARDANDO: {arquivo_alvo} ]</div>', unsafe_allow_html=True)
    
    st.markdown("<p style='color: #FF9F00; font-size: 11px; margin-bottom: 2px; text-align: center;'>• EM ANDAMENTO •</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00D2FF; font-size: 24px; font-weight: bold; text-align: center; letter-spacing: 2px;'>FLA 2 x 0 PAL</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FF9F00; font-size: 12px; text-align: center;'>2º Tempo - 22'</p>", unsafe_allow_html=True)

# COLUNA 3: Último Jogo (Direita)
with status_cols[2]:
    st.markdown("<div style='margin-top: 100px;'>", unsafe_allow_html=True) # Empurra o texto para alinhar com o placar
    st.markdown("<p style='color: #8892B0; font-size: 11px; margin-bottom: 2px; text-align: right;'>ÚLTIMO JOGO ▶</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFFFFF; font-size: 14px; font-weight: bold; text-align: right;'>VIZ 1 x 2 FLA</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00D2FF; font-size: 12px; text-align: right;'>03/06 - FIM</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Botão de atualizar centralizado
if st.button("ATUALIZAR PAINEL"):
    st.rerun()
    
# 3. LETREIRO DE LED INFERIOR (TICKER)
st.markdown("""
<div class="led-ticker-container">
    <div class="led-ticker-text">
        <div class="led-game">FLA 2 . 0 PAL [AO VIVO]</div>
        <div class="led-game">FLU 1 . 1 COR [AO VIVO]</div>
        <div class="led-game">SÃO 0 . 0 INT [PROX JOGO]</div>
    </div>
</div>
""", unsafe_allow_html=True)
