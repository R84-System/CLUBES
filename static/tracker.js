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

    async function fetchTrackData() {
        const sKey = window.sessionKey;
        if (!sKey || sKey === "None") return;
        
        try {
            // Busca dados de localização para mapear o circuito completo
            const res = await fetch(`https://api.openf1.org/v1/location?session_key=${sKey}`);
            const data = await res.json();
            if (data && data.length > 0) {
                // Pega uma amostra espaçada para desenhar todo o traçado da pista sem travar o navegador
                const step = Math.max(1, Math.floor(data.length / 3000));
                trackPoints = [];
                for (let i = 0; i < data.length; i += step) {
                    trackPoints.push(data[i]);
                }
            }
        } catch (e) {
            console.error("Erro ao buscar traçado:", e);
        }
    }

    async function fetchLivePositions() {
        const sKey = window.sessionKey;
        if (!sKey || sKey === "None") return;

        try {
            const res = await fetch(`https://api.openf1.org/v1/position?session_key=${sKey}&per_page=100`);
            const data = await res.json();
            if (data && data.length > 0) {
                // Agrupa a última posição conhecida de cada número de carro
                data.forEach(p => {
                    driverPositions[p.driver_number] = { x: p.x, y: p.y };
                });
            }
        } catch (e) {
            console.error("Erro ao buscar posições dos carros:", e);
        }
    }

    function render() {
        ctx.fillStyle = '#151820';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Status no canto do mapa
        ctx.fillStyle = '#4a5568';
        ctx.font = '12px sans-serif';
        ctx.fillText(`Session Key: ${window.sessionKey || 'N/A'}`, 15, 25);

        if (trackPoints.length === 0) {
            ctx.fillStyle = '#a0aec0';
            ctx.font = '14px sans-serif';
            ctx.fillText('Carregando traçado completo do circuito...', 15, 50);
        } else {
            // Encontra os limites (Min/Max) para centralizar e ajustar a escala perfeitamente no Canvas
            let minX = Math.min(...trackPoints.map(p => p.x));
            let maxX = Math.max(...trackPoints.map(p => p.x));
            let minY = Math.min(...trackPoints.map(p => p.y));
            let maxY = Math.max(...trackPoints.map(p => p.y));

            let scaleX = (canvas.width - 60) / (maxX - minX || 1);
            let scaleY = (canvas.height - 60) / (maxY - minY || 1);
            let scale = Math.min(scaleX, scaleY);

            let offsetX = 30 - minX * scale + (canvas.width - 60 - (maxX - minX) * scale) / 2;
            let offsetY = 30 - minY * scale + (canvas.height - 60 - (maxY - minY) * scale) / 2;

            // Desenha a linha do circuito
            ctx.strokeStyle = '#2d3748';
            ctx.lineWidth = 5;
            ctx.lineCap = 'round';
            ctx.beginPath();
            trackPoints.forEach((p, index) => {
                let px = p.x * scale + offsetX;
                let py = p.y * scale + offsetY;
                if (index === 0) ctx.moveTo(px, py);
                else ctx.lineTo(px, py);
            });
            ctx.stroke();

            // Desenha os pontos dos carros em tempo real sobre a pista
            for (let driver in driverPositions) {
                let pos = driverPositions[driver];
                let cx = pos.x * scale + offsetX;
                let cy = pos.y * scale + offsetY;

                // Ponto do carro
                ctx.fillStyle = '#e10600';
                ctx.beginPath();
                ctx.arc(cx, cy, 6, 0, Math.PI * 2);
                ctx.fill();

                // Borda branca para destaque
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.5;
                ctx.stroke();

                // Número do piloto
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 11px sans-serif';
                ctx.fillText(`#${driver}`, cx + 10, cy + 4);
            }
        }

        requestAnimationFrame(render);
    }

    if (window.sessionKey && window.sessionKey !== "None") {
        fetchTrackData();
        fetchLivePositions();
        setInterval(fetchLivePositions, 2000); // Atualiza posições dos carros de forma fluida
    }

    render();
});
