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
            // Primeiro descobre um piloto ativo na sessão para traçar o circuito base
            const driversRes = await fetch(`https://api.openf1.org/v1/drivers?session_key=${sKey}`);
            const drivers = await driversRes.json();
            if (!drivers || drivers.length === 0) return;
            
            const sampleDriver = drivers[0].driver_number;

            // Busca a localização apenas desse piloto para desenhar o circuito limpo
            const res = await fetch(`https://api.openf1.org/v1/location?session_key=${sKey}&driver_number=${sampleDriver}`);
            const data = await res.json();
            if (data && data.length > 0) {
                // Ordena cronologicamente para formar o traçado correto da pista
                data.sort((a, b) => new Date(a.date) - new Date(b.date));
                
                // Amostragem para manter leve
                const step = Math.max(1, Math.floor(data.length / 1500));
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

        ctx.fillStyle = '#4a5568';
        ctx.font = '12px sans-serif';
        ctx.fillText(`Session Key: ${window.sessionKey || 'N/A'}`, 15, 25);

        if (trackPoints.length === 0) {
            ctx.fillStyle = '#a0aec0';
            ctx.font = '14px sans-serif';
            ctx.fillText('Carregando traçado do circuito...', 15, 50);
        } else {
            let minX = Math.min(...trackPoints.map(p => p.x));
            let maxX = Math.max(...trackPoints.map(p => p.x));
            let minY = Math.min(...trackPoints.map(p => p.y));
            let maxY = Math.max(...trackPoints.map(p => p.y));

            let scaleX = (canvas.width - 60) / (maxX - minX || 1);
            let scaleY = (canvas.height - 60) / (maxY - minY || 1);
            let scale = Math.min(scaleX, scaleY);

            let offsetX = 30 - minX * scale + (canvas.width - 60 - (maxX - minX) * scale) / 2;
            let offsetY = 30 - minY * scale + (canvas.height - 60 - (maxY - minY) * scale) / 2;

            // Desenha a linha fina e limpa do circuito
            ctx.strokeStyle = '#3182ce';
            ctx.lineWidth = 3;
            ctx.lineCap = 'round';
            ctx.beginPath();
            trackPoints.forEach((p, index) => {
                let px = p.x * scale + offsetX;
                let py = p.y * scale + offsetY;
                if (index === 0) ctx.moveTo(px, py);
                else ctx.lineTo(px, py);
            });
            ctx.stroke();

            // Desenha os pontos dos carros em tempo real
            for (let driver in driverPositions) {
                let pos = driverPositions[driver];
                let cx = pos.x * scale + offsetX;
                let cy = pos.y * scale + offsetY;

                ctx.fillStyle = '#e10600';
                ctx.beginPath();
                ctx.arc(cx, cy, 5, 0, Math.PI * 2);
                ctx.fill();

                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1;
                ctx.stroke();

                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 10px sans-serif';
                ctx.fillText(`#${driver}`, cx + 8, cy + 4);
            }
        }

        requestAnimationFrame(render);
    }

    if (window.sessionKey && window.sessionKey !== "None") {
        fetchTrackData();
        fetchLivePositions();
        setInterval(fetchLivePositions, 2000);
    }

    render();
});
