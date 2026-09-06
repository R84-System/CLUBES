import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="F1 Live Telemetry")

st.title("🏎️ F1 Live Telemetry & Circuit Tracker")

# Seletor de Sessão
session_key = st.selectbox("Selecione a Sessão (Meeting / Grand Prix)", ["latest", "9629", "9636"])

# Injetar a Session Key globalmente no JavaScript
st.markdown(f"""
    <script>
        window.sessionKey = "{session_key}";
    </script>
""", unsafe_allow_html=True)

# Layout em Duas Colunas (Esquerda: Mapa com carros andando | Direita: Torre de Tempos)
col_map, col_table = st.columns([1.6, 1.1])

with col_map:
    st.subheader("Mapa do Circuito em Tempo Real")
    # Carregar o arquivo HTML/JS do Tracker
    tracker_html = """
    <div style="background-color: #121214; border-radius: 8px; padding: 10px; border: 1px solid #2e2e38;">
        <canvas id="trackCanvas" style="width: 100%; height: 480px; display: block;"></canvas>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        // Inserir o script compilado aqui ou carregar via static folder
    </script>
    """
    # Alternativa limpa carregando o script JS externo criado acima:
    components.html("""
        <div style="background-color: #121214; border-radius: 8px; padding: 5px; text-align: center;">
            <canvas id="trackCanvas" style="width: 100%; height: 480px;"></canvas>
        </div>
        <script>
            window.sessionKey = '""" + str(session_key) + """';
        </script>
        <script src="http://localhost:8501/app/static/tracker.js"></script>
    """, height=500)

with col_table:
    st.subheader("Torre de Tempos & Pneus")
    # Tabela simulada/padrão F1 com dados da OpenF1
    import pandas as pd
    import requests
    
    try:
        res = requests.get(f"https://api.openf1.org/v1/drivers?session_key={session_key}")
        drivers_data = res.json()
        if drivers_data:
            df_drivers = pd.DataFrame(drivers_data)[['driver_number', 'name_acronym', 'team_name']]
            df_drivers.columns = ['No', 'Piloto', 'Equipe']
            df_drivers['Pneu'] = 'MEDIUM'  # Mock/Integração com Stints
            df_drivers['Gap'] = '+0.000'
            st.dataframe(df_drivers, hide_index=True, use_container_width=True)
        else:
            st.info("Aguardando dados da sessão...")
    except Exception as e:
        st.warning("Carregando telemetria ao vivo...")
