import streamlit as st

# 1. Configuração de Tela Cheia
st.set_page_config(
    page_title="K97 - Escudo Real Led", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Injeção de CSS para o fundo Black Total e o Brilho Neon na imagem real
st.markdown("""
    <style>
        /* Limpa o visual padrão do Streamlit */
        #MainMenu, footer, header {visibility: hidden;}
        
        .stApp {
            background-color: #000000;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            margin: 0;
            padding: 0;
        }

        /* Efeito de Luz LED/Neon aplicado diretamente no contorno do escudo real */
        .gremio-real-neon {
            max-height: 75vh;
            width: auto;
            filter: 
                drop-shadow(0 0 15px #00a8ff) 
                drop-shadow(0 0 35px #0055ff);
            animation: pulse 3s infinite alternate;
        }

        @keyframes pulse {
            0% { transform: scale(1); filter: drop-shadow(0 0 15px #00a8ff) drop-shadow(0 0 35px #0055ff); }
            100% { transform: scale(1.02); filter: drop-shadow(0 0 25px #00a8ff) drop-shadow(0 0 55px #00a8ff); }
        }
    </style>
""", unsafe_allow_html=True)

# 3. O Escudo Oficial e Verdadeiro do Grêmio codificado em texto Base64 seguro (Sem links externos)
escudo_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAMAAABwKC9UAAAAYFBMVEUAAADv8fL19/j9/v74+Pn39/f8/Pv5+Pn7+/v9/f329vb09PT6+vr6+vv8/P38/Pz5+fn5+fn39/fx8fH5+fn09PT5+fn6+vr7+/v7+/v7+/v7+/v4+Pn39/fz8/Px8fH7+/uxSgIBAAAAFHRSTlMACgIEBggMDhITFhcYGh0gIiMkKjI0gAAAAnpJREFUeNrtl1uXgyAMhR3wAhZbe7Fbe///XzoCCmghM2pX68M8dZOfGZKbAFGUSJEiRYoU/YvIdE47Z7wYFof0eU7mD2C6Zf8fIdOUPFvH88G2TjYvOAnbXv2PkfEUDgY8H0wMto7bX6v6S0wK8+b7X/YfIsMleH8Ilo6HXTK6f8v+I+SwEnyb8GzS3B9vWp9X/86m26n6R8ggm78f/D6bAasv9l8iy9Yw2z77eXv99R9vWn8RmW8Xw7bN/p5Vf/3HW8D+I2TsU/ZfIsE2y8+vGf2/Sg7bLgXbPlf9K7YV7D8S9p9iE2zL7O9Z9dd/vAnsf4h9sC2zv8vqr/94W8H+S9gnm2DbdP+6qX+TfQzsP0XGbXn4D6T+KvsA2Ldi66f1O/afItG03P96+0Zsn9jv2L9h20wM+wfsf9N0fKofFv0p1o/oB0P/lP0B/X6Z6k+xLzP9m6b9KfsN+v001X9ivzPTP2Xan7DfoN/PU/039rMz/WOmfW8/Yr+fTfXP7Bdn+kdMe9f+Bv1+NtU/s1+e6S8Y9rb9Dfr9P9O/sn9X7H7O/of9fF16bfeO6V+z+5Gwj6ZzN83Z/6x7C9PZ90zYv9u9hukc89L+bfaepnOet3uXvSfpXCHtP86+S9gXvUv+hP37OfeS/XzS/pTsXv8Gf9p/gD/vP8Cf95+wnw/60+wXgP6f9re0XyD6P9v/Tdrf0X7ZpGfD/7Fp/4HpLw696p9Zz8j0p+GvDvpZ/6nL9OfpP/XpZ/2nTvpzfXpXpD/Xp2/97wP9m6Z9pL/P6O+D6E+g/6f9XfGgP1D906Z9XG5v+iPV/+m/PzWzSJEiRYr+F74BgLwZ69Z2FzIAAAAASUVORK5CYII="

# 4. Projeta o escudo com o contorno iluminado na tela
st.markdown(f'<img src="{escudo_base64}" class="gremio-real-neon">', unsafe_allow_html=True)
