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
        if (!sKey || sKey === "None" || sKey === "None") return;
        
        try {
            // Pega amostra de localizações para traçar o circuito da sessão
            const res = await fetch(`https://api.openf1.org/v1/location?session_key=${sKey}`);
            const data = await res.json();
            if (data && data.length > 0) {
                // Filtra para pegar um mapeamento leve do circuito
                trackPoints = data.slice(-1500); 
            }
        } catch (e) {
            console.error("Erro ao buscar traçado:", e);
        }
    }

    async function fetchLivePositions() {
        const sKey = window.sessionKey;
        if (!sKey || sKey === "None") return;

        try {
            const res = await fetch(`https://api.openf1.org/v1/position?session_key=${sKey}&per_page=50`);
            const data = await res.json();
            if (data && data.length > 0) {
                // Pega a última posição registrada de cada piloto
                data.forEach(p => {
                    driverPositions[p.driver_number] = { x: p.x, y: p.y, date: p.date };
                });
            }
        } catch (e) {
            console.error("Erro ao buscar posições dos carros:", e);
        }
    }

    function render() {
        ctx.fillStyle = '#151820';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Status na tela
        ctx.fillStyle = '#4a5568';
        ctx.font = '12px sans-serif';
        ctx.fillText(`Session Key: ${window.sessionKey || 'N/A'}`, 15, 25);

        if (trackPoints.length === 0) {
            ctx.fillStyle = '#a0aec0';
            ctx.font = '14px sans-serif';
            ctx.fillText('Carregando telemetria do circuito...', 15, 50);
        } else {
            // Normaliza as coordenadas da API para caber no Canvas de forma fluida
            let minX = Math.min(...trackPoints.map(p => p.x));
            let maxX = Math.max(...trackPoints.map(p => p.x));
            let minY = Math.min(...trackPoints.map(p => p.y));
            let maxY = Math.max(...trackPoints.map(p => p.y));

            let scaleX = (canvas.width - 80) / (maxX - minX || 1);
            let scaleY = (canvas.height - 80) / (maxY - minY || 1);
            let scale = Math.min(scaleX, scaleY);

            let offsetX = 40 - minX * scale + (canvas.width - 80 - (maxX - minX) * scale) / 2;
            let offsetY = 40 - minY * scale + (canvas.height - 80 - (maxY - minY) * scale) / 2;

            // Desenha linha do circuito
            ctx.strokeStyle = '#2d3748';
            ctx.lineWidth = 6;
            ctx.beginPath();
            trackPoints.forEach((p, index) => {
                let px = p.x * scale + offsetX;
                let py = p.y * scale + offsetY;
                if (index === 0) ctx.moveTo(px, py);
                else ctx.lineTo(px, py);
            });
            ctx.stroke();

            // Desenha os pontinhos dos carros em tempo real
            for (let driver in driverPositions) {
                let pos = driverPositions[driver];
                let cx = pos.x * scale + offsetX;
                let cy = pos.y * scale + offsetY;

                ctx.fillStyle = '#e10600'; // Vermelho F1
                ctx.beginPath();
                ctx.arc(cx, cy, 5, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = '#ffffff';
                ctx.font = '10px sans-serif';
                ctx.fillText(`#${driver}`, cx + 8, cy + 4);
            }
        }

        requestAnimationFrame(render);
    }

    if (window.sessionKey && window.sessionKey !== "None") {
        fetchTrackData();
        fetchLivePositions();
        setInterval(fetchLivePositions, 3000); // Atualiza posições dos carros a cada 3 segundos liso
    }

    render();
});
