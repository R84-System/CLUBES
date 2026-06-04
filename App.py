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
# MOTOR GRÁFICO LOCAL: COMPACTO E NITIDO
# ==========================================
def gerar_imagem_led_matrix_local(nome_arquivo, tamanho_matriz=64):
    """
    Carrega a imagem localmente com matriz de 64x64, ideal para o tamanho
    redimensionado e mantendo a fidelidade dos pontos físicos.
    """
    try:
        caminho_imagem = os.path.join("escudos", nome_arquivo)
        
        if not os.path.exists(caminho_imagem):
            return None
            
        img = Image.open(caminho_imagem).convert("RGBA")
        img_led = img.resize((tamanho_matriz, tamanho_matriz), Image.Resampling.NEAREST)
        
        fator_escala = 6  # Reduzido ligeiramente para ajustar ao novo frame
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
# ESTILIZAÇÃO CUSTOMIZADA (CSS) - REDIMENSIONAMENTO EQUILIBRADO
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #030712; }
    
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
    
    h2, h3, label, .stMarkdown p { color: #E2E8F0 !important; font-family: 'Courier New', monospace; }
    
    /* Container principal */
    .main-display-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        border: 2px solid #0B2545; border-radius: 16px; padding: 25px;
        background-color: #050E1E; box-shadow: 0 0 35px rgba(0, 102, 204, 0.25);
        margin: 0 auto; max-width: 850px;
    }
    
    /* Moldura central - TAMANHO PERFEITO E COMPACTO */
    .shield-wrapper {
        display: flex; justify-content: center; align-items: center;
        width: 100%; max-width: 380px; height: 380px; /* Reduzido para conter o exagero */
        border: 3px solid #134074; border-radius: 12px; padding: 12px;
        background-color: #010409; box-shadow: inset 0 0 30px rgba(0, 210, 255, 0.2);
        margin-bottom: 25px; overflow: hidden;
    }
    
    .shield-wrapper img { width: 100%; height: 100%; object-fit: contain; display: block; }
    
    /* Grid de informações */
    .game-status-bar { width: 100%; max-width: 750px; font-family: 'Courier New', monospace; margin-bottom: 25px; }
    
    /* LETREIRO DE LED GIGANTE NO RODAPÉ */
    .led-ticker-container {
        width: 100%; overflow: hidden; background-color: #000000; 
        border: 4px solid #134074; border-radius: 6px; padding: 20px 0; margin-top: 10px; position: relative;
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.5);
    }
    .led-ticker-container::before {
        content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 1
