import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import datetime

# Configuração de Página Ultra-Wide e responsiva
st.set_page_config(page_title="F1 Ultra-Low Latency Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: #FF1801; margin-bottom: 5px;'>🏎️ F1 REAL-TIME TELEMETRY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; margin-top: 0px;'>Suporte a Dados Históricos e Ao Vivo com Nome de Pilotos</p>", unsafe_allow_html=True)

# --- CONFIGURAÇÃO AUTOMÁTICA DE SESSÕES VIA PYTHON ---
@st.cache_data(ttl=60)
def buscar_sessoes_ativas():
    try:
        url = "https://openf1.org"
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            agora = datetime.utcnow()
            opcoes = {}
            for s in dados[::-1]:
                data_inicio_str = s.get('date_start')
                if not data_inicio_str: continue
                try:
                    data_limpa = data_inicio_str.split('+')[0].rstrip('Z')
                    data_inicio = datetime.strptime(data_limpa, "%Y-%m-%dT%H:%M:%S")
                except ValueError: continue
                
                if data_inicio <= agora:
                    nome_formatado = f"📍 {s.get('location', 'Desconhecido')} ({s.get('year')}) - {s.get('session_name')}"
                    if nome_formatado not in opcoes and len(opcoes) < 30:
                        opcoes[nome_formatado] = str(s.get('session_key'))
            if opcoes: return opcoes
    except Exception: pass
    return {"GP de Mônaco (2024) - Race": "9523"}

dicionario_sessoes = buscar_sessoes_ativas()
sessao_selecionada = st.selectbox("🏁 Selecione o Grande Prêmio:", list(dicionario_sessoes.keys()))
session_key_final = dicionario_sessoes[sessao_selecionada]

st.caption(f"ID da Sessão ativa enviado ao Motor JS: `{session_key_final}`")
st.markdown("---")

# --- BLOCCO JAVASCRIPT INJETADO (Mínima Latência e Leitura Completa) ---
js_telemetry_engine = f"""
<div style="background-color: #1a1a1a; padding: 20px; border-radius: 10px; font-family: monospace; color: white; border: 1px solid #333;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px;">
        <div style="background: #262626; padding: 15px; border-radius: 8px; border-left: 5px solid #FF1801;">
            <h3 style="margin: 0 0 10px 0; color: #FF1801;">STATUS DA PISTA</h3>
            <div id="track-status" style="font-size: 24px; font-weight: bold;">Carregando dados estáveis...</div>
        </div>
        <div style="background: #262626; padding: 15px; border-radius: 8px; border-left: 5px solid #00D2C4;">
            <h3 style="margin: 0 0 10px 0; color: #00D2C4;">MAIOR VELOCIDADE EM PISTA</h3>
            <div id="top-speed" style="font-size: 28px; font-weight: bold;">-- <span style="font-size: 14px; color: #888;">km/h</span></div>
            <div id="top-driver" style="font-size: 14px; color: #aaa;">Processando pacotes...</div>
        </div>
    </div>

    <h3 style="color: #FF1801; border-bottom: 1px solid #333; padding-bottom: 5px;">LIVE GRID INTERVALS</h3>
    <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 15px;">
        <thead>
            <tr style="color: #888; border-bottom: 2px solid #333;">
                <th style="padding: 10px 5px;">POS</th>
                <th>PILOTO</th>
                <th>GAP P/ LÍDER</th>
                <th>INTERVALO</th>
            </tr>
        </thead>
        <tbody id="grid-table-body">
            <tr><td colspan="4" style="padding: 20px; text-align: center; color: #666;">Buscando base de dados da F1...</td></tr>
        </tbody>
    </table>
</div>

<script>
const SESSION_KEY = "{session_key_final}";

// Dicionário de tradução dos números dos pilotos para facilitar a leitura no tablet
const driversMap = {{
    "1": "VER (Red Bull)", "11": "PER (Red Bull)", "16": "LEC (Ferrari)", "55": "SAI (Ferrari)",
    "44": "HAM (Mercedes)", "63": "RUS (Mercedes)", "4": "NOR (McLaren)", "81": "PIA (McLaren)",
    "14": "ALO (Aston Martin)", "18": "STR (Aston Martin)", "10": "GAS (Alpine)", "31": "OCO (Alpine)",
    "23": "ALB (Williams)", "2": "SAR (Williams)", "3": "RIC (RB)", "22": "TSU (RB)",
    "77": "BOT (Sauber)", "24": "ZHU (Sauber)", "20": "MAG (Haas)", "27": "HUL (Haas)"
}};

async function updateTelemetry() {{
    try {{
        // 1. Status da Pista (Pega o último status gerado na corrida)
        const trackRes = await fetch(`https://openf1.org{{SESSION_KEY}}`);
        const trackData = await trackRes.json();
        if(trackData && trackData.length > 0) {{
            const latestStatus = trackData[trackData.length - 1];
            const statusDiv = document.getElementById('track-status');
            statusDiv.innerText = latestStatus.flag || "PISTA LIMPA";
            if(latestStatus.flag === "RED") statusDiv.style.color = "#FF1801";
            else if(latestStatus.flag === "YELLOW") statusDiv.style.color = "#FFCC00";
            else if(latestStatus.flag === "GREEN") statusDiv.style.color = "#00FF00";
            else statusDiv.style.color = "#FFFFFF";
        }} else {{
            document.getElementById('track-status').innerText = "FINALIZADA / LIMPA";
        }}

        // 2. Velocidade Máxima Gravada (Removemos o filtro dinâmico de tempo para buscar o recorde geral da sessão)
        const carRes = await fetch(`https://openf1.org{{SESSION_KEY}}&speed>280`);
        const carData = await carRes.json();
        if(carData && carData.length > 0) {{
            let maxSpeed = 0;
            let fastDriverNum = "";
            // Analisa uma amostragem grande para achar o ponto mais rápido
            const sample = carData.length > 300 ? carData.slice(-300) : carData;
            sample.forEach(d => {{
                if(d.speed > maxSpeed) {{
                    maxSpeed = d.speed;
                    fastDriverNum = String(d.driver_number);
                }}
            }});
            if(maxSpeed > 0) {{
                const driverName = driversMap[fastDriverNum] || `Piloto #${{fastDriverNum}}`;
                document.getElementById('top-speed').innerHTML = `${{maxSpeed}} <span style="font-size: 14px; color: #888;">km/h</span>`;
                document.getElementById('top-driver').innerText = "Registrado por: " + driverName;
            }}
        }}

        // 3. Tabela de Posições e Gaps Completos
        const intervalRes = await fetch(`https://openf1.org{{SESSION_KEY}}`);
        const intervalData = await intervalRes.json();
        if(intervalData && intervalData.length > 0) {{
            const uniqueDrivers = {{}};
            // Processa todas as entradas para montar o grid final consolidado da corrida
            intervalData.forEach(item => {{
                uniqueDrivers[item.driver_number] = item;
            }});

            const sortedGrid = Object.values(uniqueDrivers).sort((a, b) => {{
                return (parseFloat(a.gap_to_leader) || 0) - (parseFloat(b.gap_to_leader) || 0);
            }});

            let tbodyHtml = "";
            sortedGrid.forEach((row, index) => {{
                const driverNumStr = String(row.driver_number);
                const driverLabel = driversMap[driverNumStr] || `Piloto #${{driverNumStr}}`;
                
                let gapText = row.gap_to_leader === null || row.gap_to_leader === undefined ? "LÍDER" : `+${{row.gap_to_leader}}s`;
                if(index === 0) gapText = "LÍDER";

                tbodyHtml += `
                    <tr style="border-bottom: 1px solid #222; font-size: 14px;">
                        <td style="padding: 10px 5px; font-weight: bold; color: #FF1801;">${{index + 1}}</td>
                        <td style="font-weight: bold; color: #fff;">${{driverLabel}}</td>
                        <td style="color: #00D2C4;">${{gapText}}</td>
                        <td style="color: #ccc;">+${{row.interval || '0.000'}}s</td>
                    </tr>
                `;
            }});
            document.getElementById('grid-table-body').innerHTML = tbodyHtml;
        }} else {{
            document.getElementById('grid-table-body').innerHTML = '<tr><td colspan="4" style="padding: 20px; text-align: center; color: #888;">Sem telemetria de grid salva para este ID. Traga um GP recente de 2024!</td></tr>';
        }}

    }} catch (error) {{
        console.error("Erro no motor JavaScript:", error);
    }}
}}

// Mantém o ciclo ativo
setInterval(updateTelemetry, 3000);
updateTelemetry();
</script>
"""

components.html(js_telemetry_engine, height=650, scrolling=True)
st.caption("⚡ Sistema híbrido ativado. Pronto para a próxima corrida ao vivo do final de semana.")
