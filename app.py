import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="F1 Live Dashboard", layout="wide")

st.title("🏎️ F1 Live Dashboard - MultiViewer Style")
st.markdown("Painel de telemetria e posições em tempo real.")

# Carrega o CSS externo
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Layout principal dividindo Mapa e Tabela de Posições
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Circuito em Tempo Real")
    # Injeta o HTML e o script JS do mapa
    with open("static/tracker.js") as f:
        js_code = f.read()
    
    track_html = f"""
    <div class="track-container">
        <canvas id="f1Canvas"></canvas>
    </div>
    <script>{js_code}</script>
    """
    st.components.v1.html(track_html, height=520)

with col2:
    st.subheader("Posições & Pneus")
    # Exemplo de tabela mockada/inicial para teste
    df_drivers = pd.DataFrame({
        "Pos": [1, 2, 3],
        "Piloto": ["VER", "HAM", "LEC"],
        "Pneu": ["SOFT", "MEDIUM", "HARD"],
        "Box": ["Não", "Não", "Sim"]
    })
    st.dataframe(df_drivers, hide_index=True, use_container_width=True)
