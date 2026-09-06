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
    
    st.subheader(f"Painel Oficial - {session.get('circuit_short_name')} ({session.get('year')})")
    
    if st.button("Carregar Dados da Sessão (Mapa + Posições)"):
        with st.spinner("Buscando telemetria e posições..."):
            # Requisições em paralelo lógico
            loc_res = requests.get(f"https://api.openf1.org/v1/location?session_key={session_key}")
            pos_res = requests.get(f"https://api.openf1.org/v1/position?session_key={session_key}")
            drv_res = requests.get(f"https://api.openf1.org/v1/drivers?session_key={session_key}")
            
            if loc_res.status_code == 200 and pos_res.status_code == 200:
                loc_data = loc_res.json()
                pos_data = pos_res.json()
                drv_data = drv_res.json() if drv_res.status_code == 200 else []
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### 🗺️ Mapa do Circuito")
                    if loc_data:
                        df_loc = pd.DataFrame(loc_data)
                        sample_driver = df_loc['driver_number'].iloc[0]
                        df_track = df_loc[df_loc['driver_number'] == sample_driver]
                        df_latest_loc = df_loc.sort_values(by='date').groupby('driver_number').tail(1)
                        
                        fig = px.scatter(
                            df_track, x='x', y='y',
                            opacity=0.3,
                            height=550
                        )
                        fig.add_scatter(
                            x=df_latest_loc['x'],
                            y=df_latest_loc['y'],
                            mode='markers+text',
                            text=df_latest_loc['driver_number'],
                            textposition="top center",
                            marker=dict(size=10, color='red'),
                            name='Carros'
                        )
                        fig.update_layout(
                            xaxis=dict(visible=False),
                            yaxis=dict(visible=False),
                            margin=dict(l=0, r=0, t=0, b=0),
                            showlegend=False
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Sem dados de localização.")
                
                with col2:
                    st.markdown("### 📊 Classificação")
                    if pos_data:
                        df_pos = pd.DataFrame(pos_data)
                        df_latest_pos = df_pos.sort_values(by='date').groupby('driver_number').tail(1)
                        
                        if drv_data:
                            df_drv = pd.DataFrame(drv_data)
                            df_table = pd.merge(df_latest_pos, df_drv[['driver_number', 'name_acronym', 'team_name']], on='driver_number', how='left')
                        else:
                            df_table = df_latest_pos
                            
                        # Ordenar por posição se a coluna existir
                        if 'position' in df_table.columns:
                            df_table = df_table.sort_values(by='position')
                            cols_to_show = ['position', 'driver_number', 'name_acronym'] if 'name_acronym' in df_table.columns else ['position', 'driver_number']
                            st.dataframe(df_table[cols_to_show], hide_index=True, use_container_width=True)
                        else:
                            st.dataframe(df_table, use_container_width=True)
                    else:
                        st.warning("Sem dados de posições.")
            else:
                st.error("Erro ao buscar dados da API da OpenF1.")
else:
    st.warning("Não foi possível carregar a sessão atual da OpenF1.")
