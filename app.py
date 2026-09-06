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

if data:
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
            # Requisições em paralelo na OpenF1
            drivers_res = requests.get(f"https://api.openf1.org/v1/drivers?session_key={session_key}").json()
            stints_res = requests.get(f"https://api.openf1.org/v1/stints?session_key={session_key}").json()
            intervals_res = requests.get(f"https://api.openf1.org/v1/intervals?session_key={session_key}").json()
            laps_res = requests.get(f"https://api.openf1.org/v1/laps?session_key={session_key}").json()
            
            if drivers_res:
                df_drivers = pd.DataFrame(drivers_res)
                
                # 1. Pneus (Stints recentes)
                tires_map = {}
                if stints_res:
                    df_stints = pd.DataFrame(stints_res)
                    if not df_stints.empty and "stint_number" in df_stints.columns:
                        df_stints = df_stints.sort_values("stint_number")
                        for _, row in df_stints.iterrows():
                            tires_map[row["driver_number"]] = row.get("compound", "UNKNOWN")
                
                # 2. Gaps e Intervalos em segundos
                interval_map = {}
                gap_map = {}
                if intervals_res:
                    df_intervals = pd.DataFrame(intervals_res)
                    if not df_intervals.empty:
                        df_intervals = df_intervals.drop_duplicates(subset=["driver_number"], keep="last")
                        for _, row in df_intervals.iterrows():
                            d_num = row["driver_number"]
                            interval_map[d_num] = f"+{row['interval']}s" if row.get('interval') is not None else "LEADER"
                            gap_map[d_num] = f"+{row['gap_to_leader']}s" if row.get('gap_to_leader') is not None else "LEADER"
                
                # 3. Melhor Volta em segundos formatados
                best_lap_map = {}
                if laps_res:
                    df_laps = pd.DataFrame(laps_res)
                    if not df_laps.empty and "lap_duration" in df_laps.columns:
                        df_valid_laps = df_laps.dropna(subset=["lap_duration"])
                        if not df_valid_laps.empty:
                            idx_min = df_valid_laps.groupby("driver_number")["lap_duration"].idxmin()
                            best_laps = df_valid_laps.loc[idx_min]
                            for _, row in best_laps.iterrows():
                                secs = row["lap_duration"]
                                mins = int(secs // 60)
                                remaining = secs % 60
                                best_lap_map[row["driver_number"]] = f"{mins}:{remaining:06.3f}" if mins > 0 else f"{remaining:06.3f}"
                
                # Mesclando dados na tabela
                df_drivers["Pneu"] = df_drivers["driver_number"].map(tires_map).fillna("N/A")
                df_drivers["Intervalo"] = df_drivers["driver_number"].map(interval_map).fillna("-")
                df_drivers["Gap"] = df_drivers["driver_number"].map(gap_map).fillna("-")
                df_drivers["Melhor Volta"] = df_drivers["driver_number"].map(best_lap_map).fillna("-")
                
                df_display = df_drivers[["driver_number", "name_acronym", "team_name", "Pneu", "Intervalo", "Gap", "Melhor Volta"]].copy()
                df_display.columns = ["Nº", "Piloto", "Equipe", "Pneu", "Intervalo", "Gap", "Melhor Volta"]
                
                st.dataframe(df_display, hide_index=True, use_container_width=True, height=500)
            else:
                st.info("Aguardando dados dos pilotos...")
        except Exception as e:
            st.error(f"Erro ao processar telemetria: {e}")
    else:
        st.info("Conecte a uma sessão válida.")
