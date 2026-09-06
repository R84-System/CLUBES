import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="F1 Pro Dashboard - EA & F1TV Style", layout="wide")

# Estilos CSS Avançados para Layout Profissional (F1 TV Style & Cards)
st.markdown(r"""
<style>
    .stApp {
        background-color: #0b0e14;
        color: #ffffff;
    }
    .f1-card {
        background: linear-gradient(135deg, #121824 0%, #1a2332 100%);
        border: 1px solid #1f2a3a;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
    }
    .f1-card:hover {
        border-color: #e10600;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(225,6,0,0.2);
    }
    .podium-1 { border-left: 6px solid #ffd700; }
    .podium-2 { border-left: 6px solid #c0c0c0; }
    .podium-3 { border-left: 6px solid #cd7f32; }
    .standard-card { border-left: 6px solid #2563eb; }
    
    .badge-pill {
        background: #1f2a3a;
        color: #e2e8f0;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 800;
        color: #ffffff;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Estilo F1 TV Timing Tower Cards */
    .timing-container {
        max-height: 520px;
        overflow-y: auto;
        padding-right: 5px;
    }
    .timing-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #131822;
        border: 1px solid #1f2a3a;
        border-left: 5px solid #2563eb;
        border-radius: 6px;
        padding: 8px 12px;
        margin-bottom: 6px;
        font-family: sans-serif;
    }
    .timing-pos-1 { border-left-color: #e10600; background: linear-gradient(90deg, #2a1215 0%, #131822 100%); }
    .timing-pos-2, .timing-pos-3 { border-left-color: #ffd700; }
    
    .timing-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .timing-pos {
        background: #1f2a3a;
        color: #ffffff;
        font-weight: 900;
        font-size: 0.9rem;
        padding: 3px 8px;
        border-radius: 4px;
        min-width: 28px;
        text-align: center;
    }
    .timing-driver {
        font-weight: 800;
        color: #ffffff;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
    }
    .timing-team {
        color: #94a3b8;
        font-size: 0.7rem;
    }
    .tyre-badge {
        font-size: 0.75rem;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 3px;
        text-align: center;
        min-width: 20px;
    }
    .tyre-soft { background: #da291c; color: #ffffff; }
    .tyre-medium { background: #ffd100; color: #000000; }
    .tyre-hard { background: #ffffff; color: #000000; }
    .tyre-unknown { background: #475569; color: #ffffff; }

    .timing-right {
        text-align: right;
    }
    .timing-time {
        font-weight: 700;
        color: #f1f5f9;
        font-size: 0.85rem;
    }
    .timing-gap {
        font-size: 0.75rem;
        color: #38bdf8;
        font-weight: 600;
    }

    /* Mini Setores */
    .mini-sector {
        display: inline-block;
        width: 7px;
        height: 12px;
        margin-right: 2px;
        border-radius: 2px;
        background: #475569;
    }
    .ms-purple { background: #a855f7; }
    .ms-green { background: #22c55e; }
    .ms-yellow { background: #eab308; }
</style>
""", unsafe_allow_html=True)

# Mapeamento de Bandeiras por Nacionalidade
def get_driver_flag(nationality):
    flags = {
        "British": "🇬🇧", "Dutch": "🇳🇱", "Monegasque": "🇲🇨", "Spanish": "🇪🇸",
        "Mexican": "🇲🇽", "Italian": "🇮🇹", "French": "🇫🇷", "German": "🇩🇪",
        "Australian": "🇦🇺", "Thai": "🇹🇭", "Japanese": "🇯🇵", "Chinese": "🇨🇳",
        "Canadian": "🇨🇦", "Danish": "🇩🇰", "Finnish": "🇫🇮", "American": "🇺🇸",
        "Argentine": "🇦🇷", "Brazilian": "🇧🇷", "Swiss": "🇨🇭", "New Zealander": "🇳🇿",
        "Austrian": "🇦🇹", "Polish": "🇵🇱"
    }
    return flags.get(nationality, "🏁")

# Mapeamento de Escudos/Ícones por Equipe
def get_team_badge(team_name):
    badges = {
        "Ferrari": "🔴 🐎", "Red Bull": "🔵 🐂", "Mercedes": "⬛ ⭐️", "McLaren": "🟠 🏎️",
        "Aston Martin": "💚 🏎️", "Alpine": "💙 🇫🇷", "Williams": "🔷 🇬🇧", "RB": "⚪ 🏎️",
        "Kick Sauber": "🟢 🇨🇭", "Haas F1 Team": "⬜ 🇺🇸", "Audi": "🩶 🇩🇪"
    }
    for key, badge in badges.items():
        if key.lower() in team_name.lower():
            return badge
    return "🏎️ F1"

# Menu Lateral de Navegação
st.sidebar.title("🏁 F1 Hub Pro")
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

    col1, col2 = st.columns([1.4, 1.6])

    with col1:
        st.subheader("Circuito em Tempo Real")
        try:
            with open("static/tracker.js", "r", encoding="utf-8") as f:
                js_code = f.read()
        except FileNotFoundError:
            js_code = "// tracker.js não encontrado"

        track_html = f"""
        <div class="track-container" style="position:relative; width:100%; height:520px; background:#0b0e14; border-radius:12px; border:1px solid #1f2a3a; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">
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
        
        modo_tempo = st.radio(
            "Visualizar diferença de tempo:",
            ["Intervalo (Carro da Frente)", "Diferença para o Líder (Gap)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        is_interval = (modo_tempo == "Intervalo (Carro da Frente)")

        if session_key:
            try:
                drivers_res = requests.get(f"https://api.openf1.org/v1/drivers?session_key={session_key}").json()
                stints_res = requests.get(f"https://api.openf1.org/v1/stints?session_key={session_key}").json()
                intervals_res = requests.get(f"https://api.openf1.org/v1/intervals?session_key={session_key}").json()
                positions_res = requests.get(f"https://api.openf1.org/v1/position?session_key={session_key}").json()
                laps_res = requests.get(f"https://api.openf1.org/v1/laps?session_key={session_key}").json()
                
                current_lap = "1"
                if laps_res and isinstance(laps_res, list):
                    df_laps = pd.DataFrame(laps_res)
                    if not df_laps.empty and "lap_number" in df_laps.columns:
                        current_lap = str(int(df_laps["lap_number"].max()))
                
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; background: #121824; padding: 6px 12px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #1f2a3a;">
                    <span style="font-size: 0.85rem; color: #94a3b8;">Volta Atual da Corrida:</span>
                    <span style="font-size: 0.9rem; font-weight: 800; color: #38bdf8;">🏁 Volta {current_lap}</span>
                </div>
                """, unsafe_allow_html=True)

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
                        compound = tires_map.get(d_num, "N/A")
                        
                        comp_upper = compound.upper()
                        if "SOFT" in comp_upper:
                            tyre_letter, tyre_class = "S", "tyre-soft"
                        elif "MEDIUM" in comp_upper:
                            tyre_letter, tyre_class = "M", "tyre-medium"
                        elif "HARD" in comp_upper:
                            tyre_letter, tyre_class = "H", "tyre-hard"
                        else:
                            tyre_letter, tyre_class = "-", "tyre-unknown"
                        
                        table_data.append({
                            "Pos": position,
                            "Nº": d_num,
                            "Piloto": acronym,
                            "Equipe": team,
                            "Pneu": tyre_letter,
                            "TyreClass": tyre_class,
                            "Intervalo": interval_map.get(d_num, "LEADER" if position == 1 else "-"),
                            "Gap": gap_map.get(d_num, "LEADER" if position == 1 else "-"),
                            "Melhor Volta": best_lap_map.get(d_num, "-")
                        })
                    
                    df_display = pd.DataFrame(table_data)
                    df_display = df_display.sort_values(by="Pos").reset_index(drop=True)
                    
                    # Renderização correta em blocos (Evitando quebra de markdown)
                    st.markdown('<div class="timing-container">', unsafe_allow_html=True)
                    for _, row in df_display.iterrows():
                        pos = row["Pos"]
                        pos_class = "timing-pos-1" if pos == 1 else ("timing-pos-2" if pos == 2 or pos == 3 else "")
                        pilot = row["Piloto"]
                        team = row["Equipe"]
                        tyre = row["Pneu"]
                        t_class = row["TyreClass"]
                        lap_time = row["Melhor Volta"]
                        
                        time_display = row["Intervalo"] if is_interval else row["Gap"]
                        if pos == 1:
                            time_display = "LEADER"

                        # Mini setores ilustrativos
                        ms_html = '<span class="mini-sector ms-green"></span><span class="mini-sector ms-purple"></span><span class="mini-sector ms-green"></span>'

                        row_html = f'''<div class="timing-row {pos_class}">
                            <div class="timing-left">
                                <div class="timing-pos">{pos}</div>
                                <div class="tyre-badge {t_class}">{tyre}</div>
                                <div>
                                    <div class="timing-driver">{pilot}</div>
                                    <div class="timing-team">{team}</div>
                                </div>
                            </div>
                            <div style="display:flex; align-items:center; gap:6px;">
                                {ms_html}
                            </div>
                            <div class="timing-right">
                                <div class="timing-time">{lap_time}</div>
                                <div class="timing-gap">{time_display}</div>
                            </div>
                        </div>'''
                        st.markdown(row_html, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("Aguardando dados dos pilotos...")
            except Exception as e:
                st.error(f"Erro ao processar telemetria: {e}")
        else:
            st.info("Conecte a uma sessão válida.")

elif menu == "🏆 Classificação do Campeonato":
    st.title("🏆 Classificação do Campeonato Mundial")
    
    tab1, tab2 = st.tabs(["Pilotos", "Construtores"])
    
    with tab1:
        st.subheader("Mundial de Pilotos")
        try:
            res = requests.get("https://api.jolpi.ca/ergast/f1/current/driverStandings.json")
            data = res.json()
            standings_list = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
            
            for item in standings_list:
                pos = int(item["position"])
                card_class = f"podium-{pos}" if pos <= 3 else "standard-card"
                driver_name = f"{item['Driver']['givenName']} {item['Driver']['familyName']}"
                nationality = item['Driver'].get('nationality', '')
                flag = get_driver_flag(nationality)
                team_name = item["Constructors"][0]["name"]
                badge = get_team_badge(team_name)
                points = item["points"]
                wins = item["wins"]
                
                card_html = f'<div class="f1-card {card_class}"><div style="display: flex; justify-content: space-between; align-items: center;"><div style="display: flex; align-items: center; gap: 15px;"><span style="font-size: 1.5rem; font-weight: 900; color: {"#ffd700" if pos==1 else "#c0c0c0" if pos==2 else "#cd7f32" if pos==3 else "#ffffff"};">#{pos}</span><div><h3 style="margin: 0; font-size: 1.1rem; color: #ffffff;">{flag} {driver_name}</h3><p style="margin: 2px 0 0 0; font-size: 0.85rem; color: #94a3b8;">{badge} {team_name}</p></div></div><div style="text-align: right; display: flex; gap: 15px; align-items: center;"><div><div class="metric-label">Vitórias</div><div style="font-weight: 700; color: #e2e8f0;">{wins}</div></div><div style="background: #1f2a3a; padding: 8px 16px; border-radius: 8px; text-align: center;"><div class="metric-label">Pontos</div><div class="metric-value" style="color: #e10600;">{points}</div></div></div></div></div>'
                st.markdown(card_html, unsafe_allow_html=True)
        except Exception:
            st.info("Carregando classificação de pilotos...")
            
    with tab2:
        st.subheader("Mundial de Construtores")
        try:
            res = requests.get("https://api.jolpi.ca/ergast/f1/current/constructorStandings.json")
            data = res.json()
            standings_list = data["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]
            
            for item in standings_list:
                pos = int(item["position"])
                card_class = f"podium-{pos}" if pos <= 3 else "standard-card"
                team_name = item["Constructor"]["name"]
                badge = get_team_badge(team_name)
                points = item["points"]
                wins = item["wins"]
                
                card_html = f'<div class="f1-card {card_class}"><div style="display: flex; justify-content: space-between; align-items: center;"><div style="display: flex; align-items: center; gap: 15px;"><span style="font-size: 1.5rem; font-weight: 900; color: {"#ffd700" if pos==1 else "#c0c0c0" if pos==2 else "#cd7f32" if pos==3 else "#ffffff"};">#{pos}</span><div><h3 style="margin: 0; font-size: 1.1rem; color: #ffffff;">{badge} {team_name}</h3></div></div><div style="text-align: right; display: flex; gap: 15px; align-items: center;"><div><div class="metric-label">Vitórias</div><div style="font-weight: 700; color: #e2e8f0;">{wins}</div></div><div style="background: #1f2a3a; padding: 8px 16px; border-radius: 8px; text-align: center;"><div class="metric-label">Pontos</div><div class="metric-value" style="color: #e10600;">{points}</div></div></div></div></div>'
                st.markdown(card_html, unsafe_allow_html=True)
        except Exception:
            st.info("Carregando classificação de construtores...")

elif menu == "📅 Próximos GPs (Calendário)":
    st.title("📅 Calendário de Grandes Prêmios")
    try:
        res = requests.get("https://api.jolpi.ca/ergast/f1/current.json")
        data = res.json()
        races = data["MRData"]["RaceTable"]["Races"]
        
        cols = st.columns(2)
        for idx, race in enumerate(races):
            round_num = race["round"]
            race_name = race["raceName"]
            circuit = race["Circuit"]["circuitName"]
            country = race["Circuit"]["Location"]["country"]
            date = race["date"]
            
            card_html = f'<div class="f1-card standard-card"><div style="display: flex; justify-content: space-between; align-items: flex-start;"><div><span class="badge-pill">Etapa {round_num}</span><h3 style="margin: 8px 0 4px 0; font-size: 1.05rem; color: #ffffff;">🏁 {race_name}</h3><p style="margin: 0; font-size: 0.85rem; color: #94a3b8;">📍 {circuit} ({country})</p></div><div style="text-align: right;"><div class="metric-label">Data</div><div style="font-weight: 700; color: #e2e8f0; font-size: 0.95rem;">📅 {date}</div></div></div></div>'
            cols[idx % 2].markdown(card_html, unsafe_allow_html=True)
            
    except Exception:
        st.info("Carregando calendário de GPs...")
