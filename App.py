import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="F1 Live Dashboard", layout="wide")

st.title("🏎️ F1 Live Dashboard - OpenF1")

@st.cache_data(ttl=300)
def get_sessions():
    url = "https://api.openf1.org/v1/sessions?year=2024"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return pd.DataFrame(res.json())
    except:
        pass
    return pd.DataFrame()

df_sessions = get_sessions()

if not df_sessions.empty:
    st.sidebar.header("Configuração da Sessão")
    
    years = sorted(df_sessions['year'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Ano", years)
    
    df_filtered_year = df_sessions[df_sessions['year'] == selected_year]
    circuit_list = df_filtered_year['circuit_short_name'].unique()
    selected_circuit = st.sidebar.selectbox("Circuito", circuit_list)
    
    df_filtered_circuit = df_filtered_year[df_filtered_year['circuit_short_name'] == selected_circuit]
    session_name_list = df_filtered_circuit['session_name'].unique()
    selected_session_name = st.sidebar.selectbox("Sessão", session_name_list)
    
    session_row = df_filtered_circuit[df_filtered_circuit['session_name'] == selected_session_name].iloc[0]
    session_key = session_row['session_key']
    
    st.sidebar.success(f"Sessão Selecionada: {session_key}")
    
    st.subheader(f"Painel Oficial - {selected_circuit} ({selected_year}) - {selected_session_name}")
    
    if 'loaded_session_key' not in st.session_state:
        st.session_state.loaded_session_key = None

    if st.button("Carregar Dados da Sessão") or st.session_state.loaded_session_key == session_key:
        st.session_state.loaded_session_key = session_key
        
        with st.spinner("Baixando telemetria e posições da API..."):
            loc_res = requests.get(f"https://api.openf1.org/v1/location?session_key={session_key}")
            pos_res = requests.get(f"https://api.openf1.org/v1/position?session_key={session_key}")
            drv_res = requests.get(f"https://api.openf1.org/v1/drivers?session_key={session_key}")
            
            if loc_res.status_code == 200 and pos_res.status_code == 200:
                loc_data = loc_res.json()
                pos_data = pos_res.json()
                drv_data = drv_res.json() if drv_res.status_code == 200 else []
                
                df_loc = pd.DataFrame(loc_data)
                df_loc['date'] = pd.to_datetime(df_loc['date'])
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### 🗺️ Mapa do Circuito Interativo")
                    if not df_loc.empty:
                        sample_driver = df_loc['driver_number'].iloc[0]
                        df_track = df_loc[df_loc['driver_number'] == sample_driver]
                        
                        # Criando um slider de tempo baseado nos registros da pista
                        min_time = df_loc['date'].min()
                        max_time = df_loc['date'].max()
                        
                        # Seletor de momento na sessão
                        selected_time = st.slider(
                            "Arraste para mover os carros na pista:",
                            min_value=min_time.to_pydatetime(),
                            max_value=max_time.to_pydatetime(),
                            value=min_time.to_pydatetime(),
                            format="HH:mm:ss"
                        )
                        
                        # Filtrar posições próximas ao timestamp escolhido (janela de 1 segundo)
                        time_window_end = pd.to_datetime(selected_time) + pd.Timedelta(seconds=1)
                        df_filtered_loc = df_loc[(df_loc['date'] >= pd.to_datetime(selected_time)) & (df_loc['date'] <= time_window_end)]
                        df_current_loc = df_filtered_loc.sort_values(by='date').groupby('driver_number').tail(1)
                        
                        if df_current_loc.empty:
                            df_current_loc = df_loc.sort_values(by='date').groupby('driver_number').tail(1)

                        if drv_data:
                            df_drv = pd.DataFrame(drv_data)
                            df_current_loc = pd.merge(df_current_loc, df_drv[['driver_number', 'name_acronym', 'team_colour']], on='driver_number', how='left')
                            df_current_loc['team_colour'] = df_current_loc['team_colour'].apply(lambda c: f"#{c}" if c and not str(c).startswith('#') else (c if c else "FFFFFF"))
                        else:
                            df_current_loc['name_acronym'] = df_current_loc['driver_number'].astype(str)
                            df_current_loc['team_colour'] = "red"
                        
                        fig = px.scatter(
                            df_track, x='x', y='y',
                            opacity=0.15,
                            height=450
                        )
                        
                        fig.add_scatter(
                            x=df_current_loc['x'],
                            y=df_current_loc['y'],
                            mode='markers+text',
                            text=df_current_loc['name_acronym'],
                            textposition="top center",
                            marker=dict(
                                size=12, 
                                color=df_current_loc['team_colour'] if 'team_colour' in df_current_loc.columns else 'red'
                            ),
                            name='Carros'
                        )
                        
                        fig.update_layout(
                            xaxis=dict(visible=False),
                            yaxis=dict(visible=False),
                            margin=dict(l=0, r=0, t=0, b=0),
                            showlegend=False,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)'
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
                            
                        if 'position' in df_table.columns:
                            df_table = df_table.sort_values(by='position')
                            cols_to_show = ['position', 'driver_number', 'name_acronym', 'team_name'] if 'name_acronym' in df_table.columns else ['position', 'driver_number']
                            st.dataframe(df_table[cols_to_show], hide_index=True, use_container_width=True, height=450)
                        else:
                            st.dataframe(df_table, use_container_width=True, height=450)
                    else:
                        st.warning("Sem dados de posições.")
                
                st.markdown("---")
                st.markdown("### 📈 Telemetria de Velocidade por Piloto")
                if drv_data:
                    df_drv_list = pd.DataFrame(drv_data)
                    driver_options = {f"{row['name_acronym']} (#{row['driver_number']})": row['driver_number'] for _, row in df_drv_list.iterrows()}
                    selected_driver_label = st.selectbox("Selecione um piloto para ver a velocidade:", list(driver_options.keys()))
                    selected_driver_number = driver_options[selected_driver_label]
                    
                    if st.button("Carregar Telemetria do Piloto"):
                        with st.spinner("Buscando dados de velocidade (car_data)..."):
                            car_res = requests.get(f"https://api.openf1.org/v1/car_data?session_key={session_key}&driver_number={selected_driver_number}")
                            if car_res.status_code == 200 and car_res.json():
                                df_car = pd.DataFrame(car_res.json())
                                
                                fig_speed = px.line(
                                    df_car, x='date', y='speed',
                                    title=f"Velocidade ao longo do tempo - Piloto {selected_driver_label}",
                                    labels={'date': 'Tempo', 'speed': 'Velocidade (km/h)'}
                                )
                                fig_speed.update_layout(
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    height=350
                                )
                                st.plotly_chart(fig_speed, use_container_width=True)
                            else:
                                st.info("Não há dados de telemetria de velocidade disponíveis para este piloto nesta sessão.")
            else:
                st.error("Erro ao buscar dados da API da OpenF1.")
else:
    st.error("Não foi possível carregar a lista de sessões da OpenF1.")
