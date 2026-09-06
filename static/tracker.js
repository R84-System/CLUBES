function initTracker() {
    const canvas = document.getElementById('f1Canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    // Ajusta tamanho real do canvas
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;

    function draw() {
        // Limpa tela
        ctx.fillStyle = '#151820';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Desenha pista placeholder (exemplo visual)
        ctx.strokeStyle = '#2d3748';
        ctx.lineWidth = 40;
        ctx.beginPath();
        ctx.arc(canvas.width / 2, canvas.height / 2, 150, 0, Math.PI * 2);
        ctx.stroke();

        // Texto indicativo
        ctx.fillStyle = '#a0aec0';
        ctx.font = '14px sans-serif';
        ctx.fillText('Aguardando dados da API OpenF1...', 20, 30);
    }

    draw();
}

window.addEventListener('load', initTracker);
