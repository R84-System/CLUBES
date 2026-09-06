import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="F1 Pro Dashboard - EA & F1TV Style", layout="wide")

# Carrega o CSS externo se existir
try:
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Menu Lateral de Navegação
st.sidebar.title("🏁 F1 Hub Menu")
menu = st.sidebar.radio(
    "Navegação",
    ["🏎️ Telemetria ao Vivo", "🏆 Classificação do Campeonato", "📅 Próximos GPs (Calendário)"]
)

if menu == "🏎️ Telemetria ao Vivo":
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
        st.sidebar.success(f"Sessão Ativa: {circuit_name} ({year})")
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
                drivers_res = requests.get(f"https://api.openf1.org/v1/drivers?session_key={session_key}").json()
                stints_res = requests.get(f"https://api.openf1.org/v1/stints?session_key={session_key}").json()
                intervals_res = requests.get(f"https://api.openf1.org/v1/intervals?session_key={session_key}").json()
                positions_res = requests.get(f"https://api.openf1.org/v1/position?session_key={session_key}").json()
                laps_res = requests.get(f"https://api.openf1.org/v1/laps?session_key={session_key}").json()
                
                if drivers_res and isinstance(drivers_res, list):
                    tires_map = {}
                    if stints_res and isinstance(stints_res, list):
                        for s in stints_res:
                            d_num = s.get("driver_number")
                            if d_num:
                                tires_map[d_num] = s.get("compound", "N/A")
                    
                    pos_map = {}
                    if positions_res and isinstance(positions_res, list):
                        df_pos = pd.DataFrame(positions_res)
                        if not df_pos.empty and "driver_number" in df_pos.columns and "position" in df_pos.columns:
                            df_pos = df_pos.sort_values("date")
                            for _, row in df_pos.drop_duplicates(subset=["driver_number"], keep="last").iterrows():
                                pos_map[row["driver_number"]] = row["position"]

                    interval_map = {}
                    gap_map = {}
                    if intervals_res and isinstance(intervals_res, list):
                        df_int = pd.DataFrame(intervals_res)
                        if not df_int.empty:
                            df_int = df_int.sort_values("date")
                            for _, row in df_int.drop_duplicates(subset=["driver_number"], keep="last").iterrows():
                                d_num = row.get("driver_number")
                                inter = row.get('interval')
                                gap = row.get('gap_to_leader')
                                if d_num:
                                    interval_map[d_num] = f"+{inter}s" if inter is not None else "-"
                                    gap_map[d_num] = f"+{gap}s" if gap is not None else "-"
                    
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

                    table_data = []
                    for driver in drivers_res:
                        d_num = driver.get("driver_number")
                        acronym = driver.get("name_acronym", str(d_num))
                        team = driver.get("team_name", "Desconhecida")
                        position = pos_map.get(d_num, 99)
                        
                        table_data.append({
                            "Pos": position,
                            "Nº": d_num,
                            "Piloto": acronym,
                            "Equipe": team,
                            "Pneu": tires_map.get(d_num, "N/A"),
                            "Intervalo": interval_map.get(d_num, "LEADER" if position == 1 else "-"),
                            "Gap": gap_map.get(d_num, "LEADER" if position == 1 else "-"),
                            "Melhor Volta": best_lap_map.get(d_num, "-")
                        })
                    
                    df_display = pd.DataFrame(table_data)
                    df_display = df_display.sort_values(by="Pos").reset_index(drop=True)
                    
                    st.dataframe(df_display, hide_index=True, use_container_width=True, height=500)
                else:
                    st.info("Aguardando dados dos pilotos...")
            except Exception as e:
                st.error(f"Erro ao processar telemetria: {e}")
        else:
            st.info("Conecte a uma sessão válida.")

elif menu == "🏆 Classificação do Campeonato":
    st.title("🏆 Classificação do Campeonato Mundial de F1")
    
    tab1, tab2 = st.tabs(["Pilotos", "Construtores"])
    
    with tab1:
        st.subheader("Mundial de Pilotos")
        try:
            res = requests.get("https://api.jolpi.ca/ergast/f1/current/driverStandings.json")
            data = res.json()
            standings_list = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
            
            drivers_data = []
            for item in standings_list:
                drivers_data.append({
                    "Pos": item["position"],
                    "Piloto": f"{item['Driver']['givenName']} {item['Driver']['familyName']}",
                    "Equipe": item["Constructors"][0]["name"],
                    "Pontos": item["points"],
                    "Vitórias": item["wins"]
                })
            st.dataframe(pd.DataFrame(drivers_data), hide_index=True, use_container_width=True)
        except Exception:
            st.info("Carregando dados de classificação de pilotos...")
            
    with tab2:
        st.subheader("Mundial de Construtores")
        try:
            res = requests.get("https://api.jolpi.ca/ergast/f1/current/constructorStandings.json")
            data = res.json()
            standings_list = data["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]
            
            constructors_data = []
            for item in standings_list:
                constructors_data.append({
                    "Pos": item["position"],
                    "Equipe": item["Constructor"]["name"],
                    "Pontos": item["points"],
                    "Vitórias": item["wins"]
                })
            st.dataframe(pd.DataFrame(constructors_data), hide_index=True, use_container_width=True)
        except Exception:
            st.info("Carregando dados de construtores...")

elif menu == "📅 Próximos GPs (Calendário)":
    st.title("📅 Calendário de Grandes Prêmios da Temporada")
    try:
        res = requests.get("https://api.jolpi.ca/ergast/f1/current.json")
        data = res.json()
        races = data["MRData"]["RaceTable"]["Races"]
        
        calendar_data = []
        for race in races:
            calendar_data.append({
                "Etapa": race["round"],
                "Grande Prêmio": race["raceName"],
                "Circuito": race["Circuit"]["circuitName"],
                "País": race["Circuit"]["Location"]["country"],
                "Data": race["date"]
            })
            
        st.dataframe(pd.DataFrame(calendar_data), hide_index=True, use_container_width=True, height=600)
    except Exception:
        st.info("Carregando calendário de GPs...")
