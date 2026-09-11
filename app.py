import streamlit as st
import requests
import pandas as pd

# Configuração de Página Limpa e Escura
st.set_page_config(page_title="F1 Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: #FF1801; margin-bottom: 5px;'>🏎️ F1 DASHBOARD TELEMETRIA</h1>", unsafe_allow_html=True)

# 1. BUSCA AS SESSÕES (Filtro leve direto por Python)
@st.cache_data(ttl=60)
def carregar_gps():
    try:
        # Puxa apenas as últimas 40 sessões para não travar o app
        url = "https://api.openf1.org/v1/sessions"
        r = requests.get(url, timeout=5).json()
        opcoes = {}
        for s in r[::-1]:
            if s.get('session_key') and s.get('location'):
                nome = f"📍 {s.get('location')} ({s.get('year')}) - {s.get('session_name')}"
                if nome not in opcoes and len(opcoes) < 40:
                    opcoes[nome] = str(s.get('session_key'))
        return opcoes
    except:
        return {"GP de Mônaco (2024) - Race": "9523"}

dicionario_gps = carregar_gps()
selecionado = st.selectbox("🏁 Escolha o Grande Prêmio:", list(dicionario_gps.keys()))
id_sessao = dicionario_gps[selecionado]

# Botão manual para forçar a atualização dos dados se necessário
if st.button("🔄 Atualizar Dados da Pista"):
    st.cache_data.clear()

st.markdown("---")

# Mapeamento oficial dos pilotos
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

# 2. REQUISIÇÃO DIRETA DOS DADOS (Sem JavaScript complexo)
try:
    with st.spinner("Buscando dados no servidor da F1..."):
        # Puxa o status mais recente da pista
        url_status = f"https://openf1.org{id_sessao}"
        dados_status = requests.get(url_status, timeout=5).json()
        
        # Puxa a tabela de posições/gaps
        url_grid = f"https://openf1.org{id_sessao}"
        dados_grid = requests.get(url_grid, timeout=5).json()

    # --- EXIBIÇÃO DO STATUS DA PISTA ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚩 STATUS DA PISTA")
        if dados_status:
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
        st.code(f"ID Único da Corrida (Session Key): {id_sessao}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 CLASSIFICAÇÃO / INTERVALOS DOS PILOTOS")

    # --- PROCESSAMENTO DA TABELA DE INTERVALOS ---
    if dados_grid:
        # Consolida o último registro de cada piloto
        df_bruto = pd.DataFrame(dados_grid)
        df_ultimos = df_bruto.sort_values('date').groupby('driver_number').last().reset_index()
        
        # Aplica os nomes reais dos pilotos
        df_ultimos['Piloto'] = df_ultimos['driver_number'].map(drivers_map).fillna(df_ultimos['driver_number'].apply(lambda x: f"Piloto #{x}"))
        
        # Organiza por quem está mais perto do líder (menor gap)
        df_ultimos['gap_num'] = pd.to_numeric(df_ultimos['gap_to_leader'], errors='coerce').fillna(0)
        df_final = df_ultimos.sort_values('gap_num')
        
        # Formata os dados para exibição final elegante
        tabela_exibicao = pd.DataFrame({
            "Piloto": df_final['Piloto'],
            "Gap para o Líder": df_final['gap_to_leader'].apply(lambda x: "LÍDER" if pd.isna(x) or x == "" else f"+{x}s"),
            "Intervalo p/ Carro da Frente": df_final['interval'].apply(lambda x: "---" if pd.isna(x) or x == "" else f"+{x}s")
        }).reset_index(drop=True)
        
        # Ajusta o índice para começar da Posição 1
        tabela_exibicao.index = tabela_exibicao.index + 1
        
        # Desenha a tabela nativa do Streamlit na tela do Tablet
        st.dataframe(tabela_exibicao, use_container_width=True)
    else:
        st.warning("⚠️ Não há dados de voltas salvos para este treino/corrida selecionado.")

except Exception as erro:
    st.error(f"Erro de comunicação com a API F1. Detalhes: {erro}")
