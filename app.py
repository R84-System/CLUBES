import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="F1 Live Dashboard", layout="wide")

# Carrega o CSS externo
try:
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

st.title("🏎️ F1 Live Dashboard - OpenF1 API")

@st.cache_data(ttl=60)
def get_latest_session():
    res = requests.get("https://api.openf1.org/v1/sessions?session_key=latest")
    return res.json()

data = get_latest_session()

if data:
    latest_session = data[0]
    session_key = latest_session["session_key"]
    st.sidebar.success(f"Sessão Conectada: {latest_session.get('circuit_short_name', 'F1')} ({latest_session.get('year', '')})")
else:
    session_key = None
    st.sidebar.warning("Nenhuma sessão ao vivo encontrada no momento.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Circuito em Tempo Real")
    
    try:
        with open("static/tracker.js", "r", encoding="utf-8") as f:
            js_code = f.read()
    except FileNotFoundError:
        js_code = "// tracker.js não encontrado"

    track_html = f"""
    <div class="track-container" style="position:relative; width:100%; height:500px; background:#151820; border-radius:8px;">
        <canvas id="f1Canvas" style="width:100%; height:100%;"></canvas>
    </div>
    <script>
        window.sessionKey = "{session_key}";
        {js_code}
    </script>
    """
    st.components.v1.html(track_html, height=520)

with col2:
    st.subheader("Posições & Pilotos")
    if session_key:
        drivers_res = requests.get(f"https://api.openf1.org/v1/drivers?session_key={session_key}").json()
        if drivers_res:
            df_drivers = pd.DataFrame(drivers_res)[["driver_number", "name_acronym", "team_name"]]
            df_drivers.columns = ["Número", "Sigla", "Equipe"]
            st.dataframe(df_drivers, hide_index=True, use_container_width=True)
        else:
            st.info("Aguardando dados de pilotos para esta sessão.")
    else:
        st.info("Conecte a uma sessão válida para ver os pilotos.")
