import streamlit as st
import requests

# Configuração de Página Ultra-Wide e responsiva para o Tablet
st.set_page_config(page_title="F1 Live Telemetry", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: #FF1801; margin-bottom: 5px;'>🏎️ F1 REAL-TIME TELEMETRY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; margin-top: 0px;'>Painel Definitivo — Modo Híbrido com Simulador de Pista Embutido</p>", unsafe_allow_html=True)

# 1. SELETOR DE MODO NO TOPO DO TABLET (Garante o funcionamento mesmo se a API cair)
modo_painel = st.radio(
    "📡 SELECIONE O MODO DE OPERAÇÃO DO SINAL:",
    ("Sinal Oficial da F1 (Requer Servidor Online)", "Modo Simulação Dinâmica (À Prova de Quedas/Testes)"),
    horizontal=True
)

# 2. CAPTURA AUTOMÁTICA DA ÚLTIMA SESSÃO (Roda apenas no modo oficial)
session_key_ativa = "11361"
nome_do_gp = "Conexão de Contingência Local"

if modo_painel == "Sinal Oficial da F1 (Requer Servidor Online)":
    try:
        url = "https://openf1.org"
        resposta = requests.get(url, timeout=3).json()
        if resposta and len(resposta) > 0:
            ultimo_evento = resposta[-1]
            session_key_ativa = str(ultimo_evento.get('session_key'))
            nome_do_gp = f"{ultimo_evento.get('location')} ({ultimo_evento.get('year')}) - {ultimo_evento.get('session_name')}"
    except:
        pass
    st.success(f"📺 Modo Live: Monitorando {nome_do_gp} | ID: `{session_key_ativa}`")
else:
    st.warning("🎮 Modo Simulação Ativo: Gerando dados de corrida locais de alta velocidade a 2000ms.")

st.markdown("---")

# Define se o JavaScript vai usar dados da internet ou dados simulados locais
usar_simulador = "true" if modo_painel == "Modo Simulação Dinâmica (À Prova de Quedas/Testes)" else "false"

# 3. MOTOR EM JAVASCRIPT ROBUSTO COM SIMULADOR INTEGRADO
js_live_engine = f"""
<div style="background-color: #111; font-family: monospace; color: white; padding: 15px; border-radius: 8px;">
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
        <div style="background: #1e1e1e; padding: 12px; border-radius: 6px; border-left: 5px solid #FF1801;">
            <div style="color: #888; font-size: 12px;">SINAL DA PISTA</div>
            <div id="pista-status" style="font-size: 20px; font-weight: bold; color: #00FF00;">CONECTANDO...</div>
        </div>
        <div style="background: #1e1e1e; padding: 12px; border-radius: 6px; border-left: 5px solid #00D2C4;">
            <div style="color: #888; font-size: 12px;">STATUS DO SINAL</div>
            <div id="sync-status" style="font-size: 13px; margin-top: 5px; color: #aaa;">Buscando telemetria...</div>
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
            <tr><td colspan="4" style="padding: 20px; text-align: center; color: #666;">Iniciando conexões do feed...</td></tr>
        </tbody>
    </table>
</div>

<script>
const SESSION_KEY = "{session_key_ativa}";
const SIMULAR_ATIVO = {usar_simulador};

const driversMap = {{
    "1": "Max VERSTAPPEN", "11": "Sergio PEREZ", "16": "Charles LECLERC", "55": "Carlos SAINZ",
    "44": "Lewis HAMILTON", "63": "George RUSSELL", "4": "Lando NORRIS", "81": "Oscar PIASTRI",
    "14": "Fernando ALONSO", "43": "Franco COLAPINTO", "12": "Kimi ANTONELLI"
}};

// Dados iniciais estáveis para alimentar o simulador interno se a API falhar
let simGrid = [
    {{driver: "Lando NORRIS", gap: 0.0, interval: 0.0}},
    {{driver: "Oscar PIASTRI", gap: 0.521, interval: 0.521}},
    {{driver: "Charles LECLERC", gap: 2.140, interval: 1.619}},
    {{driver: "Max VERSTAPPEN", gap: 4.890, interval: 2.750}},
    {{driver: "George RUSSELL", gap: 6.120, interval: 1.230}},
    {{driver: "Lewis HAMILTON", gap: 8.450, interval: 2.330}},
    {{driver: "Kimi ANTONELLI", gap: 12.980, interval: 4.530}},
    {{driver: "Franco COLAPINTO", gap: 18.420, interval: 5.440}}
];

async function processarLiveTelemetry() {{
    // CAMINHO A: MODO SIMULAÇÃO (Roda localmente sem precisar de internet ou servidores externos)
    if(SIMULAR_ATIVO) {{
        document.getElementById('pista-status').innerText = "🟢 PISTA LIMPA (SIM)";
        document.getElementById('pista-status').style.color = "#00FF00";
        document.getElementById('sync-status').innerText = "Gerador interno ativo. Motores a 2500ms.";
        document.getElementById('sync-status').style.color = "#FFCC00";

        // Simula pequenas mudanças nos tempos de volta a cada ciclo para dar realismo de corrida
        simGrid.forEach((row, i) => {{
            if(i > 0) {{
                let variacao = (Math.random() * 0.4) - 0.2; // Varia entre -0.2s e +0.2s
                row.interval = Math.max(0.01, row.interval + variacao);
                row.gap = simGrid[i-1].gap + row.interval;
            }}
        }});
        
        // Reordena o grid caso algum piloto ultrapasse o outro na simulação
        simGrid.sort((a, b) => a.gap - b.gap);

        let html = "";
        simGrid.forEach((row, index) => {{
            html += `<tr style="border-bottom: 1px solid #222; height: 38px;">
                <td style="color: #FF1801; font-weight: bold; padding: 4px;">${{index + 1}}</td>
                <td style="font-weight: bold;">${{row.driver}}</td>
                <td style="color: #00D2C4;">${{index === 0 ? "LÍDER" : "+" + row.gap.toFixed(3) + "s"}}</td>
                <td style="color: #ccc;">${{index === 0 ? "---" : "+" + row.interval.toFixed(3) + "s"}}</td>
            </tr>`;
        }});
        document.getElementById('tabela-corpo').innerHTML = html;
        return;
    }}

    # CAMINHO B: MODO LIVE REAL (Conecta na internet buscando o treino ao vivo)
    try {{
        const trackRes = await fetch(`https://openf1.org{{SESSION_KEY}}`);
        if(trackRes.ok) {{
            const trackData = await trackRes.json();
            if(trackData && trackData.length > 0) {{
                const flag = trackData[trackData.length - 1].flag || "GREEN";
                const pistaDiv = document.getElementById('pista-status');
                pistaDiv.innerText = flag === "GREEN" ? "🟢 PISTA LIMPA" : flag === "YELLOW" ? "🟡 BANDEIRA AMARELA" : "🔴 BANDEIRA VERMELHA";
            }}
        }}

        const intervalRes = await fetch(`https://openf1.org{{SESSION_KEY}}`);
        if(!intervalRes.ok) return;
        
        const intervalData = await intervalRes.json();
        if(intervalData && intervalData.length > 0) {{
            const uniqueDrivers = {{}};
            intervalData.forEach(item => {{ uniqueDrivers[item.driver_number] = item; }});
            const sortedGrid = Object.values(uniqueDrivers).sort((a, b) => (parseFloat(a.gap_to_leader) || 0) - (parseFloat(b.gap_to_leader) || 0));

            let htmlTabela = "";
            sortedGrid.forEach((row, index) => {{
                const n = String(row.driver_number);
                const nomePiloto = driversMap[n] || `Piloto #${{n}}`;
                const gap = index === 0 ? "LÍDER" : `+${{row.gap_to_leader}}s`;
                const intervalo = row.interval === null ? "---" : `+${{row.interval}}s`;

                htmlTabela += `<tr style="border-bottom: 1px solid #222; height: 38px;">
                    <td style="color: #FF1801; font-weight: bold; padding: 4px;">${{index + 1}}</td>
                    <td style="font-weight: bold;">${{nomePiloto}}</td>
                    <td style="color: #00D2C4;">${{gap}}</td>
                    <td style="color: #ccc;">${{intervalo}}</td>
                </tr>`;
            }});

            document.getElementById('tabela-corpo').innerHTML = htmlTabela;
            document.getElementById('sync-status').innerText = "Sinal Oficial Conectado (" + new Date().toLocaleTimeString() + ")";
            document.getElementById('sync-status').style.color = "#00FF00";
        }} else {{
            document.getElementById('sync-status').innerText = "Servidor conectado, mas sem carros na pista agora.";
            document.getElementById('sync-status').style.color = "#FFCC00";
        }}
    }} catch (error) {{
        document.getElementById('sync-status').innerText = "Servidor OpenF1 offline ou congestionado.";
        document.getElementById('sync-status').style.color = "#FF3333";
    }}
}}

// Início do ciclo em segundo plano (2500ms)
setInterval(processarLiveTelemetry, 2500);
processarLiveTelemetry();
</script>
"""

components.html(js_live_engine, height=550, scrolling=False)
st.caption("⚡ Sistema de telemetria integrado para o Tablet concluído.")
