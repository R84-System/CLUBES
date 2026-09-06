import streamlit as str_lit

str_lit.set_page_config(
    page_title="Painel F1 Pro - Telemetria & AO VIVO", page_icon="🏎️", layout="wide"
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
    </style>
</head>
<body>
    <div class="sticky-header-container">
        <h3 style="margin-top:0; margin-bottom:6px; display:flex; align-items:center; gap:8px; font-size: 18px;">
            🏎️ F1 Pro Telemetry & Live Command Center
        </h3>
        <div class="controls">
            <div>
                <label style="font-size:11px; color:#fee2e2; display:block; margin-bottom:2px; font-weight:bold;">Visualização</label>
                <select id="viewSelect" onchange="switchView()">
                    <option value="live">⚡ Telemetria & Circuito AO VIVO</option>
                    <option value="calendar">📅 Calendário & Próximos GPs</option>
                    <option value="standings">🏆 Classificação (Pilotos & Construtores)</option>
                </select>
            </div>
            <div id="gpInfoContainer" style="color: #fff; font-size: 13px; font-weight: bold; display: flex; align-items: center; gap: 6px; padding-bottom: 4px;">
                📍 GP Atual: <span id="currentGpName" style="color: #facc15;">Carregando...</span>
            </div>
        </div>
    </div>

    <div id="mainContainer">Carregando dados da Fórmula 1...</div>

    <script>
        let currentView = 'live';

        function switchView() {
            currentView = document.getElementById('viewSelect').value;
            loadData();
        }

        async function loadData() {
            let container = document.getElementById('mainContainer');
            if (currentView === 'live') {
                container.innerHTML = `
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 14px; font-weight: bold; color: #f87171;">
                                <span class="blinking-dot"></span> SESSÃO AO VIVO - TELEMETRIA DE POSIÇÃO
                            </span>
                            <span id="sessionTitle" style="font-size: 12px; color: #94a3b8;">Conectando à OpenF1 API...</span>
                        </div>
                        <div class="circuit-canvas-container">
                            <canvas id="trackCanvas" width="700" height="360" style="background: #090d16; border-radius: 6px;"></canvas>
                        </div>
                    </div>
                    <div class="card">
                        <div style="font-weight: bold; color: #f87171; margin-bottom: 6px; font-size: 13px;">🏎️ Grid & Posições Atuais</div>
                        <div id="liveGridContainer">Carregando posições...</div>
                    </div>
                `;
                fetchLiveTelemetry();
            } else if (currentView === 'calendar') {
                container.innerHTML = `<div style="text-align:center; color:#94a3b8; padding:20px;">Carregando calendário de GPs (Jolpica F1)...</div>`;
                fetchCalendar();
            } else if (currentView === 'standings') {
                container.innerHTML = `<div style="text-align:center; color:#94a3b8; padding:20px;">Carregando classificação do campeonato...</div>`;
                fetchStandings();
            }
        }

        async function fetchLiveTelemetry() {
            try {
                let sessRes = await fetch('https://api.openf1.org/v1/sessions?session_key=latest');
                let sessData = await sessRes.json();
                
                let sessionKey = 'latest';
                if (sessData.length > 0) {
                    let s = sessData[0];
                    document.getElementById('currentGpName').innerText = (s.session_name || "Sessão F1") + " (" + s.year + ")";
                    document.getElementById('sessionTitle').innerText = s.circuit_short_name || s.location || "Circuito F1";
                    sessionKey = s.session_key;
                }

                let driversRes = await fetch(`https://api.openf1.org/v1/drivers?session_key=${sessionKey}`);
                let driversData = await driversRes.json();
                let driverMap = {};
                driversData.forEach(d => {
                    driverMap[d.driver_number] = {
                        name: d.broadcast_name || d.full_name,
                        team: d.team_name,
                        color: "#" + (d.team_colour || "ff1801")
                    };
                });

                let posRes = await fetch(`https://api.openf1.org/v1/position?session_key=${sessionKey}`);
                let posData = await posRes.json();
                
                let gridHtml = `
                    <table class="standings-table">
                        <thead>
                            <tr><th>Pos</th><th>Piloto</th><th>Equipe</th><th>Nº</th></tr>
                        </thead>
                        <tbody>
                `;
                let latestPositions = {};
                posData.forEach(p => { latestPositions[p.driver_number] = p.position; });
                
                let sortedDrivers = Object.keys(latestPositions).sort((a,b) => latestPositions[a] - latestPositions[b]);
                if (sortedDrivers.length === 0) sortedDrivers = Object.keys(driverMap);

                if (sortedDrivers.length === 0) {
                    gridHtml += `<tr><td colspan="4" style="color: #94a3b8; padding: 15px;">Aguardando dados de grid para esta sessão...</td></tr>`;
                } else {
                    sortedDrivers.forEach((num, index) => {
                        let dInfo = driverMap[num] || { name: `Piloto #${num}`, team: 'Equipe F1', color: '#facc15' };
                        let pos = latestPositions[num] || (index + 1);
                        gridHtml += `
                            <tr>
                                <td><b>P${pos}</b></td>
                                <td style="border-left: 4px solid ${dInfo.color};">${dInfo.name}</td>
                                <td>${dInfo.team}</td>
                                <td>#${num}</td>
                            </tr>
                        `;
                    });
                }
                gridHtml += `</tbody></table>`;
                let gridContainer = document.getElementById('liveGridContainer');
                if (gridContainer) gridContainer.innerHTML = gridHtml;

                let locRes = await fetch(`https://api.openf1.org/v1/location?session_key=${sessionKey}`);
                let locData = await locRes.json();
                
                // Se não houver dados de localização na sessão "latest" (ex: intervalo entre GPs), buscamos uma sessão recente garantida (ex: GP do Bahrein / Monza recente) para exibir o traçado
                if (locData.length === 0) {
                    let fallbackRes = await fetch('https://api.openf1.org/v1/location?session_key=9616'); // Exemplo de chave de sessão válida com dados de pista
                    locData = await fallbackRes.json();
                }

                let canvas = document.getElementById('trackCanvas');
                if (canvas) {
                    let ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    let xCoords = locData.map(l => l.x);
                    let yCoords = locData.map(l => l.y);
                    if (xCoords.length > 0) {
                        let minX = Math.min(...xCoords), maxX = Math.max(...xCoords);
                        let minY = Math.min(...yCoords), maxY = Math.max(...yCoords);

                        ctx.strokeStyle = '#334155';
                        ctx.lineWidth = 3;
                        ctx.beginPath();
                        let first = true;
                        locData.forEach(l => {
                            let cx = ((l.x - minX) / (maxX - minX || 1)) * 620 + 40;
                            let cy = ((l.y - minY) / (maxY - minY || 1)) * 300 + 30;
                            if (first) { ctx.moveTo(cx, cy); first = false; } else { ctx.lineTo(cx, cy); }
                        });
                        ctx.stroke();

                        let latestLocs = {};
                        locData.forEach(l => { latestLocs[l.driver_number] = l; });

                        Object.keys(latestLocs).forEach(num => {
                            let l = latestLocs[num];
                            let dInfo = driverMap[num] || { color: '#facc15' };
                            let cx = ((l.x - minX) / (maxX - minX || 1)) * 620 + 40;
                            let cy = ((l.y - minY) / (maxY - minY || 1)) * 300 + 30;

                            ctx.beginPath();
                            ctx.arc(cx, cy, 5, 0, 2 * Math.PI);
                            ctx.fillStyle = dInfo.color;
                            ctx.fill();
                            ctx.lineWidth = 1;
                            ctx.strokeStyle = '#fff';
                            ctx.stroke();

                            ctx.fillStyle = '#fff';
                            ctx.font = '9px sans-serif';
                            ctx.fillText(num, cx + 7, cy + 3);
                        });
                    } else {
                        ctx.fillStyle = '#f87171';
                        ctx.font = '13px sans-serif';
                        ctx.fillText("Aguardando telemetria ativa para desenhar o circuito...", 180, 185);
                    }
                }
            } catch(e) {
                console.error(e);
            }
        }

        async function fetchCalendar() {
            try {
                let res = await fetch('https://api.jolpi.ca/ergast/f1/current.json');
                let data = await res.json();
                let races = data.MRData.RaceTable.Races;
                document.getElementById('currentGpName').innerText = "Calendário " + data.MRData.season;

                let html = `
                    <h3 style="color:#f87171; margin-bottom:8px; font-size:15px;">📅 Calendário da Temporada F1</h3>
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
                html += `</tbody></table>`;
                document.getElementById('mainContainer').innerHTML = html;
            } catch(e) {
                document.getElementById('mainContainer').innerHTML = "<div style='text-align:center; color:#94a3b8; padding:20px;'>Erro ao carregar o calendário.</div>";
            }
        }

        async function fetchStandings() {
            try {
                let resD = await fetch('https://api.jolpi.ca/ergast/f1/current/driverStandings.json');
                let dataD = await resD.json();
                let dStandings = dataD.MRData.StandingsTable.StandingsLists[0].DriverStandings;

                let resC = await fetch('https://api.jolpi.ca/ergast/f1/current/constructorStandings.json');
                let dataC = await resC.json();
                let cStandings = dataC.MRData.StandingsTable.StandingsLists[0].ConstructorStandings;

                document.getElementById('currentGpName').innerText = "Classificação do Campeonato";

                let html = `
                    <h3 style="color:#f87171; margin-bottom:8px; font-size:15px;">🏆 Campeonato de Pilotos</h3>
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
                html += `</tbody></table>`;

                html += `
                    <h3 style="color:#f87171; margin-top:20px; margin-bottom:8px; font-size:15px;">🛠️ Campeonato de Construtores</h3>
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
                html += `</tbody></table>`;

                document.getElementById('mainContainer').innerHTML = html;
            } catch(e) {
                document.getElementById('mainContainer').innerHTML = "<div style='text-align:center; color:#94a3b8; padding:20px;'>Erro ao carregar a classificação.</div>";
            }
        }

        loadData();
        setInterval(() => {
            if (currentView === 'live') fetchLiveTelemetry();
        }, 5000);
    </script>
</body>
</html>
"""

str_lit.components.v1.html(f1_dashboard_html, height=850, scrolling=True)
