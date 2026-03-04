import streamlit as st
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# 0. DICCIONARIO DE IDIOMAS (Configuración)
languages = {
    'English': {
        'title': "⚽ Soccer Lineup Visualizer",
        'desc': "Enter player names and choose your tactical layout.",
        'settings': "Team Settings",
        'lang_sel': "Select Language",
        'form_sel': "Select Formation",
        'roster': "Matchday Roster",
        'btn': "Generate Tactical View",
        'pos_names': {
            'ARQUERO': 'GK', 
            'LATERAL_DERECHO': 'RB', 'CENTRAL_DERECHO': 'RCB', 'CENTRAL_IZQUIERDO': 'LCB', 'LATERAL_IZQUIERDO': 'LB', # linea de 4 
            'DEFENSOR_DERECHO_CENTRAL': 'RWB', 'DEFENSOR_IZQUIERDO_CENTRAL': 'LWB', 'DEFENSOR_CENTRAL': 'CB', # linea de 3
            'MEDIO_CENTRO_DEFENSIVO': 'CDM', 'VOLANTE_OFENSIVO_DERECHO': 'CAMR', 'VOLANTE_OFENSIVO_IZQUIERO': 'CAML', # medio con 3
            'VOLANTE_LATERAL_DERECHO': 'RCM', 'VOLANTE_LATERAL_IZQUIERDO': 'LCM', 'VOLANTE_CENTRO_DERECHA': 'CM',
            'PUNTERO_DERECHO': 'RW', 'PUNTERO_IZQUIERDO': 'LW', 'DELANTERO_CENTRO': 'ST',
            'DELANTERO_IZQUIERDO': 'LS',  'DELANTERO_DERECHO': 'RS'
        }
    },
    'Español': {
        'title': "⚽ Visualizador de Tácticas",
        'desc': "Ingresá los nombres de los jugadores y armá tu esquema.",
        'settings': "Configuración de Equipo",
        'lang_sel': "Elegir Idioma",
        'form_sel': "Elegir Formación",
        'roster': "Plantilla del Partido",
        'btn': "Generar Vista Táctica",
        'pos_names': {
            'ARQUERO': 'ARQ', 
            'LATERAL_DERECHO': '4', 'CENTRAL_DERECHO': '2', 'CENTRAL_IZQUIERDO': '6', 'LATERAL_IZQUIERDO': '3', # linea de 4 
            'DEFENSOR_DERECHO_CENTRAL': '4', 'DEFENSOR_IZQUIERDO_CENTRAL': '3', 'DEFENSOR_CENTRAL': '2', # linea de 3
            'MEDIO_CENTRO_DEFENSIVO': '5', 'VOLANTE_OFENSIVO_DERECHO': '8', 'VOLANTE_OFENSIVO_IZQUIERO': '10', # medio con 3
            'VOLANTE_LATERAL_DERECHO': '8', 'VOLANTE_LATERAL_IZQUIERDO': '11', 'VOLANTE_CENTRO_DERECHA': '5',
            'PUNTERO_DERECHO': '7', 'PUNTERO_IZQUIERDO': '11', 'DELANTERO_CENTRO': '9',
            'DELANTERO_IZQUIERDO': '9',  'DELANTERO_DERECHO': '7'
        }
    }
}

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Soccer Lineup", layout="wide")

# 1. SELECTOR DE IDIOMA
lang_choice = st.sidebar.selectbox("Language / Idioma", ["Español", "English"])
texts = languages[lang_choice]

st.title(texts['title'])
st.markdown(texts['desc'])

# 2. SELECTOR DE FORMACIÓN
st.sidebar.header(texts['settings'])
formation = st.sidebar.selectbox(texts['form_sel'], ["4-4-2", "3-5-2", "4-1-2-2-1"])

# COORDENADAS FIJAS
COORDS = {
    'ARQUERO': (5, 40), 'LATERAL_DERECHO': (25, 70), 'CENTRAL_DERECHO': (25, 50), 'CENTRAL_IZQUIERDO': (25, 30), 'LATERAL_IZQUIERDO': (25, 10),
    'DEFENSOR_DERECHO_CENTRAL': (25, 60), 'DEFENSOR_IZQUIERDO_CENTRAL': (25, 20), 'DEFENSOR_CENTRAL': (25, 40),
    'MEDIO_CENTRO_DEFENSIVO': (40, 40),  'VOLANTE_OFENSIVO_DERECHO': (55, 53), 'VOLANTE_OFENSIVO_IZQUIERO': (55, 27), 
    'VOLANTE_LATERAL_DERECHO': (55, 70), 'VOLANTE_LATERAL_IZQUIERDO': (55, 10), 'VOLANTE_CENTRO_DERECHA': (55, 50),
    'PUNTERO_DERECHO': (65, 70), 'DELANTERO_CENTRO': (75, 40), 'PUNTERO_IZQUIERDO': (65, 10),
    'DELANTERO_DERECHO': (80, 55), 'DELANTERO_IZQUIERDO': (80, 25)
}

# DEFINICIÓN DE FORMACIONES
FORMATIONS = {
    "4-4-2": ['ARQUERO', 
              'LATERAL_DERECHO', 'CENTRAL_DERECHO', 'CENTRAL_IZQUIERDO', 'LATERAL_IZQUIERDO', 
              'VOLANTE_LATERAL_DERECHO', 'VOLANTE_CENTRO_DERECHA', 'VOLANTE_OFENSIVO_IZQUIERO', 'VOLANTE_LATERAL_IZQUIERDO', 
              'DELANTERO_DERECHO', 'DELANTERO_IZQUIERDO'],
    "3-5-2": ['ARQUERO', 
              'DEFENSOR_DERECHO_CENTRAL', 'DEFENSOR_IZQUIERDO_CENTRAL', 'DEFENSOR_CENTRAL',
              'VOLANTE_LATERAL_DERECHO', 'VOLANTE_CENTRO_DERECHA', 'MEDIO_CENTRO_DEFENSIVO', 'VOLANTE_OFENSIVO_IZQUIERO', 'VOLANTE_LATERAL_IZQUIERDO', 
              'DELANTERO_DERECHO', 'DELANTERO_IZQUIERDO'],
    "4-1-2-2-1": ['ARQUERO', 
              'LATERAL_DERECHO', 'CENTRAL_DERECHO', 'CENTRAL_IZQUIERDO', 'LATERAL_IZQUIERDO', 
              'VOLANTE_CENTRO_DERECHA', 'MEDIO_CENTRO_DEFENSIVO', 'VOLANTE_OFENSIVO_IZQUIERO',
              'PUNTERO_DERECHO', 'DELANTERO_CENTRO', 'PUNTERO_IZQUIERDO']
}

# 3. INPUT DE JUGADORES
st.subheader(texts['roster'])
col1, col2 = st.columns(2)
active_positions = FORMATIONS[formation]
player_data = {}

for i, pos_key in enumerate(active_positions):
    translated_pos = texts['pos_names'].get(pos_key, pos_key)
    with col1 if i < 6 else col2:
        name = st.text_input(f"{translated_pos}", f"Player {i+1}", key=f"in_{pos_key}")
        player_data[pos_key] = name

# 4. GENERAR VISTA
if st.button(texts['btn']):
    # Creamos la cancha con estilo profesional (oscuro)
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#2b3d2b', line_color='#c7d5cc', stripe=False)
    fig, ax = pitch.draw(figsize=(12, 8))
    fig.set_facecolor('#2b3d2b')
    
    for pos_key, player_name in player_data.items():
        if pos_key in COORDS:
            x, y = COORDS[pos_key]
            translated_pos = texts['pos_names'].get(pos_key, pos_key)
            
            # Dibujamos el círculo (la camiseta)
            pitch.scatter(x, y, s=1100, c='#e21017', edgecolors='white', linewidth=2, ax=ax, zorder=3)
            
            # Nombre del Jugador
            pitch.annotate(player_name.upper(), xy=(x, y + 6), c='white', va='center', ha='center', 
                           size=12, weight='bold', ax=ax)
            
            # Posición (Número/Sigla) dentro del círculo
            pitch.annotate(translated_pos, xy=(x, y), c='white', va='center', ha='center', 
                           size=10, weight='bold', ax=ax, zorder=4)
    
    st.pyplot(fig)
