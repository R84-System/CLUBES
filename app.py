import streamlit as st
import streamlit.components.v1 as components
import requests

# Configuração de Página Ultra-Wide e responsiva
st.set_page_config(page_title="F1 Ultra-Low Latency Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: #FF1801; margin-bottom: 5px;'>🏎️ F1 REAL-TIME TELEMETRY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; margin-top: 0px;'>Painel Inteligente Automático — Baixa Latência</p>", unsafe_allow_html=True)

# --- CONFIGURAÇÃO AUTOMÁTICA DE SESSÕES VIA PYTHON ---
@st.cache_data(ttl=300)  # Atualiza a lista a cada 5 minutos
def buscar_sessoes_ativas():
    try:
        # Busca as últimas sessões registradas no servidor OpenF1
        url = "https://api.openf1.org/v1/sessions"
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            # Inverte para mostrar as mais recentes primeiro e filtra dados válidos
            dados_recentes = dados[::-1][:25]
            opcoes = {}
            for s in dados_recentes:
                # Monta um nome amigável para o menu: Ex: "Monaco (2024) - Race"
                nome_formatado = f"📍 {s.get('location', 'Desconhecido')} ({s.get('year')}) - {s.get('session_name')}"
                opcoes[nome_formatado] = str(s.get('session_key'))
            return opcoes
    except Exception as e:
        pass
    # Caso o servidor falhe, retorna uma sessão padrão histórica de segurança
    return {"GP de Mônaco - Corrida Histórica": "9523"}

# Carrega o menu no topo do painel do tablet
dicionario_sessoes = buscar_sessoes_ativas()
sessao_selecionada = st.selectbox("🏁 Selecione o Grande Prêmio / Sessão atual:", list(dicionario_sessoes.keys()))
session_key_final = dicionario_sessoes[sessao_selecionada]

# Mostra o ID ativo em tamanho menor para checagem rápida
st.caption(f"ID da Sessão ativa enviado ao Motor JS: `{session_key_final}`")
st.markdown("---")

# --- BLOCCO JAVASCRIPT INJETADO (Mínima Latência) ---
js_telemetry_engine = f"""
<div style="background-color: #1a1a1a; padding: 20px; border-radius: 10px; font-family: monospace; color: white; border: 1px solid #333;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px;">
        <div style="background: #262626; padding: 15px; border-radius: 8px; border-left: 5px solid #FF1801;">
            <h3 style="margin: 0 0 10px 0; color: #FF1801;">STATUS DA PISTA</h3>
            <div id="track-status" style="font-size: 24px; font-weight: bold; animation: pulse 2s infinite;">Conectando sinal...</div>
        </div>
        <div style="background: #262626; padding: 15px; border-radius: 8px; border-left: 5px solid #00D2C4;">
            <h3 style="margin: 0 0 10px 0; color: #00D2C4;">MAIOR VELOCIDADE EM PISTA</h3>
            <div id="top-speed" style="font-size: 28px; font-weight: bold;">-- <span style="font-size: 14px; color: #888;">km/h</span></div>
            <div id="top-driver" style="font-size: 14px; color: #aaa;">Buscando telemetria...</div>
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
            <tr><td colspan="4" style="padding: 20px; text-align: center; color: #666;">Aguardando sincronia com a cronometragem oficial...</td></tr>
        </tbody>
    </table>
</div>

<script>
const SESSION_KEY = "{session_key_final}";

async function updateTelemetry() {{
    try {{
        // 1. Status da Pista (Bandeiras)
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
            document.getElementById('track-status').innerText = "SEM INFOS AO VIVO";
        }}

        // 2. Velocidade Máxima Recente
        const carRes = await fetch(`https://openf1.org{{SESSION_KEY}}&speed>230`);
        const carData = await carRes.json();
        if(carData && carData.length > 0) {{
            let maxSpeed = 0;
            let fastDriver = "";
            carData.slice(-80).forEach(d => {{
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

        // 3. Tabela de Posições e Gaps
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
            sortedGrid.slice(0, 12).forEach((row, index) => {{
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
            document.getElementById('grid-table-body').innerHTML = '<tr><td colspan="4" style="padding: 20px; text-align: center; color: #888;">Sessão antiga ou sem carros na pista neste momento.</td></tr>';
        }}

    }} catch (error) {{
        console.error("Erro na busca de dados JS:", error);
    }}
}}

// Executa o pooling a cada 2 segundos no dispositivo cliente
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

components.html(js_telemetry_engine, height=650, scrolling=True)
st.caption("⚡ Sincronização direta com a infraestrutura OpenF1 via JavaScript.")
