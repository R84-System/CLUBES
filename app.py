import streamlit as st
import requests
import pandas as pd

# Configuração de Página Limpa e Escura para o tablet
st.set_page_config(page_title="F1 Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: #FF1801; margin-bottom: 5px;'>🏎️ F1 DASHBOARD TELEMETRIA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; margin-top: 0px;'>Painel de Contingência — Proteção contra quedas de API</p>", unsafe_allow_html=True)

# 1. BUSCA AS SESSÕES (Filtro seguro direto no Python)
@st.cache_data(ttl=120)
def carregar_gps():
    try:
        url = "https://api.openf1.org/v1/sessions"
        resposta = requests.get(url, timeout=5)
        
        # Garante que só vai ler se o servidor responder com sucesso (Status 200) e formato correto
        if resposta.status_code == 200 and "application/json" in resposta.headers.get("Content-Type", ""):
            r = resposta.json()
            opcoes = {}
            for s in r[::-1]:
                ano = s.get('year')
                # Bloqueia as sessões vazias planejadas para 2026, focando em dados reais históricos
                if ano and int(ano) < 2026:
                    nome = f"📍 {s.get('location')} ({ano}) - {s.get('session_name')}"
                    if nome not in opcoes and len(opcoes) < 25:
                        opcoes[nome] = str(s.get('session_key'))
            if opcoes:
                return opcoes
    except:
        pass
    # Backup estável de segurança caso o servidor OpenF1 esteja offline
    return {"📍 Monaco (2024) - Race": "9523", "📍 Spa-Francorchamps (2024) - Race": "9549"}

dicionario_gps = carregar_gps()
selecionado = st.selectbox("🏁 Escolha o Grande Prêmio:", list(dicionario_gps.keys()))
id_sessao = dicionario_gps[selecionado]

if st.button("🔄 Forçar Atualização do Sinal"):
    st.cache_data.clear()
    st.rerun()

st.markdown("---")

# Mapeamento dos pilotos reais do grid
drivers_map = {
    1: "Max VERSTAPPEN (Red Bull)", 11: "Sergio PEREZ (Red Bull)", 
    16: "Charles LECLERC (Ferrari)", 55: "Carlos SAINZ (Ferrari)",
    44: "Lewis HAMILTON (Mercedes)", 63: "George RUSSELL (Mercedes)", 
    4: "Lando NORRIS (McLaren)", 81: "Oscar PIASTRI (McLaren)",
    14: "Fernando ALONSO (Aston Martin)", 18: "Lance STROLL (Aston Martin)", 
    10: "Pierre GASLY (Alpine)", 31: "Esteban OCON (Alpine)",
    23: "Alex ALBON (Williams)", 22: "Yuki TSUNODA (RB)", 
    27: "Nico HULKENBERG (Haas)"
}

# 2. REQUISIÇÃO PROTEGIDA CONTRA ERROS
try:
    dados_status = None
    dados_grid = None
    
    with st.spinner("Conectando com o centro de dados da F1..."):
        # Requisição segura de Status da pista
        url_status = "https://openf1.org"
        res_status = requests.get(url_status, params={"session_key": id_sessao}, timeout=5)
        if res_status.status_code == 200 and "application/json" in res_status.headers.get("Content-Type", ""):
            dados_status = res_status.json()
        
        # Requisição segura dos Intervalos de grid
        url_grid = "https://api.openf1.org/v1/intervals"
        res_grid = requests.get(url_grid, params={"session_key": id_sessao}, timeout=5)
        if res_grid.status_code == 200 and "application/json" in res_grid.headers.get("Content-Type", ""):
            dados_grid = res_grid.json()

    # --- RENDERIZAÇÃO NA TELA ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚩 STATUS DA PISTA")
        if dados_status and len(dados_status) > 0:
            ultima_bandeira = dados_status[-1].get('flag', 'PISTA LIMPA')
            if ultima_bandeira == "RED": st.error("🔴 BANDEIRA VERMELHA (Sessão Suspensa)")
            elif ultima_bandeira == "YELLOW": st.warning("🟡 BANDEIRA AMARELA (Atenção)")
            elif ultima_bandeira == "GREEN": st.success("🟢 BANDEIRA VERDE (Pista Livre)")
            else: st.info(f"⚪ STATUS: {ultima_bandeira}")
        else:
            st.info("⚪ STATUS: SINAL INSTÁVEL / SEM INCIDENTES")

    with col2:
        st.subheader("⚡ LINK DA CORRIDA")
        st.code(f"Session Key Ativa: {id_sessao}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 CLASSIFICAÇÃO / INTERVALOS DOS PILOTOS")

    if dados_grid and len(dados_grid) > 0:
        df_bruto = pd.DataFrame(dados_grid)
        df_ultimos = df_bruto.sort_values('date').groupby('driver_number').last().reset_index()
        df_ultimos['Piloto'] = df_ultimos['driver_number'].map(drivers_map).fillna(df_ultimos['driver_number'].apply(lambda x: f"Piloto #{x}"))
        
        df_ultimos['gap_num'] = pd.to_numeric(df_ultimos['gap_to_leader'], errors='coerce').fillna(0)
        df_final = df_ultimos.sort_values('gap_num')
        
        tabela_exibicao = pd.DataFrame({
            "Piloto": df_final['Piloto'],
            "Gap para o Líder": df_final['gap_to_leader'].apply(lambda x: "LÍDER" if pd.isna(x) or x == "" or str(x) == "0" else f"+{x}s"),
            "Intervalo p/ Frente": df_final['interval'].apply(lambda x: "---" if pd.isna(x) or x == "" else f"+{x}s")
        }).reset_index(drop=True)
        
        tabela_exibicao.index = tabela_exibicao.index + 1
        st.dataframe(tabela_exibicao, use_container_width=True)
    else:
        # Se o endpoint de intervalos falhar, avisa sem derrubar o app
        st.warning("⚠️ Servidor OpenF1 instável ou sem dados de voltas salvos para este circuito no momento. Tente trocar de GP ou clicar em 'Forçar Atualização'.")

except Exception as e:
    st.error("📡 O servidor oficial da F1 recusou o pacote de telemetria por excesso de tráfego. Por favor, toque no botão 'Forçar Atualização' acima.")
