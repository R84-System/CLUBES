import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="F1 Live Dashboard - EA Style", layout="wide")

# Carrega o CSS externo
try:
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

st.title("🏎️ F1 EA Telemetry & Live Dashboard")

@st.cache_data(ttl=30)
def get_latest_session():
    res = requests.get("https://api.openf1.org/v1/sessions?session_key=latest")
    return res.json()

data = get_latest_session()

if data:
    latest_session = data[0]
    session_key = latest_session["session_key"]
    st.sidebar.success(f"Sessão: {latest_session.get('circuit_short_name', 'F1')} ({latest_session.get('year', '')})")
else:
    session_key = None
    st.sidebar.warning("Nenhuma sessão ao vivo encontrada.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Circuito em Tempo Real")
    
    try:
        with open("static/tracker.js", "r", encoding="utf-8") as f:
            js_code = f.read()
    except FileNotFoundError:
        js_code = "// tracker.js não encontrado"

    track_html = f"""
    <div class="track-container" style="position:relative; width:100%; height:520px; background:#0b0e14; border-radius:10px; border:1px solid #1f2a3a;">
        <canvas id="f1Canvas" style="width:100%; height:100%;"></canvas>
    </div>
    <script>
        window.sessionKey = "{session_key}";
        {js_code}
    </script>
    """
    st.components.v1.html(track_html, height=540)

with col2:
    st.subheader("Posições & Pilotos")
    if session_key:
        # Busca dados necessários
        drivers_res = requests.get(f"https://api.openf1.org/v1/drivers?session_key={session_key}").json()
        stints_res = requests.get(f"https://api.openf1.org/v1/stints?session_key={session_key}").json()
        positions_res = requests.get(f"https://api.openf1.org/v1/position?session_key={session_key}&per_page=100").json()
        
        if drivers_res:
            df_drivers = pd.DataFrame(drivers_res)
            
            # Pega o stint mais recente (maior stint_number) para cada piloto
            tires_map = {}
            if stints_res:
                df_stints = pd.DataFrame(stints_res)
                if not df_stints.empty and "stint_number" in df_stints.columns:
                    df_stints = df_stints.sort_values("stint_number")
                    for _, row in df_stints.iterrows():
                        tires_map[row["driver_number"]] = row.get("compound", "UNKNOWN")
            
            df_drivers["Pneu"] = df_drivers["driver_number"].map(tires_map).fillna("N/A")
            
            # Seleciona e renomeia as colunas principais
            df_display = df_drivers[["driver_number", "name_acronym", "team_name", "Pneu"]].copy()
            df_display.columns = ["Nº", "Piloto", "Equipe", "Pneu"]
            
            st.dataframe(df_display, hide_index=True, use_container_width=True, height=500)
        else:
            st.info("Aguardando dados dos pilotos...")
    else:
        st.info("Conecte a uma sessão válida.")
