import streamlit as str_lit

str_lit.set_page_config(
    page_title="Painel F1 Pro - Tempo Real & Pits", page_icon="🏎️", layout="wide"
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
        .waiting-banner {
            background: #0f172a;
            border: 1px dashed #f59e0b;
            padding: 15px;
            text-align: center;
            border-radius: 8px;
            color: #ffb020;
            font-weight: bold;
            margin-bottom: 12px;
            font-size: 13px;
        }
        .alert-banner {
            padding: 10px 15px;
            border-radius: 6px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
            font-size: 13px;
            display: none;
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
        .badge-out {
            background-color: #ef4444;
            color: #fff;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: bold;
            margin-left: 5px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="sticky-header-container">
        <h3 style="margin-top:0; margin-bottom:6px; display:flex; align-items:center; gap:8px; font-size: 18px;">
            🏎️ F1 Pro - Central de Classificação & Tempo Real
        </h3>
        
        <div id="raceControlAlert" class="alert-banner"></div>

        <div class="controls">
            <div>
                <label style="font-size:11px; color:#fee2e2; display:block; margin-bottom:2px; font-weight:bold;">Visualização</label>
                <select id="viewSelect" onchange="switchView()">
                    <option value="standings">🏆 Classificação & Grid (Campeonato)</option>
                    <option value="live" selected>⚡ Tempo Real (AO VIVO)</option>
                    <option value="calendar">📅 Calendário</option>
                </select>
            </div>
            <div id="gpInfoContainer" style="color: #fff; font-size: 13px; font-weight: bold; display: flex; align-items: center; gap: 10px; padding-bottom: 4px; flex-wrap: wrap;">
                📍 GP Atual: <span id="currentGpName" style="color: #facc15;">Carregando...</span>
                <span id="sessionTypeBadge" style="background: #1e293b; padding: 3px 8px; border-radius: 4px; font-size: 11px; color: #facc15; border: 1px solid #334155;">Sessão: --</span>
                <span id="sessionDetailsBadge" style="background: #0f172a; padding: 3px 8px; border-radius: 4px; font-size: 11px; color: #f87171; border: 1px solid #334155;">Status: AO VIVO</span>
                <span id="lapCounterBadge" style="background: #0f172a; padding: 3px 8px; border-radius: 4px; font-size: 11px; color: #38bdf8; border: 1px solid #334155; display:none;">Volta: --</span>
            </div>
        </div>
    </div>

    <div id="mainContainer">Carregando dados da Fórmula 1...</div>

    <script>
        let currentView = 'live';
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
                        ⏳ CONECTANDO À SESSÃO AO VIVO (OpenF1)...<br>
                        <span style="font-size:12px; color:#94a3b8; font-weight:normal;">O painel atualizará automaticamente assim que a telemetria estiver ativa.</span>
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
                        <div style="font-weight: bold; color: #f87171; margin-bottom: 6px; font-size: 13px;">🏎️ Grid, Tempos de Volta, Pits, Pneus & Voltas</div>
                        <table id="liveTable" class="standings-table">
                            <thead>
                                <tr>
                                    <th>Pos</th>
                                    <th>Piloto</th>
                                    <th>Equipe / Escudo</th>
                                    <th>Nº</th>
                                    <th>Tempo da Volta</th>
                                    <th>Gap p/ Líder</th>
                                    <th>Intervalo</th>
                                    <th>Pneus</th>
                                    <th>Volta Atual</th>
                                </tr>
                            </thead>
                            <tbody id="liveTableBody">
                                <tr><td colspan="9" style="text-align:center; color:#94a3b8; padding:20px;">Carregando pilotos da sessão atual...</td></tr>
                            </tbody>
                        </table>
                    </div>
                `;
                fetchLiveTelemetry();
                if (!liveInterval) {
                    liveInterval = setInterval(() => {
                        if (currentView === 'live') fetchLiveTelemetry();
                    }, 5000);
                }
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

        function formatLapTime(seconds) {
            if (!seconds || isNaN(seconds)) return '-';
            let mins = Math.floor(seconds / 60);
            let secs = (seconds % 60).toFixed(3);
            return mins > 0 ? `${mins}:${secs < 10 ? '0' : ''}${secs}` : `${secs}s`;
        }

        function classifySessionName(name) {
            if (!name) return { label: 'Sessão F1', type: 'other' };
            let n = name.toLowerCase();
            if (n.includes('practice') || n.includes('treino')) return { label: '🛠️ Treino Livre', type: 'practice' };
            if (n.includes('qualifying') || n.includes('quali')) {
                if (n.includes('q1')) return { label: '⏱️ Q1', type: 'quali' };
                if (n.includes('q2')) return { label: '⏱️ Q2', type: 'quali' };
                if (n.includes('q3')) return { label: '⏱️ Q3', type: 'quali' };
                return { label: '⏱️ Qualificação', type: 'quali' };
            }
            if (n.includes('sprint')) return { label: '🏁 Sprint', type: 'sprint' };
            if (n.includes('race') || n.includes('grand prix') || n.includes('corrida')) return { label: '🏁 Corrida Oficial', type: 'race' };
            return { label: name, type: 'other' };
        }

        const safeFetch = async (url) => {
            try { let r = await fetch(url); return await r.json(); } catch(e) { return []; }
        };

        async function fetchLiveTelemetry() {
            let sessData = await safeFetch('https://api.openf1.org/v1/sessions?session_key=latest');
            let sessionKey = 'latest';
            let sessionName = 'Sessão AO VIVO';
            let circuitName = 'Circuito';
            let year = new Date().getFullYear();

            if (Array.isArray(sessData) && sessData.length > 0) {
                let s = sessData[sessData.length - 1]; // Pega a última sessão válida
                sessionKey = s.session_key;
                sessionName = s.session_name || "Sessão F1";
                circuitName = s.circuit_short_name || s.location || "Circuito";
                year = s.year || year;
                let gpElem = document.getElementById('currentGpName');
                if (gpElem) gpElem.innerText = `${s.location || circuitName} (${year})`;
                
                let sessionMeta = classifySessionName(sessionName);
                let typeBadge = document.getElementById('sessionTypeBadge');
                let detailsBadge = document.getElementById('sessionDetailsBadge');
                if (typeBadge) typeBadge.innerText = sessionMeta.label;
                if (detailsBadge) detailsBadge.innerText = `Status: AO VIVO`;
                let sessionTitleElem = document.getElementById('sessionTitle');
                if(sessionTitleElem) {
                    sessionTitleElem.innerText = `${circuitName} - ${sessionName} (Key: ${sessionKey})`;
                }
            }

            let [driversData, posData, intervalsData, stintsData, lapsData, locData, raceControlData, pitsData] = await Promise.all([
                safeFetch(`https://api.openf1.org/v1/drivers?session_key=${sessionKey}`),
                safeFetch(`https://api.openf1.org/v1/position?session_key=${sessionKey}`),
                safeFetch(`https://api.openf1.org/v1/intervals?session_key=${sessionKey}`),
                safeFetch(`https://api.openf1.org/v1/stints?session_key=${sessionKey}`),
                safeFetch(`https://api.openf1.org/v1/laps?session_key=${sessionKey}`),
                safeFetch(`https://api.openf1.org/v1/location?session_key=${sessionKey}`),
                safeFetch(`https://api.openf1.org/v1/race_control?session_key=${sessionKey}`),
                safeFetch(`https://api.openf1.org/v1/pits?session_key=${sessionKey}`)
            ]);

            // SEM FALLBACK FIXO: Mantém sempre a sessão atual ao vivo, mesmo que os dados ainda estejam chegando
            let banner = document.getElementById('statusBanner');
            if ((!posData || posData.length === 0) && (!driversData || driversData.length === 0)) {
                if (banner) {
                    banner.style.display = 'block';
                    banner.innerHTML = `⏳ SESSÃO AO VIVO CONECTADA (Key: ${sessionKey}), MAS OS DADOS AINDA ESTÃO SENDO LIBERADOS PELA FIA...`;
                }
            } else {
                if (banner) banner.style.display = 'none';
            }

            let alertBox = document.getElementById('raceControlAlert');
            if (Array.isArray(raceControlData) && raceControlData.length > 0) {
                let latestRC = raceControlData[raceControlData.length - 1];
                let msg = (latestRC.message || '').toUpperCase();
                let flag = (latestRC.flag || '').toUpperCase();
                let category = (latestRC.category || '').toUpperCase();

                let alertText = "";
                let alertBg = "#1e293b";
                let alertColor = "#fff";
                let showAlert = false;

                if (msg.includes('SAFETY CAR') || category.includes('SAFETYCAR')) {
                    alertText = `🚨 ALERTA DIREÇÃO DE PROVA: ${latestRC.message}`;
                    alertBg = "#ca8a04"; alertColor = "#000"; showAlert = true;
                } else if (flag === 'YELLOW' || msg.includes('YELLOW FLAG')) {
                    alertText = `⚠️ BANDEIRA AMARELA: ${latestRC.message}`;
                    alertBg = "#eab308"; alertColor = "#000"; showAlert = true;
                } else if (flag === 'RED' || msg.includes('RED FLAG')) {
                    alertText = `🛑 BANDEIRA VERMELHA: ${latestRC.message}`;
                    alertBg = "#dc2626"; alertColor = "#fff"; showAlert = true;
                } else if (flag === 'GREEN' || msg.includes('TRACK CLEAR')) {
                    alertText = `🟢 PISTA LIVRE / BANDEIRA VERDE`;
                    alertBg = "#16a34a"; alertColor = "#fff"; showAlert = true;
                } else if (msg.includes('CHECKERED') || flag === 'CHEQUERED') {
                    alertText = `🏁 BANDEIRA QUADRICULADA! FIM DE SESSÃO.`;
                    alertBg = "#334155"; alertColor = "#facc15"; showAlert = true;
                }

                if (showAlert && alertBox) {
                    alertBox.style.display = 'block';
                    alertBox.style.background = alertBg;
                    alertBox.style.color = alertColor;
                    alertBox.innerHTML = alertText;
                } else if (alertBox) {
                    alertBox.style.display = 'none';
                }
            } else if (alertBox) {
                alertBox.style.display = 'none';
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

            let maxLapNum = 0;
            let driverCurrentLap = {};
            let driverLastLapTime = {};
            let fastestLapDriverNum = null;
            let minLapTime = Infinity;

            if (Array.isArray(lapsData)) {
                lapsData.forEach(l => {
                    if (l.lap_number > maxLapNum) maxLapNum = l.lap_number;
                    if (!driverCurrentLap[l.driver_number] || l.lap_number > driverCurrentLap[l.driver_number]) {
                        driverCurrentLap[l.driver_number] = l.lap_number;
                    }
                    if (!driverLastLapTime[l.driver_number] || l.lap_number >= driverLastLapTime[l.driver_number].lap) {
                        driverLastLapTime[l.driver_number] = { lap: l.lap_number, duration: l.lap_duration };
                    }
                    if (l.lap_duration && l.lap_duration < minLapTime) {
                        minLapTime = l.lap_duration;
                        fastestLapDriverNum = l.driver_number;
                    }
                });
            }

            let inPitSet = {};
            if (Array.isArray(pitsData)) {
                pitsData.forEach(p => {
                    if (p.lap_number === driverCurrentLap[p.driver_number] && (p.pit_duration === null || p.pit_duration === undefined)) {
                        inPitSet[p.driver_number] = true;
                    }
                });
            }

            let totalLapsEst = maxLapNum > 0 ? Math.max(maxLapNum, 57) : 57;
            let currentLapBadge = document.getElementById('lapCounterBadge');
            if (currentLapBadge) {
                currentLapBadge.style.display = 'inline-block';
                currentLapBadge.innerText = `Volta: ${maxLapNum || '--'} / ${totalLapsEst}`;
            }

            let isRaceFinished = false;
            let sessionMeta = classifySessionName(sessionName);
            if (sessionMeta.type === 'race' && maxLapNum >= totalLapsEst - 1 && maxLapNum > 0) {
                isRaceFinished = true;
            }

            let sortedDrivers = Object.keys(latestPositions).sort((a,b) => latestPositions[a] - latestPositions[b]);
            if (sortedDrivers.length === 0) sortedDrivers = Object.keys(driverMap);

            let tbody = document.getElementById('liveTableBody');
            if (!tbody) return;

            if (sortedDrivers.length === 0) {
                tbody.innerHTML = `<tr><td colspan="9" style="text-align:center; color:#94a3b8; padding:20px;">Sessão ativa, mas a tabela de pilotos ainda está vazia na API. Aguarde...</td></tr>`;
                return;
            }

            sortedDrivers.forEach((num, index) => {
                let dInfo = driverMap[num] || { name: `Piloto #${num}`, team: 'Equipe F1', color: '#facc15' };
                let pos = latestPositions[num] || (index + 1);
                let gapInfo = latestIntervals[num] || { gap: '-', interval: '-' };
                let tyre = latestStints[num] || 'SOFT';
                let tyreBadgeHtml = getTyreBadge(tyre);
                let teamShield = getTeamShield(dInfo.team);
                let dLap = driverCurrentLap[num] || maxLapNum || '-';
                
                let lapTimeData = driverLastLapTime[num];
                let formattedTime = lapTimeData ? formatLapTime(lapTimeData.duration) : '-';

                let isFastest = (parseInt(num) === parseInt(fastestLapDriverNum));
                let fastestBadge = isFastest ? ' <span title="Volta Mais Rápida" style="cursor:help;">⏱️</span>' : '';
                let winnerBadge = (isRaceFinished && pos === 1) ? ' <span>🏁</span>' : '';
                let pitBadge = inPitSet[num] ? ' <span class="badge-pit">PIT</span>' : '';
                let isAbandoned = (maxLapNum > 5 && dLap !== '-' && (maxLapNum - dLap > 5));
                let outBadge = isAbandoned ? ' <span class="badge-out">OUT LAP</span>' : '';

                let rowId = `row-driver-${num}`;
                let row = document.getElementById(rowId);

                if (!row) {
                    row = document.createElement('tr');
                    row.id = rowId;
                    row.innerHTML = `
                        <td id="cell-pos-${num}"><b>P${pos}</b></td>
                        <td id="cell-name-${num}" style="border-left: 4px solid ${dInfo.color}; text-align: left; padding-left: 8px;">${dInfo.name}</td>
                        <td id="cell-team-${num}">${teamShield}</td>
                        <td id="cell-num-${num}">#${num}</td>
                        <td id="cell-time-${num}"><span style="color:#facc15; font-weight:bold;">${formattedTime}</span></td>
                        <td id="cell-gap-${num}"><span style="color:#f87171; font-weight:bold;">${gapInfo.gap}</span></td>
                        <td id="cell-interval-${num}"><span style="color:#38bdf8;">${gapInfo.interval}</span></td>
                        <td id="cell-tyre-${num}">${tyreBadgeHtml}</td>
                        <td id="cell-lap-${num}"><b>${dLap}</b></td>
                    `;
                    tbody.appendChild(row);
                } else {
                    let cPos = document.getElementById(`cell-pos-${num}`);
                    let cName = document.getElementById(`cell-name-${num}`);
                    let cTeam = document.getElementById(`cell-team-${num}`);
                    let cNum = document.getElementById(`cell-num-${num}`);
                    let cTime = document.getElementById(`cell-time-${num}`);
                    let cGap = document.getElementById(`cell-gap-${num}`);
                    let cInterval = document.getElementById(`cell-interval-${num}`);
                    let cTyre = document.getElementById(`cell-tyre-${num}`);
                    let cLap = document.getElementById(`cell-lap-${num}`);

                    if (cPos) cPos.innerHTML = `<b>P${pos}</b>`;
                    if (cName) {
                        cName.style.borderLeftColor = dInfo.color;
                        cName.innerHTML = `${dInfo.name} ${fastestBadge} ${winnerBadge} ${pitBadge} ${outBadge}`;
                    }
                    if (cTeam) cTeam.innerHTML = teamShield;
                    if (cNum) cNum.innerText = `#${num}`;
                    if (cTime) cTime.innerHTML = `<span style="color:#facc15; font-weight:bold;">${formattedTime}</span>`;
                    if (cGap) cGap.innerHTML = `<span style="color:#f87171; font-weight:bold;">${gapInfo.gap}</span>`;
                    if (cInterval) cInterval.innerHTML = `<span style="color:#38bdf8;">${gapInfo.interval}</span>`;
                    if (cTyre) cTyre.innerHTML = tyreBadgeHtml;
                    if (cLap) cLap.innerHTML = `<b>${dLap}</b>`;
                }
                
                tbody.appendChild(row);
            });

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
                    ctx.fillText("Aguardando telemetria ativa para desenhar o circuito...", 160, 185);
                }
            }
        }

        async function fetchStandings() {
            try {
                let resD = await safeFetch('https://api.jolpi.ca/ergast/f1/current/driverStandings.json');
                let dStandings = resD.MRData?.StandingsTable?.StandingsLists[0]?.DriverStandings || [];

                let resC = await safeFetch('https://api.jolpi.ca/ergast/f1/current/constructorStandings.json');
                let cStandings = resC.MRData?.StandingsTable?.StandingsLists[0]?.ConstructorStandings || [];

                document.getElementById('currentGpName').innerText = "Temporada Atual";
                document.getElementById('sessionTypeBadge').innerText = "Campeonato Geral";
                document.getElementById('sessionDetailsBadge').innerText = "Tabela Oficial";
                document.getElementById('raceControlAlert').style.display = 'none';

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
                document.getElementById('sessionTypeBadge').innerText = "Temporada Regular";
                document.getElementById('sessionDetailsBadge').innerText = "Etapas";
                document.getElementById('raceControlAlert').style.display = 'none';

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
