import streamlit as st

# 1. Configuração da Página para Largura Total
st.set_page_config(
    page_title="F1 Pro Dashboard",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Ocultação do cabeçalho, rodapé e ajuste de margens nativas do Streamlit
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 0.4rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }
        header {visibility: hidden;} /* Oculta o cabeçalho padrão */
        footer {visibility: hidden;} /* Oculta o rodapé padrão */
        
        /* Ajuste do fundo geral da aplicação */
        .stApp {
            background-color: #0e1117;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Painel F1 construído com HTML/CSS customizado e integrado via iframe
f1_dashboard_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #0e1117;
            color: #ffffff;
            margin: 0;
            padding: 0;
        }
        /* Cabeçalho Estilo F1 */
        .f1-header {
            background: linear-gradient(90deg, #e10600 0%, #15151e 70%);
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.6);
            margin-bottom: 12px;
        }
        .f1-logo {
            font-size: 22px;
            font-weight: 900;
            font-style: italic;
            letter-spacing: 2px;
            color: #ffffff;
        }
        .f1-logo span {
            color: #e10600;
            background: #ffffff;
            padding: 2px 6px;
            border-radius: 4px;
            margin-left: 4px;
        }
        .live-badge {
            background: #22c55e;
            color: #fff;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }

        /* Barra de Filtros e Controles Horizontal */
        .controls-bar {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            background: #161b22;
            padding: 12px 15px;
            border-radius: 8px;
            border-top: 3px solid #e10600;
            align-items: flex-end;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }
        .control-group {
            display: flex;
            flex-direction: column;
            font-size: 11px;
            color: #8b949e;
            text-transform: uppercase;
            font-weight: bold;
        }
        .control-group select, .control-group input {
            background: #0d1117;
            color: #fff;
            border: 1px solid #30363d;
            padding: 7px 10px;
            border-radius: 6px;
            margin-top: 4px;
            font-size: 13px;
            outline: none;
        }
        .control-group select:focus, .control-group input:focus {
            border-color: #e10600;
        }

        /* Grid de Cards */
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }
        .card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }
        .card-title {
            font-size: 15px;
            font-weight: bold;
            color: #f0f6fc;
            margin-bottom: 10px;
            border-bottom: 1px solid #30363d;
            padding-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Tabelas Estilizadas */
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        th, td {
            padding: 7px 8px;
            text-align: left;
            border-bottom: 1px solid #21262d;
        }
        th {
            color: #8b949e;
            font-weight: 600;
            background: #0d1117;
        }
        tr:hover {
            background: #1f242c;
        }
        .pos-1 { color: #facc15; font-weight: bold; }
        .pos-2 { color: #e5e7eb; font-weight: bold; }
        .pos-3 { color: #fb923c; font-weight: bold; }
        
        .telemetry-box {
            background: #0d1117;
            border: 1px solid #30363d;
            padding: 10px;
            border-radius: 6px;
            margin-top: 8px;
        }
        .metric-row {
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            margin-bottom: 6px;
        }
        .metric-label { color: #8b949e; }
        .metric-value { font-weight: bold; color: #58a6ff; }
    </style>
</head>
<body>

    <!-- Header F1 -->
    <div class="f1-header">
        <div class="f1-logo">FORMULA 1 <span>DASHBOARD</span></div>
        <div><span class="live-badge">TEMPORADA ATIVA</span></div>
    </div>

    <!-- Barra de Controles Superior -->
    <div class="controls-bar">
        <div class="control-group">
            <label>Temporada</label>
            <select>
                <option>2026</option>
                <option>2025</option>
                <option>2024</option>
            </select>
        </div>
        <div class="control-group">
            <label>Grande Prêmio</label>
            <select>
                <option>Round 08: GP de Mônaco 🇲🇨</option>
                <option>Round 07: GP de Ímola 🇮🇹</option>
                <option>Round 06: GP de Miami 🇺🇸</option>
            </select>
        </div>
        <div class="control-group">
            <label>Sessão</label>
            <select>
                <option>Corrida (Race)</option>
                <option>Qualificação (Quali)</option>
                <option>Treino Livre (FP3)</option>
            </select>
        </div>
        <div class="control-group">
            <label>Buscar Piloto / Equipe</label>
            <input type="text" placeholder="Ex: Verstappen, Ferrari...">
        </div>
    </div>

    <!-- Layout em Grid / Blocos -->
    <div class="grid-container">
        
        <!-- Card 1: Tabela de Pilotos -->
        <div class="card">
            <div class="card-title">🏆 Mundial de Pilotos (Top 5)</div>
            <table>
                <tr><th>Pos</th><th>Piloto</th><th>Equipe</th><th>Pts</th></tr>
                <tr><td class="pos-1">1</td><td>M. Verstappen</td><td>Red Bull</td><td>165</td></tr>
                <tr><td class="pos-2">2</td><td>L. Hamilton</td><td>Ferrari</td><td>142</td></tr>
                <tr><td class="pos-3">3</td><td>C. Leclerc</td><td>Ferrari</td><td>138</td></tr>
                <tr><td>4</td><td>L. Norris</td><td>McLaren</td><td>125</td></tr>
                <tr><td>5</td><td>O. Piastri</td><td>McLaren</td><td>110</td></tr>
            </table>
        </div>

        <!-- Card 2: Tabela de Construtores -->
        <div class="card">
            <div class="card-title">🏎️ Mundial de Construtores</div>
            <table>
                <tr><th>Pos</th><th>Construtor</th><th>Pts</th></tr>
                <tr><td class="pos-1">1</td><td>Scuderia Ferrari</td><td>280</td></tr>
                <tr><td class="pos-2">2</td><td>Red Bull Racing</td><td>245</td></tr>
                <tr><td class="pos-3">3</td><td>McLaren F1 Team</td><td>235</td></tr>
                <tr><td>4</td><td>Mercedes AMG F1</td><td>180</td></tr>
                <tr><td>5</td><td>Aston Martin Aramco</td><td>75</td></tr>
            </table>
        </div>

        <!-- Card 3: Telemetria / Voltas Rápidas -->
        <div class="card">
            <div class="card-title">⚡ Volta Mais Rápida da Pista</div>
            <div class="telemetry-box">
                <div class="metric-row"><span class="metric-label">Piloto:</span><span class="metric-value">L. Hamilton</span></div>
                <div class="metric-row"><span class="metric-label">Equipe:</span><span class="metric-value">Ferrari</span></div>
                <div class="metric-row"><span class="metric-label">Tempo:</span><span class="metric-value" style="color: #facc15;">1:12.984</span></div>
                <div class="metric-row"><span class="metric-label">Velocidade Média:</span><span class="metric-value">168.4 km/h</span></div>
                <div class="metric-row"><span class="metric-label">Volta:</span><span class="metric-value">64 / 78</span></div>
            </div>
        </div>

    </div>

</body>
</html>
"""

# Renderizando o painel F1 customizado sem margens laterais e preenchendo a tela inteira
st.components.v1.html(f1_dashboard_html, height=620, scrolling=True)
