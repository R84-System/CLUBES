import streamlit as st
import streamlit.components.v1 as components

# Configuração de Página Ultra-Wide e responsiva
st.set_page_config(page_title="F1 Ultra-Low Latency Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: #FF1801; margin-bottom: 5px;'>🏎️ F1 REAL-TIME TELEMETRY</h1>", unsafe_allow_html=True)

# Barra de seleção para mudar a corrida em tempo real pelo Tablet
st.markdown("---")
session_input = st.text_input("📋 Digite o código da sessão (Session Key) ativa da F1:", "9149")
st.markdown("---")

# --- BLOCCO JAVASCRIPT INJETADO (Mínima Latência) ---
js_telemetry_engine = f"""
<div style="background-color: #1a1a1a; padding: 20px; border-radius: 10px; font-family: monospace; color: white; border: 1px solid #333;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px;">
        <div style="background: #262626; padding: 15px; border-radius: 8px; border-left: 5px solid #FF1801;">
            <h3 style="margin: 0 0 10px 0; color: #FF1801;">STATUS DA PISTA</h3>
            <div id="track-status" style="font-size: 24px; font-weight: bold; animation: pulse 2s infinite;">Buscando dados da sessão...</div>
        </div>
        <div style="background: #262626; padding: 15px; border-radius: 8px; border-left: 5px solid #00D2C4;">
            <h3 style="margin: 0 0 10px 0; color: #00D2C4;">MAIOR VELOCIDADE EM PISTA</h3>
            <div id="top-speed" style="font-size: 28px; font-weight: bold;">-- <span style="font-size: 14px; color: #888;">km/h</span></div>
            <div id="top-driver" style="font-size: 14px; color: #aaa;">Aguardando pacotes...</div>
        </div>
    </div>

    <h3 style="color: #FF1801; border-bottom: 1px solid #333; padding-bottom: 5px;">LIVE GRID INTERVALS (Atualizado a cada 2s)</h3>
    <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 15px;">
        <thead>
            <tr style="color: #888; border-bottom: 2px solid #333;">
                <th style="padding: 10px 5px;">POS</th>
                <th>PILOTO (#)</th>
                <th>GAP P/ LÍDER</th>
                <th>INTERVALO</th>
            </tr>
        </thead>
        <tbody id="grid-table-body">
            <tr><td colspan="4" style="padding: 20px; text-align: center; color: #666;">Conectando com o servidor de cronometragem da F1...</td></tr>
        </tbody>
    </table>
</div>

<script>
const SESSION_KEY = "{session_input}";

async function updateTelemetry() {{
    try {{
        // 1. Status da pista
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
            document.getElementById('track-status').innerText = "SEM DADOS ATIVOS";
        }}

        // 2. Velocidade máxima (ajustado limite para buscar dados mesmo em treinos lentos)
        const carRes = await fetch(`https://openf1.org{{SESSION_KEY}}&speed>250`);
        const carData = await carRes.json();
        if(carData && carData.length > 0) {{
            let maxSpeed = 0;
            let fastDriver = "";
            carData.slice(-100).forEach(d => {{
                if(d.speed > maxSpeed) {{
                    maxSpeed = d.speed;
                    fastDriver = "Carro Número: #" + d.driver_number;
                }}
            }});
            if(maxSpeed > 0) {{
                document.getElementById('top-speed').innerHTML = `${{maxSpeed}} <span style="font-size: 14px; color: #888;">km/h</span>`;
                document.getElementById('top-driver').innerText = fastDriver;
            }}
        }}

        // 3. Intervalos de grid
        const intervalRes = await fetch(`https://openf1.org{{SESSION_KEY}}`);
        const intervalData = await intervalRes.json();
        if(intervalData && intervalData.length > 0) {{
            const uniqueDrivers = {{}};
            intervalData.forEach(item => {{
                uniqueDrivers[item.driver_number] = item;
            }});

            const sortedGrid = Object.values(uniqueDrivers).sort((a, b) => {{
                return (parseFloat(a.gap_to_leader) || 0) - (parseFloat(b.gap_to_leader) || 0);
            }});

            let tbodyHtml = "";
            sortedGrid.slice(0, 10).forEach((row, index) => {{
                tbodyHtml += `
                    <tr style="border-bottom: 1px solid #222;">
                        <td style="padding: 12px 5px; font-weight: bold; color: #FF1801;">${{index + 1}}</td>
                        <td style="font-weight: bold;">Piloto #${{row.driver_number}}</td>
                        <td style="color: #00D2C4;">+${{row.gap_to_leader || '0.000'}}s</td>
                        <td>+${{row.interval || '0.000'}}s</td>
                    </tr>
                `;
            }});
            document.getElementById('grid-table-body').innerHTML = tbodyHtml;
        }} else {{
            document.getElementById('grid-table-body').innerHTML = '<tr><td colspan="4" style="padding: 20px; text-align: center; color: #888;">Nenhum carro na pista para esta sessão ainda.</td></tr>';
        }}

    }} catch (error) {{
        console.error("Erro na busca OpenF1:", error);
    }}
}}

setInterval(updateTelemetry, 2000);
updateTelemetry();
</script>

<style>
@keyframes pulse {{
    0% {{ opacity: 0.8; }}
    50% {{ opacity: 1; }}
    100% {{ opacity: 0.8; }}
}}
</style>
"""

components.html(js_telemetry_engine, height=600, scrolling=True)
st.caption("⚡ Conexão direta com servidores OpenF1 ativa. Altere a Session Key acima de acordo com o GP do final de semana.")
