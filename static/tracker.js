document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById('f1Canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    let trackPoints = [];
    let driverPositions = {};
    let driversInfo = {};
    let driverTires = {};

    async function fetchSessionMetadata() {
        const sKey = window.sessionKey;
        if (!sKey || sKey === "None") return;

        try {
            // 1. Busca dados dos pilotos (Nome, Equipe, Cor Oficial)
            const driversRes = await fetch(`https://api.openf1.org/v1/drivers?session_key=${sKey}`);
            const drivers = await driversRes.json();
            if (drivers && drivers.length > 0) {
                drivers.forEach(d => {
                    driversInfo[d.driver_number] = {
                        acronym: d.name_acronym,
                        team: d.team_name,
                        color: d.team_colour ? `#${d.team_colour}` : '#e10600'
                    };
                });
            }

            // 2. Busca compostos de pneus ativos (Stints)
            const stintsRes = await fetch(`https://api.openf1.org/v1/stints?session_key=${sKey}`);
            const stints = await stintsRes.json();
            if (stints && stints.length > 0) {
                // Pega o stint mais recente de cada piloto
                stints.forEach(s => {
                    driverTires[s.driver_number] = s.compound || 'UNKNOWN';
                });
            }

            // 3. Traçado da pista usando o primeiro piloto válido
            if (drivers.length > 0) {
                const sampleDriver = drivers[0].driver_number;
                const locRes = await fetch(`https://api.openf1.org/v1/location?session_key=${sKey}&driver_number=${sampleDriver}`);
                let locData = await locRes.json();
                
                if (locData && locData.length > 0) {
                    locData.sort((a, b) => new Date(a.date) - new Date(b.date));
                    trackPoints = locData.filter(p => p.x !== 0 && p.y !== 0);
                }
            }
        } catch (e) {
            console.error("Erro ao carregar metadados da sessão:", e);
        }
    }

    async function fetchLivePositions() {
        const sKey = window.sessionKey;
        if (!sKey || sKey === "None") return;

        try {
            const res = await fetch(`https://api.openf1.org/v1/position?session_key=${sKey}&per_page=100`);
            const data = await res.json();
            if (data && data.length > 0) {
                data.forEach(p => {
                    driverPositions[p.driver_number] = { x: p.x, y: p.y };
                });
            }
        } catch (e) {
            console.error("Erro ao buscar posições:", e);
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

        ctx.fillStyle = '#8a99ad';
        ctx.font = '11px sans-serif';
        ctx.fillText(`EA TELEMETRY HUB | SESSION: ${window.sessionKey || 'N/A'}`, 15, 25);

        if (trackPoints.length === 0) {
            ctx.fillStyle = '#ffffff';
            ctx.font = '14px sans-serif';
            ctx.fillText('Sincronizando telemetria do circuito...', 15, 55);
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

            // Linha da Pista com efeito Neon Suave
            ctx.shadowBlur = 10;
            ctx.shadowColor = '#1e3a8a';
            ctx.strokeStyle = '#2563eb';
            ctx.lineWidth = 4;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            ctx.beginPath();
            trackPoints.forEach((p, index) => {
                let px = p.x * scale + offsetX;
                let py = p.y * scale + offsetY;
                if (index === 0) ctx.moveTo(px, py);
                else ctx.lineTo(px, py);
            });
            ctx.stroke();
            ctx.shadowBlur = 0; // Reseta o shadow para os carros

            // Renderiza os Carros em Tempo Real com as Cores das Equipes
            for (let driver in driverPositions) {
                let pos = driverPositions[driver];
                let cx = pos.x * scale + offsetX;
                let cy = pos.y * scale + offsetY;
                let info = driversInfo[driver] || { acronym: `#${driver}`, color: '#e10600' };

                // Ponto do Carro (Círculo colorido com a cor da equipe)
                ctx.fillStyle = info.color;
                ctx.beginPath();
                ctx.arc(cx, cy, 6, 0, Math.PI * 2);
                ctx.fill();

                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.5;
                ctx.stroke();

                // Rótulo da Sigla do Piloto (Ex: VER, HAM, LEC)
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 10px sans-serif';
                ctx.fillText(info.acronym, cx + 9, cy + 4);
            }
        }

        requestAnimationFrame(render);
    }

    if (window.sessionKey && window.sessionKey !== "None") {
        fetchSessionMetadata();
        fetchLivePositions();
        setInterval(fetchLivePositions, 2000);
    }

    render();
});
