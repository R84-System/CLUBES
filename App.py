import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="F1 Live Dashboard", layout="wide")

st.title("🏎️ F1 Live Dashboard - OpenF1")

@st.cache_data(ttl=60)
def get_latest_session():
    url = "https://api.openf1.org/v1/sessions?session_key=latest"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
    return None

session = get_latest_session()

if session:
    st.sidebar.success("Sessão Conectada!")
    st.sidebar.write(f"**Nome:** {session.get('session_name')}")
    st.sidebar.write(f"**Circuito:** {session.get('circuit_short_name')}")
    st.sidebar.write(f"**Ano:** {session.get('year')}")
    
    session_key = session.get('session_key')
    
    st.subheader("Painel de Telemetria")
    st.write(f"Chave da sessão ativa: `{session_key}`")
    
    if st.button("Testar Requisição de Localização"):
        loc_url = f"https://api.openf1.org/v1/location?session_key={session_key}"
        res = requests.get(loc_url)
        if res.status_code == 200:
            loc_data = res.json()
            if loc_data:
                df_loc = pd.DataFrame(loc_data)
                st.success(f"{len(df_loc)} registros de localização encontrados!")
                st.dataframe(df_loc.tail(10))
            else:
                st.info("A API retornou dados vazios para esta sessão (provavelmente a sessão não está ativa no momento).")
        else:
            st.error("Erro ao buscar dados de localização.")
else:
    st.warning("Não foi possível carregar a sessão atual da OpenF1.")
