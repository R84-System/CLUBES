import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="F1 Live Dashboard - Pro Telemetry", layout="wide")

# Carrega o CSS externo se existir
try:
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

st.title("🏎️ F1 Pro Telemetry & Timing Tower")

@st.cache_data(ttl=15)
def get_latest_session():
    try:
        res = requests.get("https://api.openf1.org/v1/sessions?session_key=latest")
        return res.json()
    except:
        return []

data = get_latest_session()

if data and len(data) > 0:
    latest_session = data[0]
    session_key = latest_session.get("session_key")
    circuit_name = latest_session.get('circuit_short_name', 'F1')
    year = latest_session.get('year', '')
    st.sidebar.success(f"Sessão: {circuit_name} ({year})")
else:
    session_key = None
    st.sidebar.warning("Nenhuma sessão ao vivo encontrada.")

col1, col2 = st.columns([1.5, 1.5])

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
    st.subheader("Torre de Tempos & Segundos")
    if session_key:
        try:
            # Requisições para a API OpenF1
            drivers_res = requests.get(f"https://api.openf1.org/v1/drivers?session_key={session_key}").json()
            stints_res = requests.get(f"https://api.openf1.org/v1/stints?session_key={session_key}").json()
            intervals_res = requests.get(f"https://api.openf1.org/v1/intervals?session_key={session_key}").json()
            laps_res = requests.get(f"https://api.openf1.org/v1/laps?session_key={session_key}").json()
            
            if drivers_res and isinstance(drivers_res, list):
                # 1. Mapear Pneus
                tires_map = {}
                if stints_res and isinstance(stints_res, list):
                    for s in stints_res:
                        d_num = s.get("driver_number")
                        if d_num:
                            tires_map[d_num] = s.get("compound", "N/A")
                
                # 2. Mapear Intervalos e Gaps
                interval_map = {}
                gap_map = {}
                if intervals_res and isinstance(intervals_res, list):
                    for row in intervals_res:
                        d_num = row.get("driver_number")
                        if d_num:
                            inter = row.get('interval')
                            gap = row.get('gap_to_leader')
                            interval_map[d_num] = f"+{inter}s" if inter is not None else "LEADER"
                            gap_map[d_num] = f"+{gap}s" if gap is not None else "LEADER"
                
                # 3. Mapear Melhores Voltas
                best_lap_map = {}
                if laps_res and isinstance(laps_res, list):
                    df_laps = pd.DataFrame(laps_res)
                    if not df_laps.empty and "lap_duration" in df_laps.columns and "driver_number" in df_laps.columns:
                        df_valid = df_laps.dropna(subset=["lap_duration"])
                        if not df_valid.empty:
                            for d_num, group in df_valid.groupby("driver_number"):
                                min_duration = group["lap_duration"].min()
                                mins = int(min_duration // 60)
                                remaining = min_duration % 60
                                time_str = f"{mins}:{remaining:06.3f}" if mins > 0 else f"{remaining:06.3f}"
                                best_lap_map[d_num] = time_str

                # 4. Construir dados da tabela com segurança linha por linha
                table_data = []
                for driver in drivers_res:
                    d_num = driver.get("driver_number")
                    acronym = driver.get("name_acronym", str(d_num))
                    team = driver.get("team_name", "Desconhecida")
                    
                    table_data.append({
                        "Nº": d_num,
                        "Piloto": acronym,
                        "Equipe": team,
                        "Pneu": tires_map.get(d_num, "N/A"),
                        "Intervalo": interval_map.get(d_num, "-"),
                        "Gap": gap_map.get(d_num, "-"),
                        "Melhor Volta": best_lap_map.get(d_num, "-")
                    })
                
                df_display = pd.DataFrame(table_data)
                st.dataframe(df_display, hide_index=True, use_container_width=True, height=500)
            else:
                st.info("Aguardando dados dos pilotos...")
        except Exception as e:
            st.error(f"Erro ao processar telemetria: {e}")
    else:
        st.info("Conecte a uma sessão válida.")
