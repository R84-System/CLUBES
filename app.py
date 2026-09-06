import streamlit as st
import requests
import pandas as pd

# 1. Configuração da Página para Largura Total e Ocultação da Sidebar Nativa
st.set_page_config(
    page_title="F1 Pro Dashboard - EA & F1TV Style",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Estilos CSS Avançados para Layout Profissional (F1 TV Style & Cards) sem Margens Laterais
st.markdown(r"""
<style>
    .block-container {
        padding-top: 0.4rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
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

    /* Efeito de Pulso para Indicador Ao Vivo */
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    .live-dot {
        height: 10px;
        width: 10px;
        background-color: #ef4444;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #ef4444;
        animation: pulse 1.5s infinite;
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
    .pit-badge {
        background: #db2777;
        color: #ffffff;
        font-size: 0.6rem;
        font-weight: 800;
        padding: 3px 6px;
        border-radius: 4px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .timing-pos {
        background: #1f2a3a;
        color: #ffffff;
        font-weight: 900;
        font-size: 0.85rem;
        padding: 2px 6px;
        border-radius: 4px;
        min-width: 28px;
        text-align: center;
    }
    .timing-driver {
        font-weight: 800;
        color: #ffffff;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }
    .timing-team {
        color: #94a3b8;
        font-size: 0.7rem;
    }
    .tyre-badge {
        font-size: 0.65rem;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 4px;
        text-align: center;
        min-width: 18px;
    }
    .tyre-soft { background: #da291c; color: #ffffff; }
    .tyre-medium { background: #ffd100; color: #000000; }
    .tyre-hard { background: #ffffff; color: #000000; }
    .tyre-unknown { background: #475569; color: #ffffff; }

    .timing-right {
        text-align: right;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .timing-time {
        font-weight: 700;
        color: #f1f5f9;
        font-size: 0.85rem;
    }

    /* Mini Setores */
    .mini-sector {
        display: inline-block;
        width: 6px;
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

# Tradutor de Nomes de Sessão da API para Português Amigável
def translate_session_name(session_name):
    if not session_name:
        return "Sessão ao Vivo"
    mapping = {
        "Practice 1": "Treino Livre 1 (TL1)",
        "Practice 2": "Treino Livre 2 (TL2)",
        "Practice 3": "Treino Livre 3 (TL3)",
        "Qualifying": "Classificação (Q1 / Q2 / Q3)",
        "Sprint": "Corrida Sprint",
        "Race": "Corrida Principal",
        "Sprint Shootout": "Sprint Shootout",
        "Sprint Qualifying": "Classificação Sprint"
    }
    return mapping.get(session_name, session_name)

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

# 3. Cabeçalho Principal e Barra de Navegação Horizontal
col_logo, col_nav = st.columns([1.4, 3.6])
with col_logo:
    st.markdown('<div style="font-size: 1.25rem; font-weight: 900; font-style: italic; letter-spacing: 1px; color: #ffffff; padding-top: 6px;">FORMULA 1 <span style="color: #e10600; background: #ffffff; padding: 1px 5px; border-radius: 4px;">HUB PRO</span></div>', unsafe_allow_html=True)

with col_nav:
    menu = st.radio(
        "Navegação",
        ["🏎️ Telemetria ao Vivo", "🏆 Classificação do Campeonato", "📅 Próximos GPs (Calendário)"],
        horizontal=True,
        label_visibility="collapsed"
    )

st.markdown("<hr style='margin: 4px 0 15px 0; border-color: #1f2a3a;'>", unsafe_allow_html=True)

# Lógica das Telas
if menu == "🏎️ Telemetria ao Vivo":
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
        raw_session_name = latest_session.get('session_name', '')
        session_title = translate_session_name(raw_session_name)
    else:
        session_key = None
        session_title = "Aguardando Sessão"
        circuit_name = "Circuito F1"
        year = ""

    # Banner Superior Dinâmico indicando o status atual ao vivo
    banner_html = f"""
    <div style="display: flex; align-items: center; justify-content: space-between; background: linear-gradient(135deg, #121824 0%, #1a2332 100%); border: 1px solid #1f2a3a; border-left: 5px solid #e10600; padding: 12px 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span class="live-dot"></span>
            <div>
                <span style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; display: block;">Sessão Ativa na Pista</span>
                <span style="font-size: 1.1rem; font-weight: 900; color: #ffffff; letter-spacing: 0.5px;">{session_title}</span>
            </div>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 0.8rem; color: #38bdf8; font-weight: 700; background: #1f2a3a; padding: 4px 10px; border-radius: 6px;">📍 {circuit_name} — {year}</span>
        </div>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)

    col1, col2 = st.columns([1.4, 1.6])

    with col1:
        st.subheader("Circuito em Tempo Real")
        
        # Script JS integrado diretamente para evitar erro de arquivo não encontrado
        track_html = f"""
        <div class="track-container" style="position:relative; width:100%; height:520px; background:#0b0e14; border-radius:12px; border:1px solid #1f2a3a; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">
            <canvas id="f1Canvas" style="width:100%; height:100%;"></canvas>
        </div>
        <script>
            window.sessionKey = "{session_key}";
            const canvas = document.getElementById('f1Canvas');
            if (canvas) {{
                const ctx = canvas.getContext('2d');
                function resize() {{
                    canvas.width = canvas.parentElement.clientWidth;
                    canvas.height = canvas.parentElement.clientHeight;
                    drawTrack();
                }}
                
                function drawTrack() {{
                    ctx.fillStyle = '#0b0e14';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);

                    let cx = canvas.width / 2;
                    let cy = canvas.height / 2;

                    // Traçado estilizado da pista
                    ctx.strokeStyle = '#1f2a3a';
                    ctx.lineWidth = 30;
                    ctx.lineCap = 'round';
                    ctx.lineJoin = 'round';

                    ctx.beginPath();
                    ctx.moveTo(cx - 130, cy + 90);
                    ctx.lineTo(cx - 130, cy - 50);
                    ctx.arc(cx - 70, cy - 50, 60, Math.PI, 0, false);
                    ctx.lineTo(cx - 10, cy + 30);
                    ctx.arc(cx + 50, cy + 30, 60, Math.PI, 2 * Math.PI, false);
                    ctx.lineTo(cx + 110, cy - 90);
                    ctx.stroke();

                    // Linha central pontilhada
                    ctx.strokeStyle = '#e10600';
                    ctx.lineWidth = 2;
                    ctx.setLineDash([6, 6]);
                    ctx.stroke();
                    ctx.setLineDash([]);

                    // Informações na tela
                    ctx.fillStyle = '#ffffff';
                    ctx.font = 'bold 13px sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillText("📍 CIRCUITO F1 — TELEMETRIA AO VIVO", 20, 35);
                    
                    if (window.sessionKey && window.sessionKey !== "None") {{
                        ctx.fillStyle = '#22c55e';
                        ctx.fillText("● Status: Conectado à Sessão (" + window.sessionKey + ")", 20, 58);
                    }} else {{
                        ctx.fillStyle = '#f59e0b';
                        ctx.fillText("● Status: Aguardando Sessão Ativa", 20, 58);
                    }}
                }}

                window.addEventListener('resize', resize);
                resize();
            }}
        </script>
        """
        st.components.v1.html(track_html, height=540)

    with col2:
        st.subheader("Torre de Tempos")
        
        modo_tempo = st.radio(
            "Visualizar diferença:",
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
                pits_res = requests.get(f"https://api.openf1.org/v1/pits?session_key={session_key}").json()
                
                in_pit_drivers = set()
                if pits_res and isinstance(pits_res, list):
                    for p in pits_res:
                        if p.get("pit_duration") is None:
                            in_pit_drivers.add(p.get("driver_number"))

                current_lap = 1
                total_laps = 57
                if laps_res and isinstance(laps_res, list):
                    df_laps = pd.DataFrame(laps_res)
                    if not df_laps.empty and "lap_number" in df_laps.columns:
                        current_lap = int(df_laps["lap_number"].max())
                
                if "Race" in raw_session_name:
                    if current_lap == 1:
                        st.markdown("""<div style="background: linear-gradient(90deg, #b91c1c, #ef4444); color: white; padding: 6px 12px; border-radius: 6px; font-weight: 800; text-align: center; margin-bottom: 8px; font-size: 0.8rem;">🔴🔴🔴🔴🔴 LARGADA AUTORIZADA — VOLTA 1</div>""", unsafe_allow_html=True)
                    elif current_lap >= total_laps:
                        st.markdown("""<div style="background: linear-gradient(90deg, #1e293b, #334155); color: white; padding: 6px 12px; border-radius: 6px; font-weight: 800; text-align: center; margin-bottom: 8px; font-size: 0.8rem; border: 1px dashed #ffffff;">🏁 BANDEIRA QUADRICULADA — FIM DE CORRIDA! 🏁</div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div style="display: flex; justify-content: space-between; background: #121824; padding: 6px 12px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #1f2a3a;"><span style="font-size: 0.8rem; color: #94a3b8;">Total de Voltas do GP: <b>{total_laps}</b></span><span style="font-size: 0.85rem; font-weight: 800; color: #38bdf8;">🟢 Volta Atual: {current_lap} / {total_laps}</span></div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div style="display: flex; justify-content: space-between; background: #121824; padding: 6px 12px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #1f2a3a;"><span style="font-size: 0.8rem; color: #94a3b8;">Sessão: <b>{session_title}</b></span><span style="font-size: 0.85rem; font-weight: 800; color: #38bdf8;">⏱️ Voltas Registradas: {current_lap}</span></div>""", unsafe_allow_html=True)

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
                    overall_fastest_driver = None
                    if laps_res and isinstance(laps_res, list):
                        df_laps = pd.DataFrame(laps_res)
                        if not df_laps.empty and "lap_duration" in df_laps.columns and "driver_number" in df_laps.columns:
                            df_valid = df_laps.dropna(subset=["lap_duration"])
                            if not df_valid.empty:
                                min_row = df_valid.loc[df_valid["lap_duration"].idxmin()]
                                overall_fastest_driver = min_row["driver_number"]
                                
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
                            "Melhor Volta": best_lap_map.get(d_num, "-"),
                            "InPit": d_num in in_pit_drivers
                        })
                    
                    df_display = pd.DataFrame(table_data)
                    df_display = df_display.sort_values(by="Pos").reset_index(drop=True)
                    
                    st.markdown('<div class="timing-container">', unsafe_allow_html=True)
                    for _, row in df_display.iterrows():
                        pos = row["Pos"]
                        d_num = row["Nº"]
                        pos_class = "timing-pos-1" if pos == 1 else ("timing-pos-2" if pos == 2 or pos == 3 else "")
                        pilot = row["Piloto"]
                        team = row["Equipe"]
                        tyre = row["Pneu"]
                        t_class = row["TyreClass"]
                        lap_time = row["Melhor Volta"]
                        in_pit = row["InPit"]
                        
                        time_display = row["Intervalo"] if is_interval else row["Gap"]
                        if pos == 1 and "Race" in raw_session_name:
                            time_display = "LEADER"

                        is_fastest_overall = (d_num == overall_fastest_driver)
                        time_prefix = "⏱️ " if is_fastest_overall else ""
                        time_style = "color: #a855f7; font-weight: 800;" if is_fastest_overall else "color: #f1f5f9;"

                        ms_html = '<span class="mini-sector ms-green"></span><span class="mini-sector ms-purple"></span><span class="mini-sector ms-green"></span>'
                        pit_html = '<div class="pit-badge">PIT</div>' if in_pit else ''

                        row_html = f'<div class="timing-row {pos_class}"><div class="timing-left">{pit_html}<div style="display: flex; flex-direction: column; align-items: center;"><div class="timing-pos">{pos}</div><div style="font-size: 0.6rem; color: #38bdf8; margin-top: 2px; font-weight: 600;">{time_display}</div></div><div><div style="display: flex; align-items: center;"><span class="timing-driver">{pilot}</span></div><div class="timing-team">{team}</div></div></div><div style="display:flex; align-items:center; gap:6px;">{ms_html}</div><div class="timing-right"><div style="text-align: right;"><div class="timing-time" style="{time_style}">{time_prefix}{lap_time}</div></div><span class="tyre-badge {t_class}">{tyre}</span></div></div>'
                        
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
