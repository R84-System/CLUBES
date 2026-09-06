import streamlit as str_lit

str_lit.set_page_config(
    page_title="Painel F1 Pro - Tempo Real & Classificação", page_icon="🏎️", layout="wide"
)

str_lit.markdown(
    """
    <style>
        .block-container {
            padding-top: 0.4rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

f1_dashboard_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <style>
        :root {
            background-color: #0e1117;
            color: #fafafa;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        body {
            margin: 0;
            padding: 4px;
            background-color: #0e1117;
            color: #fafafa;
        }
        .sticky-header-container {
            position: sticky;
            top: 0;
            z-index: 1000;
            background-color: #0e1117;
            padding-bottom: 6px;
        }
        @keyframes blink {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(0.95); }
            100% { opacity: 1; transform: scale(1); }
        }
        .blinking-dot {
            height: 9px;
            width: 9px;
            background-color: #ef4444;
            border-radius: 50%;
            display: inline-block;
            animation: blink 2s infinite ease-in-out;
            margin-right: 5px;
            box-shadow: 0 0 8px #ef4444;
        }
        .card {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
        }
        .controls {
            margin-bottom: 8px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: flex-end;
            background: #dc2626;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #f87171;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .controls select {
            background: #0f172a;
            color: #fff;
            border: 1px solid #334155;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 13px;
            outline: none;
        }
        .standings-table {
            width: 100%;
            border-collapse: collapse;
            background: #1e293b;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #334155;
            margin-top: 10px;
        }
        .standings-table th, .standings-table td {
            padding: 8px 10px;
            text-align: center;
            font-size: 12px;
        }
        .standings-table th {
            background-color: #0f172a;
            color: #f87171;
            font-weight: bold;
        }
        .standings-table tr:nth-child(even) {
            background-color: #162032;
        }
        .standings-table td:nth-child(2) {
            text-align: left;
            font-weight: bold;
        }
        .circuit-canvas-container {
            position: relative;
            background: #090d16;
            border: 1px solid #334155;
            border-radius: 8px;
            height: 380px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        .badge-pit {
            background-color: #eab308;
            color: #000;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: bold;
            margin-left: 5px;
            display: inline-block;
        }
        .waiting-banner {
            background: #0f172a;
            border: 1px dashed #f59e0b;
            padding: 20px;
            text-align: center;
            border-radius: 8px;
            color: #ffb020;
            font-weight: bold;
            margin-bottom: 12px;
        }
    </style>
</head>
<body>
    <div class="sticky-header-container">
        <h3 style="margin-top:0; margin-bottom:6px; display:flex; align-items:center; gap:8px; font-size: 18px;">
            🏎️ F1 Pro - Central de Classificação & Tempo Real
        </h3>
        <div class="controls">
            <div>
                <label style="font-size:11px; color:#fee2e2; display:block; margin-bottom:2px; font-weight:bold;">Visualização</label>
                <select id="viewSelect" onchange="switchView()">
                    <option value="standings" selected>🏆 Classificação & Grid (Pré-Sessão)</option>
                    <option value="live">⚡ Tempo Real (AO VIVO)</option>
                    <option value="calendar">📅 Calendário</option>
                </select>
            </div>
            <div id="gpInfoContainer" style="color: #fff; font-size: 13px; font-weight: bold; display: flex; align-items: center; gap: 10px; padding-bottom: 4px; flex-wrap: wrap;">
                📍 GP Atual: <span id="currentGpName" style="color: #facc15;">Carregando...</span>
                <span id="sessionDetailsBadge" style="background: #0f172a; padding: 3px 8px; border-radius: 4px; font-size: 11px; color: #f87171; border: 1px solid #334155;">Status: Pronto</span>
                <span id="lapCounterBadge" style="background: #0f172a; padding: 3px 8px; border-radius: 4px; font-size: 11px; color: #38bdf8; border: 1px solid #334155; display:none;">Volta: --</span>
            </div>
        </div>
    </div>

    <div id="mainContainer">Carregando dados da Fórmula 1...</div>

    <script>
        let currentView = 'standings';
        let liveInterval = null;

        function switchView() {
            currentView = document.getElementById('viewSelect').value;
            if (liveInterval) {
                clearInterval(liveInterval);
                liveInterval = null;
            }
            loadData();
        }

        async function loadData() {
            let container = document.getElementById('mainContainer');
            if (currentView === 'standings') {
                container.innerHTML = `<div style="text-align:center; color:#94a3b8; padding:20px;">Carregando Classificação do Campeonato e Grid...</div>`;
                fetchStandings();
            } else if (currentView === 'live') {
                container.innerHTML = `
                    <div id="statusBanner" class="waiting-banner">
                        ⏳ SESSÃO NÃO INICIADA OU AGUARDANDO SINAL AO VIVO...<br>
                        <span style="font-size:12px; color:#94a3b8; font-weight:normal;">O painel começará a atualizar automaticamente assim que a sessão iniciar na pista.</span>
                    </div>
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 14px; font-weight: bold; color: #f87171;">
                                <span class="blinking-dot"></span> TELEMETRIA & CIRCUITO EM TEMPO REAL
                            </span>
                            <span id="sessionTitle" style="font-size: 12px; color: #94a3b8;">Aguardando transmissão...</span>
                        </div>
                        <div class="circuit-canvas-container">
                            <canvas id="trackCanvas" width="700" height="360" style="background: #090d16; border-radius: 6px;"></canvas>
                        </div>
                    </div>
                    <div class="card">
                        <div style="font-weight: bold; color: #f87171; margin-bottom: 6px; font-size: 13px;">🏎️ Grid, Intervalos & Pneus em Tempo Real</div>
                        <div id="liveGridContainer">Aguardando início do evento ao vivo...</div>
                    </div>
                `;
                fetchLiveTelemetry();
                liveInterval = setInterval(() => {
                    if (currentView === 'live') fetchLiveTelemetry();
                }, 5000);
            } else if (currentView === 'calendar') {
                container.innerHTML = `<div style="text-align:center; color:#94a3b8; padding:20px;">Carregando calendário de GPs...</div>`;
                fetchCalendar();
            }
        }

        function getTeamShield(teamName) {
            if (!teamName) return '🏎️';
            let t = teamName.toLowerCase();
            if (t.includes('red bull')) return '🐂 RBR';
            if (t.includes('ferrari')) return '🐎 Ferrari';
            if (t.includes('mercedes')) return '⭐ Mercedes';
            if (t.includes('mclaren')) return '🧡 McLaren';
            if (t.includes('aston martin')) return '🟩 Aston Martin';
            if (t.includes('alpine')) return '🔵 Alpine';
            if (t.includes('williams')) return '💙 Williams';
            if (t.includes('rb') || t.includes('visa')) return '🐂 VCARB';
            if (t.includes('sauber') || t.includes('kick')) return '💚 Sauber';
            if (t.includes('haas')) return '🔲 Haas';
            return '🛡️ ' + teamName;
        }

        function getTyreBadge(compound) {
            if (!compound) return '<span style="color:#94a3b8">-</span>';
            let c = compound.toUpperCase();
            if (c.includes('SOFT') || c === 'SOFT') return '<span style="color:#ef4444; font-weight:bold;">🔴 SOFT</span>';
            if (c.includes('MEDIUM') || c === 'MEDIUM') return '<span style="color:#eab308; font-weight:bold;">🟡 MED</span>';
            if (c.includes('HARD') || c === 'HARD') return '<span style="color:#f8fafc; font-weight:bold;">⚪ HARD</span>';
            if (c.includes('INTER') || c === 'INTERMEDIATE') return '<span style="color:#22c55e; font-weight:bold;">🟢 INTER</span>';
            if (c.includes('WET') || c === 'WET') return '<span style="color:#3b82f6; font-weight:bold;">🔵 WET</span>';
            return `<span style="color:#facc15;">${c}</span>`;
        }

        const safeFetch = async (url) => {
            try { let r = await fetch(url); return await r.json(); } catch(e) { return []; }
        };

        async function fetchLiveTelemetry() {
            let sessData = await safeFetch('https://api.openf1.org/v1/sessions?session_key=latest');
            let sessionKey = 'latest';
            let sessionName = 'Sessão AO VIVO';
            if (sessData.length > 0) {
                let s = sessData[0];
                sessionKey = s.session_key;
                sessionName = s.session_name || "Sessão F1";
                document.getElementById('currentGpName').innerText = `${s.location || s.circuit_short_name || 'GP'} (${s.year})`;
                document.getElementById('sessionDetailsBadge').innerText = `Sessão: ${sessionName}`;
                if(document.getElementById('sessionTitle')) {
                    document.getElementById('sessionTitle').innerText = `${s.circuit_short_name || 'Circuito'} - ${sessionName}`;
                }
            }

            let [driversData, posData, intervalsData, stintsData, pitData, lapsData, locData] = await Promise.all([
                safeFetch(`https://api.openf1.org/v1/drivers?session_key=${sessionKey}`),
                safeFetch(`https://api.openf1.org/v1/position?session_key=${sessionKey}`),
                safeFetch(`https://api.openf1.org/v1/intervals?session_key=${sessionKey}`),
                safeFetch(`https://api.openf1.org/v1/stints?session_key=${sessionKey}`),
                safeFetch(`https://api.openf1.org/v1/pit?session_key=${sessionKey}`),
                safeFetch(`https://api.openf1.org/v1/laps?session_key=${sessionKey}`),
                safeFetch(`https://api.openf1.org/v1/location?session_key=${sessionKey}`)
            ]);

            // Se não houver dados ao vivo no momento (ex: antes da largada), usa sessão de referência para exibir o grid base
            let isSimulation = false;
            if (!posData || posData.length === 0 || !locData || locData.length === 0) {
                isSimulation = true;
                sessionKey = 9480; 
                driversData = await safeFetch(`https://api.openf1.org/v1/drivers?session_key=${sessionKey}`);
                posData = await safeFetch(`https://api.openf1.org/v1/position?session_key=${sessionKey}`);
                intervalsData = await safeFetch(`https://api.openf1.org/v1/intervals?session_key=${sessionKey}`);
                stintsData = await safeFetch(`https://api.openf1.org/v1/stints?session_key=${sessionKey}`);
                pitData = await safeFetch(`https://api.openf1.org/v1/pit?session_key=${sessionKey}`);
                lapsData = await safeFetch(`https://api.openf1.org/v1/laps?session_key=${sessionKey}`);
                locData = await safeFetch(`https://api.openf1.org/v1/location?session_key=${sessionKey}`);
            } else {
                let banner = document.getElementById('statusBanner');
                if (banner) banner.style.display = 'none';
            }

            let driverMap = {};
            if (Array.isArray(driversData)) {
                driversData.forEach(d => {
                    driverMap[d.driver_number] = {
                        name: d.broadcast_name || d.full_name,
                        team: d.team_name,
                        color: "#" + (d.team_colour || "ff1801")
                    };
                });
            }

            let latestPositions = {};
            if (Array.isArray(posData)) {
                posData.forEach(p => { latestPositions[p.driver_number] = p.position; });
            }

            let latestIntervals = {};
            if (Array.isArray(intervalsData)) {
                intervalsData.forEach(i => {
                    latestIntervals[i.driver_number] = {
                        gap: i.gap_to_leader !== null ? (i.gap_to_leader === 0 ? 'Líder' : `+${i.gap_to_leader}s`) : '-',
                        interval: i.interval !== null ? `+${i.interval}s` : '-'
                    };
                });
            }

            let latestStints = {};
            if (Array.isArray(stintsData)) {
                stintsData.forEach(st => { latestStints[st.driver_number] = st.compound; });
            }

            let sortedDrivers = Object.keys(latestPositions).sort((a,b) => latestPositions[a] - latestPositions[b]);
            if (sortedDrivers.length === 0) sortedDrivers = Object.keys(driverMap);

            let gridHtml = `
                <table class="standings-table">
                    <thead>
                        <tr>
                            <th>Pos</th>
                            <th>Piloto</th>
                            <th>Equipe / Escudo</th>
                            <th>Nº</th>
                            <th>Gap / Intervalo</th>
                            <th>Pneus</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            sortedDrivers.forEach((num, index) => {
                let dInfo = driverMap[num] || { name: `Piloto #${num}`, team: 'Equipe F1', color: '#facc15' };
                let pos = latestPositions[num] || (index + 1);
                let gapInfo = latestIntervals[num] || { gap: '-', interval: '-' };
                let tyre = latestStints[num] || 'SOFT';
                let tyreBadgeHtml = getTyreBadge(tyre);
                let teamShield = getTeamShield(dInfo.team);

                gridHtml += `
                    <tr>
                        <td><b>P${pos}</b></td>
                        <td style="border-left: 4px solid ${dInfo.color}; text-align: left; padding-left: 8px;">
                            ${dInfo.name}
                        </td>
                        <td>${teamShield}</td>
                        <td>#${num}</td>
                        <td><span style="color:#f87171; font-weight:bold;">${gapInfo.gap}</span></td>
                        <td>${tyreBadgeHtml}</td>
                    </tr>
                `;
            });
            gridHtml += `</tbody></table>`;
            let gridContainer = document.getElementById('liveGridContainer');
            if (gridContainer) gridContainer.innerHTML = gridHtml;
        }

        async function fetchStandings() {
            try {
                let resD = await safeFetch('https://api.jolpi.ca/ergast/f1/current/driverStandings.json');
                let dStandings = resD.MRData?.StandingsTable?.StandingsLists[0]?.DriverStandings || [];

                let resC = await safeFetch('https://api.jolpi.ca/ergast/f1/current/constructorStandings.json');
                let cStandings = resC.MRData?.StandingsTable?.StandingsLists[0]?.ConstructorStandings || [];

                document.getElementById('currentGpName').innerText = "Temporada Atual";
                document.getElementById('sessionDetailsBadge').innerText = "Classificação Geral";

                let html = `
                    <div class="card">
                        <h3 style="color:#f87171; margin-top:0; margin-bottom:8px; font-size:15px;">🏆 Campeonato de Pilotos</h3>
                        <table class="standings-table">
                            <thead>
                                <tr><th>Pos</th><th>Piloto</th><th>Equipe</th><th>Pontos</th><th>Vitórias</th></tr>
                            </thead>
                            <tbody>
                `;
                dStandings.forEach(ds => {
                    let team = ds.Constructors[0] ? ds.Constructors[0].name : '';
                    html += `
                        <tr>
                            <td><b>${ds.position}</b></td>
                            <td>${ds.Driver.givenName} ${ds.Driver.familyName}</td>
                            <td>${team}</td>
                            <td><b>${ds.points}</b></td>
                            <td>${ds.wins}</td>
                        </tr>
                    `;
                });
                html += `</tbody></table></div>`;

                html += `
                    <div class="card">
                        <h3 style="color:#f87171; margin-top:0; margin-bottom:8px; font-size:15px;">🛠️ Campeonato de Construtores</h3>
                        <table class="standings-table">
                            <thead>
                                <tr><th>Pos</th><th>Construtor</th><th>Nacionalidade</th><th>Pontos</th><th>Vitórias</th></tr>
                            </thead>
                            <tbody>
                `;
                cStandings.forEach(cs => {
                    html += `
                        <tr>
                            <td><b>${cs.position}</b></td>
                            <td>${cs.Constructor.name}</td>
                            <td>${cs.Constructor.nationality}</td>
                            <td><b>${cs.points}</b></td>
                            <td>${cs.wins}</td>
                        </tr>
                    `;
                });
                html += `</tbody></table></div>`;

                document.getElementById('mainContainer').innerHTML = html;
            } catch(e) {
                document.getElementById('mainContainer').innerHTML = "<div style='text-align:center; color:#94a3b8; padding:20px;'>Erro ao carregar a classificação do campeonato.</div>";
            }
        }

        async function fetchCalendar() {
            try {
                let res = await safeFetch('https://api.jolpi.ca/ergast/f1/current.json');
                let races = res.MRData?.RaceTable?.Races || [];
                document.getElementById('currentGpName').innerText = "Calendário " + (res.MRData?.season || '');
                document.getElementById('sessionDetailsBadge').innerText = "Temporada Regular";

                let html = `
                    <div class="card">
                        <h3 style="color:#f87171; margin-top:0; margin-bottom:8px; font-size:15px;">📅 Calendário da Temporada F1</h3>
                        <table class="standings-table">
                            <thead>
                                <tr><th>Etapa</th><th>Nome do GP</th><th>Circuito</th><th>Data</th></tr>
                            </thead>
                            <tbody>
                `;
                races.forEach(r => {
                    html += `
                        <tr>
                            <td><b>R${r.round}</b></td>
                            <td>${r.raceName}</td>
                            <td>${r.Circuit.circuitName} (${r.Circuit.Location.locality}, ${r.Circuit.Location.country})</td>
                            <td>${r.date}</td>
                        </tr>
                    `;
                });
                html += `</tbody></table></div>`;
                document.getElementById('mainContainer').innerHTML = html;
            } catch(e) {
                document.getElementById('mainContainer').innerHTML = "<div style='text-align:center; color:#94a3b8; padding:20px;'>Erro ao carregar o calendário.</div>";
            }
        }

        loadData();
    </script>
</body>
</html>
"""

str_lit.components.v1.html(f1_dashboard_html, height=850, scrolling=True)
