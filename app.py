import streamlit as st
import requests
import pandas as pd

# Configuração de Página Limpa e Escura
st.set_page_config(page_title="F1 Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: #FF1801; margin-bottom: 5px;'>🏎️ F1 DASHBOARD TELEMETRIA</h1>", unsafe_allow_html=True)

# 1. BUSCA AS SESSÕES (Filtrando apenas anos anteriores para ter dados reais)
@st.cache_data(ttl=60)
def carregar_gps():
    try:
        url = "https://openf1.org"
        r = requests.get(url, timeout=5).json()
        opcoes = {}
        
        # Varre a lista de trás para frente para pegar os GPs mais recentes
        for s in r[::-1]:
            ano = s.get('year')
            # BLOQUEIA 2026 temporariamente para focar nos GPs que possuem dados salvos (2024/2023)
            if ano and int(ano) < 2026:
                nome = f"📍 {s.get('location')} ({ano}) - {s.get('session_name')}"
                if nome not in opcoes and len(opcoes) < 30:
                    opcoes[nome] = str(s.get('session_key'))
                    
        if opcoes:
            return opcoes
    except:
        pass
    # GP de segurança caso o servidor caia
    return {"📍 Monaco (2024) - Race": "9523"}

dicionario_gps = carregar_gps()
selecionado = st.selectbox("🏁 Escolha o Grande Prêmio (Históricos com Dados Ativos):", list(dicionario_gps.keys()))
id_sessao = dicionario_gps[selecionado]

# Botão para limpar o cache caso precise forçar atualização
if st.button("🔄 Resetar e Atualizar Lista"):
    st.cache_data.clear()
    st.rerun()

st.markdown("---")

# Mapeamento oficial dos pilotos reais
drivers_map = {
    1: "Max VERSTAPPEN (Red Bull)", 11: "Sergio PEREZ (Red Bull)", 
    16: "Charles LECLERC (Ferrari)", 55: "Carlos SAINZ (Ferrari)",
    44: "Lewis HAMILTON (Mercedes)", 63: "George RUSSELL (Mercedes)", 
    4: "Lando NORRIS (McLaren)", 81: "Oscar PIASTRI (McLaren)",
    14: "Fernando ALONSO (Aston Martin)", 18: "Lance STROLL (Aston Martin)", 
    10: "Pierre GASLY (Alpine)", 31: "Esteban OCON (Alpine)",
    23: "Alex ALBON (Williams)", 22: "Yuki TSUNODA (RB)", 
    27: "Nico HULKENBERG (Haas)", 30: "Liam LAWSON (RB)",
    38: "Oliver BEARMAN (Ferrari)", 43: "Franco COLAPINTO (Williams)"
}

# 2. REQUISIÇÃO CORRIGIDA (Com parâmetros separados para evitar erro na URL)
try:
    with st.spinner("Buscando dados consolidados na API da F1..."):
        # Requisição de Status da pista
        url_status = "https://openf1.org"
        params_status = {"session_key": id_sessao}
        dados_status = requests.get(url_status, params=params_status, timeout=5).json()
        
        # Requisição dos Intervalos
        url_grid = "https://openf1.org"
        params_grid = {"session_key": id_sessao}
        dados_grid = requests.get(url_grid, params=params_grid, timeout=5).json()

    # --- EXIBIÇÃO DOS PAINÉIS DE STATUS ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚩 STATUS DA PISTA")
        if dados_status and len(dados_status) > 0:
            ultima_bandeira = dados_status[-1].get('flag', 'PISTA LIMPA')
            if ultima_bandeira == "RED":
                st.error("🔴 BANDEIRA VERMELHA (Sessão Suspensa)")
            elif ultima_bandeira == "YELLOW":
                st.warning("🟡 BANDEIRA AMARELA (Atenção na pista)")
            elif ultima_bandeira == "GREEN":
                st.success("🟢 BANDEIRA VERDE (Pista Livre)")
            else:
                st.info(f"⚪ STATUS: {ultima_bandeira}")
        else:
            st.info("⚪ STATUS: PISTA LIMPA / CONCLUÍDA")

    with col2:
        st.subheader("⚡ SESSÃO CONECTADA")
        st.code(f"Session Key Ativa: {id_sessao}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 CLASSIFICAÇÃO / INTERVALOS DOS PILOTOS")

    # --- MONTAGEM DA TABELA DE CLASSIFICAÇÃO ---
    if dados_grid and len(dados_grid) > 0:
        df_bruto = pd.DataFrame(dados_grid)
        
        # Agrupa pelo número do piloto e pega o último registro de tempo dele
        df_ultimos = df_bruto.sort_values('date').groupby('driver_number').last().reset_index()
        
        # Traduz o número para o nome real do piloto
        df_ultimos['Piloto'] = df_ultimos['driver_number'].map(drivers_map).fillna(df_ultimos['driver_number'].apply(lambda x: f"Piloto #{x}"))
        
        # Organiza a tabela por proximidade do líder
        df_ultimos['gap_num'] = pd.to_numeric(df_ultimos['gap_to_leader'], errors='coerce').fillna(0)
        df_final = df_ultimos.sort_values('gap_num')
        
        # Monta a estrutura visual final
        tabela_exibicao = pd.DataFrame({
            "Piloto": df_final['Piloto'],
            "Gap para o Líder": df_final['gap_to_leader'].apply(lambda x: "LÍDER" if pd.isna(x) or x == "" or str(x) == "0" else f"+{x}s"),
            "Intervalo p/ Carro da Frente": df_final['interval'].apply(lambda x: "---" if pd.isna(x) or x == "" else f"+{x}s")
        }).reset_index(drop=True)
        
        # Ajusta posições começando em 1
        tabela_exibicao.index = tabela_exibicao.index + 1
        
        # Mostra a tabela na tela do tablet
        st.dataframe(tabela_exibicao, use_container_width=True)
    else:
        st.warning("⚠️ Não há dados de voltas salvos para esta sessão específica.")

except Exception as erro:
    st.error(f"Erro ao processar dados. Detalhes: {erro}")
