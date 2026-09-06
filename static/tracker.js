let canvas, ctx;
let trackPoints = [];
let driverPositions = {};
let driverColors = {};
let driverAcronyms = {};

async function initTracker() {
    canvas = document.getElementById('trackCanvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');
    
    // Ajustar tamanho do canvas
    canvas.width = canvas.parentElement.clientWidth || 800;
    canvas.height = 500;

    await loadTrackAndDrivers();
    
    // Loop de atualização em tempo real (a cada 1 segundo)
    setInterval(updateLiveTelemetry, 1000);
    requestAnimationFrame(renderLoop);
}

async function loadTrackAndDrivers() {
    const sKey = window.sessionKey || 'latest';
    try {
        // 1. Carregar pilotos e cores das equipes
        const driversRes = await fetch(`https://api.openf1.org/v1/drivers?session_key=${sKey}`);
        const drivers = await driversRes.json();
        drivers.forEach(d => {
            driverColors[d.driver_number] = `#${d.team_colour || 'FFFFFF'}`;
            driverAcronyms[d.driver_number] = d.name_acronym || d.driver_number;
        });

        // 2. Carregar o traçado da pista (usando o piloto 1 ou o primeiro disponível como referência de geometria)
        const sampleDriver = drivers.length > 0 ? drivers[0].driver_number : 1;
        const locRes = await fetch(`https://api.openf1.org/v1/location?session_key=${sKey}&driver_number=${sampleDriver}`);
        const locData = await locRes.json();
        
        if (locData && locData.length > 0) {
            trackPoints = locData.map(pt => ({ x: pt.x, y: pt.y }));
        }
    } catch (e) {
        console.error("Erro ao carregar dados da pista:", e);
    }
}

async function updateLiveTelemetry() {
    const sKey = window.sessionKey || 'latest';
    try {
        // Buscar as localizações mais recentes de todos os carros
        const res = await fetch(`https://api.openf1.org/v1/location?session_key=${sKey}`);
        const data = await res.json();
        
        if (data && data.length > 0) {
            // Filtrar apenas a última coordenada de cada piloto
            const latest = {};
            data.forEach(item => {
                if (!latest[item.driver_number] || new Date(item.date) > new Date(latest[item.driver_number].date)) {
                    latest[item.driver_number] = item;
                }
            });
            driverPositions = latest;
        }
    } catch (e) {
        console.error("Erro ao atualizar posições:", e);
    }
}

function renderLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Fundo escuro padrão F1 Telemetry
    ctx.fillStyle = "#121214";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (trackPoints.length > 0) {
        // Normalizar coordenadas da pista para o tamanho do Canvas
        let minX = Math.min(...trackPoints.map(p => p.x));
        let maxX = Math.max(...trackPoints.map(p => p.x));
        let minY = Math.min(...trackPoints.map(p => p.y));
        let maxY = Math.max(...trackPoints.map(p => p.y));

        let scaleX = (canvas.width - 80) / (maxX - minX || 1);
        let scaleY = (canvas.height - 80) / (maxY - minY || 1);
        let scale = Math.min(scaleX, scaleY);

        let offsetX = 40 - minX * scale + (canvas.width - 80 - (maxX - minX) * scale) / 2;
        let offsetY = 40 - minY * scale + (canvas.height - 80 - (maxY - minY) * scale) / 2;

        // Desenhar a linha do circuito
        ctx.strokeStyle = "#2e2e38";
        ctx.lineWidth = 4;
        ctx.beginPath();
        trackPoints.forEach((pt, index) => {
            let px = pt.x * scale + offsetX;
            let py = canvas.height - (pt.y * scale + offsetY); // Inverter Y do canvas
            if (index === 0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        });
        ctx.stroke();

        // Desenhar os pontos dos carros em tempo real
        for (let num in driverPositions) {
            let pos = driverPositions[num];
            let cx = pos.x * scale + offsetX;
            let cy = canvas.height - (pos.y * scale + offsetY);

            let color = driverColors[num] || "#ff1801";
            let acronym = driverAcronyms[num] || num;

            // Círculo do carro
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(cx, cy, 6, 0, 2 * Math.PI);
            ctx.fill();
            ctx.lineWidth = 2;
            ctx.strokeStyle = "#ffffff";
            ctx.stroke();

            // Sigla do piloto ao lado do ponto
            ctx.fillStyle = "#ffffff";
            ctx.font = "10px sans-serif";
            ctx.fillText(acronym, cx + 10, cy + 3);
        }
    }

    requestAnimationFrame(renderLoop);
}

window.onload = initTracker;
