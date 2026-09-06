document.addEventListener("DOMContentLoaded", () => {
    runTracker();
});

setTimeout(runTracker, 400);

function runTracker() {
    const canvas = document.getElementById('f1Canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
        canvas.width = canvas.parentElement.clientWidth || 600;
        canvas.height = canvas.parentElement.clientHeight || 520;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    let trackPoints = [];
    let driverPositions = {};
    let driversInfo = {};

    const sKey = window.sessionKey;
    if (!sKey || sKey === "None") return;

    async function fetchMetadata() {
        try {
            const dRes = await fetch(`https://api.openf1.org/v1/drivers?session_key=${sKey}`);
            const drivers = await dRes.json();
            if (drivers && drivers.length > 0) {
                drivers.forEach(d => {
                    driversInfo[d.driver_number] = {
                        acronym: d.name_acronym || d.driver_number,
                        color: d.team_colour ? `#${d.team_colour}` : '#e10600'
                    };
                });
                
                // Pega o traçado usando o primeiro piloto válido
                const sample = drivers[0].driver_number;
                const lRes = await fetch(`https://api.openf1.org/v1/location?session_key=${sKey}&driver_number=${sample}`);
                const locs = await lRes.json();
                if (locs && locs.length > 0) {
                    locs.sort((a, b) => new Date(a.date) - new Date(b.date));
                    trackPoints = locs.filter(p => p.x !== 0 && p.y !== 0);
                }
            }
        } catch (err) {
            console.error("Erro ao carregar metadados do circuito:", err);
        }
    }

    async function fetchPositions() {
        try {
            const res = await fetch(`https://api.openf1.org/v1/location?session_key=${sKey}`);
            const data = await res.json();
            if (data && data.length > 0) {
                const latest = {};
                data.forEach(p => {
                    if (!latest[p.driver_number] || new Date(p.date) > new Date(latest[p.driver_number].date)) {
                        latest[p.driver_number] = { x: p.x, y: p.y };
                    }
                });
                driverPositions = latest;
            }
        } catch (err) {
            console.error("Erro ao buscar posições ao vivo:", err);
        }
    }

    function render() {
        ctx.fillStyle = '#0b0e14';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Grid de fundo estilo radar de simulação
        ctx.strokeStyle = '#151d2a';
        ctx.lineWidth = 1;
        const gridSize = 40;
        for (let x = 0; x < canvas.width; x += gridSize) {
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
        }
        for (let y = 0; y < canvas.height; y += gridSize) {
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
        }

        if (trackPoints.length === 0) {
            ctx.fillStyle = '#ffffff';
            ctx.font = '13px sans-serif';
            ctx.fillText('Sincronizando telemetria do circuito...', 20, 40);
        } else {
            let minX = Math.min(...trackPoints.map(p => p.x));
            let maxX = Math.max(...trackPoints.map(p => p.x));
            let minY = Math.min(...trackPoints.map(p => p.y));
            let maxY = Math.max(...trackPoints.map(p => p.y));

            let scaleX = (canvas.width - 80) / (maxX - minX || 1);
            let scaleY = (canvas.height - 80) / (maxY - minY || 1);
            let scale = Math.min(scaleX, scaleY);

            let offsetX = 40 - minX * scale + (canvas.width - 80 - (maxX - minX) * scale) / 2;
            let offsetY = 40 - minY * scale + (canvas.height - 80 - (maxY - minY) * scale) / 2;

            // Linha da Pista com efeito Neon
            ctx.shadowBlur = 8;
            ctx.shadowColor = '#1e3a8a';
            ctx.strokeStyle = '#2563eb';
            ctx.lineWidth = 4;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            ctx.beginPath();
            trackPoints.forEach((p, idx) => {
                let px = p.x * scale + offsetX;
                let py = p.y * scale + offsetY;
                if (idx === 0) ctx.moveTo(px, py);
                else ctx.lineTo(px, py);
            });
            ctx.stroke();
            ctx.shadowBlur = 0;

            // Renderiza os Carros em Tempo Real com as Cores das Equipes e Siglas
            for (let num in driverPositions) {
                let pos = driverPositions[num];
                let cx = pos.x * scale + offsetX;
                let cy = pos.y * scale + offsetY;
                let info = driversInfo[num] || { acronym: `#${num}`, color: '#e10600' };

                ctx.fillStyle = info.color;
                ctx.beginPath();
                ctx.arc(cx, cy, 6, 0, Math.PI * 2);
                ctx.fill();

                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.5;
                ctx.stroke();

                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 10px sans-serif';
                ctx.fillText(info.acronym, cx + 9, cy + 4);
            }
        }

        requestAnimationFrame(render);
    }

    fetchMetadata();
    fetchPositions();
    setInterval(fetchPositions, 2000);
    render();
}
