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

    async function fetchTrackData() {
        if (!window.sessionKey || window.sessionKey === "None") return;
        try {
            // Busca coordenadas de localização da API OpenF1 para desenhar o traçado e os carros
            const res = await fetch(`https://api.openf1.org/v1/location?session_key=${window.sessionKey}`);
            const data = await res.json();
            if (data && data.length > 0) {
                trackPoints = data;
            }
        } catch (e) {
            console.error("Erro ao buscar telemetria:", e);
        }
    }

    function render() {
        ctx.fillStyle = '#151820';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Desenha indicador de status no canvas
        ctx.fillStyle = '#4a5568';
        ctx.font = '12px sans-serif';
        ctx.fillText(`Session Key: ${window.sessionKey || 'N/A'}`, 15, 25);

        if (trackPoints.length === 0) {
            ctx.fillStyle = '#a0aec0';
            ctx.font = '14px sans-serif';
            ctx.fillText('Carregando traçado do circuito e telemetria...', 15, 50);
        }

        requestAnimationFrame(render);
    }

    if (window.sessionKey && window.sessionKey !== "None") {
        fetchTrackData();
        setInterval(fetchTrackData, 5000); // Atualiza dados a cada 5 segundos de forma limpa
    }

    render();
});
