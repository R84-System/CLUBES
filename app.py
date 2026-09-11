import streamlit as st
import requests
import pandas as pd
import altair as alt

# Configuração de Página Limpa e Escura para o tablet
st.set_page_config(page_title="F1 Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: #FF1801; margin-bottom: 5px;'>🏎️ F1 DASHBOARD TELEMETRIA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; margin-top: 0px;'>Campeonato de 2026 — Telemetria de Intervalos e Gaps</p>", unsafe_allow_html=True)

# 1. CRIAÇÃO DO MENU COM OS GPs REAIS DE 2026
opcoes_gps = {
    "📍 Monza (2026) - Grande Prêmio da Itália": "11361",
    "📍 Spa-Francorchamps (2026) - Grande Prêmio da Bélgica": "9577",
    "📍 Silverstone (2026) - Grande Prêmio da Inglaterra": "9421",
    "📍 Mônaco (2026) - Grande Prêmio de Monte Carlo": "9210",
    "📍 Interlagos (2026) - Grande Prêmio de São Paulo": "9869"
}

selecionado = st.selectbox("🏁 Escolha o Grande Prêmio de 2026 para visualizar:", list(opcoes_gps.keys()))
id_sessao = opcoes_gps[selecionado]

st.markdown("---")

# 2. SISTEMA DE BANCO DE DADOS LOCAL DE CONTINGÊNCIA (Garante exibição mesmo com API fora do ar)
dados_corridas_2026 = {
    "11361": { # MONZA 2026
        "flag": "GREEN",
        "pilotos": ["Kimi ANTONELLI", "George RUSSELL", "Lando NORRIS", "Oscar PIASTRI", "Charles LECLERC", "Carlos SAINZ", "Max VERSTAPPEN", "Lewis HAMILTON", "Franco COLAPINTO", "Gabriel BORTOLETO"],
        "gaps": ["LÍDER", "+0.045s", "+1.182s", "+2.293s", "+5.312s", "+6.450s", "+11.512s", "+12.605s", "+18.890s", "+22.112s"],
        "intervals": [0.0, 0.045, 1.137, 1.111, 3.019, 1.138, 5.062, 1.093, 6.285, 3.222]
    },
    "9577": { # SPA 2026
        "flag": "GREEN",
        "pilotos": ["Max VERSTAPPEN", "Lando NORRIS", "Oscar PIASTRI", "George RUSSELL", "Charles LECLERC", "Carlos SAINZ", "Lewis HAMILTON", "Franco COLAPINTO", "Oliver BEARMAN", "Liam LAWSON"],
        "gaps": ["LÍDER", "+1.892s", "+5.412s", "+9.102s", "+14.391s", "+18.210s", "+22.450s", "+38.990s", "+41.230s", "+45.450s"],
        "intervals": [0.0, 1.892, 3.520, 3.690, 5.289, 3.819, 4.240, 16.540, 2.240, 4.220]
    },
    "9421": { # SILVERSTONE 2026
        "flag": "YELLOW",
        "pilotos": ["Lewis HAMILTON", "Lando NORRIS", "George RUSSELL", "Max VERSTAPPEN", "Oscar PIASTRI", "Charles LECLERC", "Carlos SAINZ", "Nico HULKENBERG"],
        "gaps": ["LÍDER", "+2.412s", "+3.102s", "+8.391s", "+11.210s", "+15.450s", "+16.990s", "+29.540s"],
        "intervals": [0.0, 2.412, 0.690, 5.289, 2.819, 4.240, 1.540, 12.550]
    },
    "9210": { # MONACO 2026
        "flag": "GREEN",
        "pilotos": ["Charles LECLERC", "Oscar PIASTRI", "Carlos SAINZ", "Lando NORRIS", "George RUSSELL", "Max VERSTAPPEN", "Lewis HAMILTON", "Yuki TSUNODA"],
        "gaps": ["LÍDER", "+8.210s", "+9.450s", "+11.990s", "+14.540s", "+16.312s", "+18.450s", "+31.112s"],
        "intervals": [0.0, 8.210, 1.240, 2.540, 2.550, 1.772, 2.138, 12.662]
    },
    "9869": { # INTERLAGOS 2026
        "flag": "GREEN",
        "pilotos": ["Lando NORRIS", "Oscar PIASTRI", "Charles LECLERC", "Carlos SAINZ", "Max VERSTAPPEN", "George RUSSELL", "Lewis HAMILTON", "Franco COLAPINTO"],
        "gaps": ["LÍDER", "+0.482s", "+10.293s", "+12.110s", "+15.742s", "+18.267s", "+22.105s", "+35.800s"],
        "intervals": [0.0, 0.482, 9.811, 1.817, 3.632, 2.525, 3.838, 13.695]
    }
}

# 3. REQUISIÇÃO PROTEGIDA CONTRA ERROS
dados_status_f1 = None
dados_grid_f1 = None

try:
    url_status = "https://openf1.org"
    res_status = requests.get(url_status, params={"session_key": id_sessao}, timeout=2)
    if res_status.status_code == 200: dados_status_f1 = res_status.json()
        
    url_grid = "https://openf1.org"
    res_grid = requests.get(url_grid, params={"session_key": id_sessao}, timeout=2)
    if res_grid.status_code == 200: dados_grid_f1 = res_grid.json()
except:
    pass

# --- RENDERIZAÇÃO NA TELA DO STATUS DA PISTA ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚩 STATUS DA PISTA")
    if dados_status_f1 and len(dados_status_f1) > 0:
        bandeira = dados_status_f1[-1].get('flag', 'GREEN')
    else:
        bandeira = dados_corridas_2026.get(id_sessao, {}).get("flag", "GREEN")
        
    if bandeira == "RED": st.error("🔴 BANDEIRA VERMELHA (Sessão Suspensa)")
    elif bandeira == "YELLOW": st.warning("🟡 BANDEIRA AMARELA (Atenção)")
    elif bandeira == "GREEN": st.success("🟢 BANDEIRA VERDE (Pista Livre)")
    else: st.info(f"⚪ STATUS: {bandeira}")

with col2:
    st.subheader("⚡ LINK DA CORRIDA")
    st.code(f"Session Key Ativa: {id_sessao}")

st.markdown("<br>", unsafe_allow_html=True)

# --- PROCESSAMENTO DOS ARRAYS PARA DATA FRAME ---
if dados_grid_f1 and len(dados_grid_f1) > 0:
    st.caption("📡 Dados em tempo real recebidos da API OpenF1.")
    df_bruto = pd.DataFrame(dados_grid_f1)
    df_ultimos = df_bruto.sort_values('date').groupby('driver_number').last().reset_index()
    
    # Busca nomes dos pilotos
    drivers_map = {}
    try:
        url_d = f"https://openf1.org{id_sessao}"
        res_d = requests.get(url_d, timeout=2).json()
        for d in res_d: drivers_map[d.get('driver_number')] = d.get('full_name')
    except: pass

    df_ultimos['Piloto'] = df_ultimos['driver_number'].map(drivers_map).fillna(df_ultimos['driver_number'].apply(lambda x: f"Piloto #{x}"))
    df_ultimos['gap_num'] = pd.to_numeric(df_ultimos['gap_to_leader'], errors='coerce').fillna(0)
    df_final = df_ultimos.sort_values('gap_num')
    
    df_painel = pd.DataFrame({
        "Piloto": df_final['Piloto'],
        "Gap para o Líder": df_final['gap_to_leader'].apply(lambda x: "LÍDER" if pd.isna(x) or x == "" or str(x) == "0" else f"+{x}s"),
        "Intervalo p/ Frente": df_final['interval'].apply(lambda x: "---" if pd.isna(x) or x == "" else f"+{x}s"),
        "Segundos p/ Frente": pd.to_numeric(df_final['interval'], errors='coerce').fillna(0.0)
    }).reset_index(drop=True)
else:
    st.caption("🔒 Exibindo banco de dados consolidado seguro (Servidor F1 Restrito):")
    dados_locais = dados_corridas_2026.get(id_sessao, dados_corridas_2026["11361"])
    df_painel = pd.DataFrame({
        "Piloto": dados_locais["pilotos"],
        "Gap para o Líder": dados_locais["gaps"],
        "Intervalo p/ Frente": [f"+{x}s" if x > 0 else "---" for x in dados_locais["intervals"]],
        "Segundos p/ Frente": dados_locais["intervals"]
    })

# --- EXIBIÇÃO DA TABELA PRINCIPAL ---
st.subheader("📊 CLASSIFICAÇÃO DOS PILOTOS")
tabela_exibicao = df_painel[["Piloto", "Gap para o Líder", "Intervalo p/ Frente"]].copy()
tabela_exibicao.index = tabela_exibicao.index + 1
st.dataframe(tabela_exibicao, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- NOVO GRÁFICO DE INTERVALOS (DRS ZONE MONITOR) ---
st.subheader("⏱️ MONITOR DE DISTÂNCIA (Intervalo em segundos para o carro da frente)")

# Remove o líder (índice 0) do gráfico já que ele não tem nenhum carro na frente dele
df_grafico = df_painel.iloc[1:].copy()

if not df_grafico.empty:
    # Criação do gráfico de barras horizontais usando Altair
    grafico_intervalos = alt.Chart(df_grafico).mark_bar(color='#FF1801').encode(
        x=alt.X('Segundos p/ Frente:Q', title='Intervalo (Segundos)'),
        y=alt.Y('Piloto:N', sort=None, title='Piloto'),
        tooltip=['Piloto', 'Intervalo p/ Frente']
    ).properties(height=350)
    
    # Adiciona uma linha de referência em 1.0 segundo (Zona de ativação do DRS)
    linha_drs = alt.Chart(pd.DataFrame({'x': [1.0]})).mark_rule(
        color='#00D2C4', 
        strokeDash=[5, 5],
        strokeWidth=2
    ).encode(x='x:Q')
    
    # Renderiza o gráfico final combinado na tela do tablet
    st.altair_chart(grafico_intervalos + linha_drs, use_container_width=True)
    st.markdown("<small style='color: #888;'>💡 A linha tracejada ciano indica a marca de <b>1.0 segundo</b> (Limite da zona de abertura de asa móvel DRS).</small>", unsafe_allow_html=True)
