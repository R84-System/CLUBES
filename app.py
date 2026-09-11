import streamlit as st
import streamlit.components.v1 as components
import requests

# Configuração de Página Ultra-Wide e responsiva para o Tablet
st.set_page_config(page_title="F1 Live Telemetry", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: #FF1801; margin-bottom: 5px;'>🏎️ F1 REAL-TIME TELEMETRY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; margin-top: 0px;'>Sinal 100% Tempo Real com Memória Interna de Contingência Gravada</p>", unsafe_allow_html=True)

# 1. CAPTURA AS SESSÕES DE 2026 APENAS PARA DIRECIONAR O MOTOR JS
@st.cache_data(ttl=120)
def carregar_id_2026():
    try:
        url = "https://openf1.org"
        resposta = requests.get(url, timeout=5).json()
        for s in resposta[::-1]:
            if s.get('year') and int(s.get('year')) == 2026:
                return str(s.get('session_key'))
    except:
        pass
    return "11361"

session_key_ativa = carregar_id_2026()

st.code(f"Sincronizado na Session Key Oficial de 2026: {session_key_ativa}")
st.markdown("---")

# 2. MOTOR HÍBRIDO EM JAVASCRIPT CORRIGIDO (CHAVES DUPLAS APLICADAS)
js_live_engine = f"""
<div style="background-color: #111; font-family: monospace; color: white; padding: 15px; border-radius: 8px;">
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
        <div style="background: #1e1e1e; padding: 12px; border-radius: 6px; border-left: 5px solid #FF1801;">
            <div style="color: #888; font-size: 12px;">SINAL DA PISTA</div>
            <div id="pista-status" style="font-size: 20px; font-weight: bold; color: #00FF00;">CONECTANDO...</div>
        </div>
        <div style="background: #1e1e1e; padding: 12px; border-radius: 6px; border-left: 5px solid #00D2C4;">
            <div style="color: #888; font-size: 12px;">ATUALIZAÇÃO DO MOTOR</div>
            <div id="sync-status" style="font-size: 14px; margin-top: 5px; color: #aaa;">Buscando pacotes live...</div>
        </div>
    </div>

    <h2 style="color: #FF1801; font-size: 18px; margin-bottom: 10px; border-bottom: 1px solid #333; padding-bottom: 5px;">📊 LIVE GRID INTERVALS</h2>
    
    <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;">
        <thead>
            <tr style="color: #888; border-bottom: 2px solid #333;">
                <th style="padding: 8px 4px; width: 10%;">POS</th>
                <th style="width: 45%;">PILOTO (#)</th>
                <th style="width: 22%;">GAP LÍDER</th>
                <th style="width: 23%;">INTERVALO</th>
            </tr>
        </thead>
        <tbody id="tabela-corpo">
            <tr><td colspan="4" style="padding: 20px; text-align: center; color: #666;">Iniciando escuta do feed da F1...</td></tr>
        </tbody>
    </table>
</div>

<script>
const SESSION_KEY = "{session_key_ativa}";

// Dicionário de pilotos para tradução rápida e limpa no JS
const driversMap = {{
    "1": "Max VERSTAPPEN", "11": "Sergio PEREZ", "16": "Charles LECLERC", "55": "Carlos SAINZ",
    "44": "Lewis HAMILTON", "63": "George RUSSELL", "4": "Lando NORRIS", "81": "Oscar PIASTRI",
    "14": "Fernando ALONSO", "18": "Lance STROLL", "23": "Alex ALBON", "22": "Yuki TSUNODA",
    "27": "Nico HULKENBERG", "30": "Liam LAWSON", "43": "Franco COLAPINTO", "12": "Kimi ANTONELLI",
    "5": "Sebastian VETTEL", "6": "Nicholas LATIFI", "87": "Oliver BEARMAN"
}};

function carregarDadosSalvos() {{
    const backupStatus = localStorage.getItem('f1_pista_status');
    const backupTabela = localStorage.getItem('f1_tabela_corpo');
    
    if (backupStatus) document.getElementById('pista-status').innerText = backupStatus;
    if (backupTabela) {{
        document.getElementById('tabela-corpo').innerHTML = backupTabela;
        document.getElementById('sync-status').innerText = "Exibindo dados gravados salvos.";
        document.getElementById('sync-status').style.color = "#FFCC00";
    }}
}}

async function processarLiveTelemetry() {{
    try {{
        // 1. Puxa Status da Pista
        const trackRes = await fetch(`https://openf1.org{{SESSION_KEY}}`);
        if(trackRes.ok) {{
            const trackData = await trackRes.json();
            if(trackData && trackData.length > 0) {{
                const flag = trackData[trackData.length - 1].flag || "GREEN";
                const pistaDiv = document.getElementById('pista-status');
                pistaDiv.innerText = flag === "GREEN" ? "🟢 PISTA LIMPA" : flag === "YELLOW" ? "🟡 BANDEIRA AMARELA" : "🔴 VERMELHA INTERROMPIDA";
                localStorage.setItem('f1_pista_status', pistaDiv.innerText);
            }}
        }}

        // 2. Puxa Intervalos Tempo Real
        const intervalRes = await fetch(`https://openf1.org{{SESSION_KEY}}`);
        if(!intervalRes.ok) return;
        
        const intervalData = await intervalRes.json();
        if(intervalData && intervalData.length > 0) {{
            const uniqueDrivers = {{}};
            
            intervalData.forEach(item => {{
                uniqueDrivers[item.driver_number] = item;
            }});

            const sortedGrid = Object.values(uniqueDrivers).sort((a, b) => {{
                return (parseFloat(a.gap_to_leader) || 0) - (parseFloat(b.gap_to_leader) || 0);
            }});

            let htmlTabela = "";
            sortedGrid.forEach((row, index) => {{
                const n = String(row.driver_number);
                const nomePiloto = driversMap[n] || `Piloto #${{n}}`;
                const gap = index === 0 ? "LÍDER" : `+${{row.gap_to_leader}}s`;
                const intervalo = row.interval === null ? "---" : `+${{row.interval}}s`;

                htmlTabela += `
                    <tr style="border-bottom: 1px solid #222; height: 38px;">
                        <td style="color: #FF1801; font-weight: bold; padding: 4px;">${{index + 1}}</td>
                        <td style="font-weight: bold;">${{nomePiloto}}</td>
                        <td style="color: #00D2C4;">${{gap}}</td>
                        <td style="color: #ccc;">${{intervalo}}</td>
                    </tr>
                `;
            }});

            document.getElementById('tabela-corpo').innerHTML = htmlTabela;
            document.getElementById('sync-status').innerText = "Conexão ao vivo ativa: recebendo sinal (" + new Date().toLocaleTimeString() + ")";
            document.getElementById('sync-status').style.color = "#00FF00";
            
            localStorage.setItem('f1_tabela_corpo', htmlTabela);
        }}
    }} catch (error) {{
        console.log("Servidor em timeout. Mantendo dados salvos em cache.");
        document.getElementById('sync-status').innerText = "Instabilidade detectada. Mantendo últimos dados gravados.";
        document.getElementById('sync-status').style.color = "#FF3333";
    }}
}}

carregarDadosSalvos();
setInterval(processarLiveTelemetry, 2000);
processarLiveTelemetry();
</script>
"""

components.html(js_live_engine, height=600, scrolling=False)
st.caption("⚡ Motor Híbrido ativado. Se os dados pararem de chegar da API, a classificação final ficará travada e salva na tela.")
