import streamlit as st

# 1. Configuração da Página para Largura Total
st.set_page_config(
    page_title="F1 Live Telemetry & Track Map",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Ocultação do cabeçalho, rodapé e ajuste de margens nativas
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 0.4rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp { background-color: #0e1117; }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Código HTML/JS com Pista SVG Animada e Tempo Real
f1_live_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #0e1117;
            color: #ffffff;
            margin: 0;
            padding: 0;
        }
        .f1-header {
            background: linear-gradient(90deg, #e10600 0%, #15151e 70%);
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.6);
            margin-bottom: 12px;
        }
        .f1-logo {
            font-size: 20px;
            font-weight: 900;
            font-style: italic;
            letter-spacing: 2px;
            color: #ffffff;
        }
        .f1-logo span {
            color: #e10600;
            background: #ffffff;
            padding: 2px 6px;
            border-radius: 4px;
            margin-left: 4px;
        }
        .live-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(34, 197, 94, 0.2);
            border: 1px solid #22c55e;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            color: #4ade80;
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: #22c55e;
            border-radius: 50%;
            box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7);
            animation: pulse-ring 1.5s infinite;
        }
        @keyframes pulse-ring {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
        }

        .grid-container {
            display: grid;
            grid-template-columns: 1.2fr 1fr;
            gap: 15px;
            margin-bottom: 15px;
        }
        @media (max-width: 900px) {
            .grid-container { grid-template-columns: 1fr; }
        }

        .card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }
        .card-title {
            font-size: 14px;
            font-weight: bold;
            color: #f0f6fc;
            margin-bottom: 10px;
            border-bottom: 1px solid #30363d;
            padding-bottom: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* Container do Mapa da Pista */
        .track-container {
            position: relative;
            background: #0d1117;
            border-radius: 6px;
            border: 1px solid #21262d;
            height: 320px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        
        /* Legenda dos carros */
        .track-legend {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
            font-size: 11px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 5px;
            background: #0d1117;
            padding: 3px 8px;
            border-radius: 4px;
            border: 1px solid #30363d;
        }
        .legend-color {
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }

        /* Tabelas */
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }
        th, td {
            padding: 6px 8px;
            text-align: left;
            border-bottom: 1px solid #21262d;
        }
        th { color: #8b949e; background: #0d1117; font-weight: 600; }
        tr:hover { background: #1f242c; }
        .pos-1 { color: #facc15; font-weight: bold; }
        .pos-2 { color: #e5e7eb; font-weight: bold; }
        .pos-3 { color: #fb923c; font-weight: bold; }

        /* Telemetria Ao Vivo */
        .telemetry-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            margin-top: 8px;
        }
        .tele-box {
            background: #0d1117;
            border: 1px solid #30363d;
            padding: 8px;
            border-radius: 6px;
            text-align: center;
        }
        .tele-label { font-size: 10px; color: #8b949e; text-transform: uppercase; }
        .tele-val { font-size: 16px; font-weight: bold; color: #58a6ff; margin-top: 2px; }
    </style>
</head>
<body>

    <!-- Header com Relógio Ativo -->
    <div class="f1-header">
        <div class="f1-logo">FORMULA 1 <span>LIVE TRACK</span></div>
        <div class="live-indicator">
            <div class="pulse-dot"></div>
            SESSÃO AO VIVO <span id="live-timer" style="margin-left: 5px; font-family: monospace;">00:00:00</span>
        </div>
    </div>

    <div class="grid-container">
        <!-- Coluna Esquerda: Mini-mapa do Circuito com pontos correndo -->
        <div class="card">
            <div class="card-title">
                <span>🗺️ Mapa do Circuito (Telemetria em Tempo Real)</span>
                <span style="font-size: 11px; color: #8b949e;" id="lap-counter">Volta 48 / 78</span>
            </div>
            
            <div class="track-container">
                <!-- Traçado SVG do Circuito -->
                <svg width="100%" height="100%" viewBox="0 0 500 300" style="position: absolute;">
                    <!-- Sombra e Linha da Pista -->
                    <path id="race-track" d="M 60 150 C 60 60, 140 40, 220 50 C 320 60, 420 80, 430 150 C 440 220, 360 260, 260 260 C 160 260, 100 240, 70 200 Z" 
                          fill="none" stroke="#21262d" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M 60 150 C 60 60, 140 40, 220 50 C 320 60, 420 80, 430 150 C 440 220, 360 260, 260 260 C 160 260, 100 240, 70 200 Z" 
                          fill="none" stroke="#30363d" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>

                <!-- Pontos dos Carros injetados via JavaScript -->
                <div id="cars-container" style="position: absolute; width: 100%; height: 100%; pointer-events: none;"></div>
            </div>

            <!-- Legenda com Cores das Equipes -->
            <div class="track-legend" id="track-legend"></div>
        </div>

        <!-- Coluna Direita: Tabela de Posições e Telemetria do Líder -->
        <div class="card">
            <div class="card-title">
                <span>📊 Classificação & Intervalos</span>
                <span style="font-size: 11px; color: #22c55e;">● Sincronizado</span>
            </div>
            <table>
                <thead>
                    <tr><th>Pos</th><th>Piloto</th><th>Equipe</th><th>Gap</th><th>Pneu</th></tr>
                </thead>
                <tbody id="standings-tbody">
                    <!-- Preenchido por JS -->
                </tbody>
            </table>

            <div style="margin-top: 14px;">
                <div class="card-title" style="margin-bottom: 6px; font-size: 12px;">⚡ Telemetria do Líder (Verstappen)</div>
                <div class="telemetry-grid">
                    <div class="tele-box">
                        <div class="tele-label">Velocidade</div>
                        <div class="tele-val" id="tele-speed">314 km/h</div>
                    </div>
                    <div class="tele-box">
                        <div class="tele-label">Marcha</div>
                        <div class="tele-val" id="tele-gear">7</div>
                    </div>
                    <div class="tele-box">
                        <div class="tele-label">RPM do Motor</div>
                        <div class="tele-val" id="tele-rpm">11,450</div>
                    </div>
                    <div class="tele-box">
                        <div class="tele-label">Acelerador</div>
                        <div class="tele-val" id="tele-throttle">100%</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 1. Cronômetro da Sessão em Tempo Real
        let secondsElapsed = 3640; 
        setInterval(() => {
            secondsElapsed++;
            let hrs = Math.floor(secondsElapsed / 3600).toString().padStart(2, '0');
            let mins = Math.floor((secondsElapsed % 3600) / 60).toString().padStart(2, '0');
            let secs = (secondsElapsed % 60).toString().padStart(2, '0');
            document.getElementById('live-timer').innerText = `${hrs}:${mins}:${secs}`;
        }, 1000);

        // 2. Dados dos Carros (Posições, Cores e Velocidades na Pista)
        const cars = [
            { id: 1, name: "M. Verstappen", code: "VER", team: "Red Bull", color: "#3671C6", progress: 0.18, speed: 0.0013, tire: "🟡 M", gap: "LEADER", pos: 1 },
            { id: 2, name: "L. Hamilton", code: "HAM", team: "Ferrari", color: "#E8002D", progress: 0.14, speed: 0.00125, tire: "🟡 M", gap: "+2.1s", pos: 2 },
            { id: 3, name: "C. Leclerc", code: "LEC", team: "Ferrari", color: "#E8002D", progress: 0.10, speed: 0.00122, tire: "🔴 H", gap: "+3.9s", pos: 3 },
            { id: 4, name: "L. Norris", code: "NOR", team: "McLaren", color: "#FF8000", progress: 0.07, speed: 0.00118, tire: "🟡 M", gap: "+7.4s", pos: 4 },
            { id: 5, name: "O. Piastri", code: "PIA", team: "McLaren", color: "#FF8000", progress: 0.04, speed: 0.00115, tire: "⚪ H", gap: "+10.8s", pos: 5 },
            { id: 6, name: "G. Russell", code: "RUS", team: "Mercedes", color: "#27F4D2", progress: 0.01, speed: 0.00110, tire: "🟡 M", gap: "+13.2s", pos: 6 }
        ];

        // Montar Legenda
        const legendContainer = document.getElementById('track-legend');
        cars.forEach(car => {
            legendContainer.innerHTML += `
                <div class="legend-item">
                    <div class="legend-color" style="background: ${car.color};"></div>
                    <span><b>${car.code}</b></span>
                </div>
            `;
        });

        // 3. Renderização do Movimento dos Pontos no Circuito SVG
        const trackPath = document.getElementById('race-track');
        const pathLength = trackPath.getTotalLength();
        const carsContainer = document.getElementById('cars-container');
        const carElements = {};

        cars.forEach(car => {
            const dot = document.createElement('div');
            dot.style.position = 'absolute';
            dot.style.width = '11px';
            dot.style.height = '11px';
            dot.style.backgroundColor = car.color;
            dot.style.borderRadius = '50%';
            dot.style.border = '2px solid #ffffff';
            dot.style.transform = 'translate(-50%, -50%)';
            dot.style.boxShadow = `0 0 8px ${car.color}`;
            dot.style.zIndex = '10';
            
            // Sigla do piloto flutuando ao lado do ponto
            const label = document.createElement('div');
            label.innerText = car.code;
            label.style.position = 'absolute';
            label.style.fontSize = '9px';
            label.style.color = '#fff';
            label.style.fontWeight = 'bold';
            label.style.transform = 'translate(10px, -10px)';
            label.style.textShadow = '1px 1px 2px #000';
            dot.appendChild(label);

            carsContainer.appendChild(dot);
            carElements[car.id] = dot;
        });

        // Loop de animação contínua dos pontos ao longo da linha da pista
        function animateTracks() {
            cars.forEach(car => {
                car.progress += car.speed;
                if (car.progress > 1) car.progress = 0; // Dá a volta completa

                // Pega a coordenada exata (X, Y) baseada no comprimento do traçado SVG
                const point = trackPath.getPointAtLength(car.progress * pathLength);
                
                const xPercent = (point.x / 500) * 100;
                const yPercent = (point.y / 300) * 100;

                const dot = carElements[car.id];
                dot.style.left = xPercent + '%';
                dot.style.top = yPercent + '%';
            });
            requestAnimationFrame(animateTracks);
        }
        requestAnimationFrame(animateTracks);

        // 4. Atualização dinâmica dos dados da tabela e telemetria (Efeito Tempo Real)
        setInterval(() => {
            // Oscilação realista de velocidade e RPM do líder
            let currentSpeed = Math.floor(312 + Math.random() * 10);
            let currentRpm = Math.floor(11400 + Math.random() * 250).toLocaleString();
            document.getElementById('tele-speed').innerText = currentSpeed + ' km/h';
            document.getElementById('tele-rpm').innerText = currentRpm;

            // Atualiza a tabela de posições em tempo real
            let tbody = document.getElementById('standings-tbody');
            let html = '';
            cars.forEach(car => {
                let posClass = car.pos === 1 ? 'pos-1' : (car.pos === 2 ? 'pos-2' : (car.pos === 3 ? 'pos-3' : ''));
                html += `
                    <tr>
                        <td class="${posClass}">${car.pos}</td>
                        <td><b>${car.name}</b></td>
                        <td>${car.team}</td>
                        <td style="color: #8b949e;">${car.gap}</td>
                        <td>${car.tire}</td>
                    </tr>
                `;
            });
            tbody.innerHTML = html;
        }, 1500);
    </script>
</body>
</html>
"""

# Renderizando no Streamlit sem barra lateral e ocupando a largura total
st.components.v1.html(f1_live_html, height=520, scrolling=True)
