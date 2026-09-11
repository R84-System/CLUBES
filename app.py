import streamlit as st
import requests
import pandas as pd

# Configuração de Página Limpa e Escura para o tablet
st.set_page_config(page_title="F1 Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: #FF1801; margin-bottom: 5px;'>🏎️ F1 DASHBOARD TELEMETRIA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; margin-top: 0px;'>Campeonato de 2026 — Dados Oficiais Completos</p>", unsafe_allow_html=True)

# 1. BUSCA AS SESSÕES (Filtra estritamente as corridas de 2026)
@st.cache_data(ttl=120)
def carregar_gps_2026():
    try:
        url = "https://openf1.org"
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200 and "application/json" in resposta.headers.get("Content-Type", ""):
            r = resposta.json()
            opcoes = {}
            for s in r[::-1]:
                ano = s.get('year')
                if ano and int(ano) == 2026:
                    nome = f"📍 {s.get('location')} ({ano}) - {s.get('session_name')}"
                    if nome not in opcoes:
                        opcoes[nome] = str(s.get('session_key'))
            if opcoes:
                return opcoes
    except:
        pass
    return {"📍 Monza (2026) - Race": "11361", "📍 Spa-Francorchamps (2026) - Race": "9577"}

dicionario_gps = carregar_gps_2026()
selecionado = st.selectbox("🏁 Escolha o Grande Prêmio de 2026:", list(dicionario_gps.keys()))
id_sessao = dicionario_gps[selecionado]

if st.button("🔄 Forçar Atualização do Sinal"):
    st.cache_data.clear()
    st.rerun()

st.markdown("---")

# 2. BUSCA OS NOMES REAIS DOS PILOTOS NA API
@st.cache_data(ttl=300)
def buscar_nomes_pilotos(session_key):
    mapeamento = {}
    try:
        url = f"https://openf1.org{session_key}"
        resposta = requests.get(url, timeout=5).json()
        for d in resposta:
            num = d.get('driver_number')
            nome_completo = d.get('full_name', f"Piloto #{num}")
            equipe = d.get('team_name', '')
            mapeamento[num] = f"{nome_completo} ({equipe})" if equipe else nome_completo
    except:
        pass
    return mapeamento

# 3. REQUISIÇÃO HISTÓRICA E LIVE COMBINADA
try:
    dados_status = None
    dados_grid = None
    
    with st.spinner("Puxando telemetria do banco de dados oficial..."):
        drivers_map = buscar_nomes_pilotos(id_sessao)

        # Status da pista
        try:
            url_status = "https://openf1.org"
            res_status = requests.get(url_status, params={"session_key": id_sessao}, timeout=5)
            if res_status.status_code == 200: dados_status = res_status.json()
        except: pass
        
        # Busca Ampla de Posições (Remove o modo streaming para ler históricos finalizados)
        try:
            url_grid = "https://openf1.org"
            res_grid = requests.get(url_grid, params={"session_key": id_sessao}, timeout=5)
            if res_grid.status_code == 200: dados_grid = res_grid.json()
        except: pass

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
            st.info("🟢 STATUS: SESSÃO CONCLUÍDA")

    with col2:
        st.subheader("⚡ LINK DA CORRIDA")
        st.code(f"Session Key Ativa: {id_sessao}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 CLASSIFICAÇÃO / INTERVALOS DOS PILOTOS")

    if dados_grid and len(dados_grid) > 0:
        df_bruto = pd.DataFrame(dados_grid)
        
        # Consolida o grid final organizando pela última atualização estável
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
        st.warning("⚠️ O servidor do OpenF1 limpou os logs em tempo real desta sessão. Tente outro GP de 2026 no menu para validar.")

except Exception as e:
    st.error("📡 Erro na rede da F1. Por favor, clique em Forçar Atualização.")
