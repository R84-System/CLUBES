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
    
    st.subheader("Mapa do Circuito e Posição dos Carros")
    
    # Botão para carregar o mapa
    if st.button("Gerar Mapa da Pista"):
        with st.spinner("Baixando dados de localização da pista..."):
            loc_url = f"https://api.openf1.org/v1/location?session_key={session_key}"
            res = requests.get(loc_url)
            
            if res.status_code == 200 and res.json():
                df = pd.DataFrame(res.json())
                
                # Pegamos um piloto de referência para desenhar o traçado do circuito
                sample_driver = df['driver_number'].iloc[0]
                df_track = df[df['driver_number'] == sample_driver]
                
                # Pegamos a última posição registrada de cada piloto para mostrar no mapa
                df_latest = df.sort_values(by='date').groupby('driver_number').tail(1)
                
                # Criando o gráfico com Plotly
                fig = px.scatter(
                    df_track, x='x', y='y',
                    opacity=0.3,
                    title=f"Circuito - {session.get('circuit_short_name')}"
                )
                
                # Adicionando os carros na última posição
                fig.add_scatter(
                    x=df_latest['x'],
                    y=df_latest['y'],
                    mode='markers+text',
                    text=df_latest['driver_number'],
                    textposition="top center",
                    marker=dict(size=12, color='red'),
                    name='Carros'
                )
                
                fig.update_layout(
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    height=600,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Não há dados de localização suficientes para esta sessão no momento.")
else:
    st.warning("Não foi possível carregar a sessão atual da OpenF1.")
