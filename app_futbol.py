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
            'GK': 'GK', 'RB': 'RB', 'RCB': 'RCB', 'LCB': 'LCB', 'LB': 'LB', 
            'CDM': 'CDM', 'RCM': 'RCM', 'LCM': 'LCM', 'RW': 'RW', 'ST': 'ST', 'LW': 'LW',
            'CAM': 'CAM', 'RWB': 'RWB', 'LWB': 'LWB', 'RS': 'RS', 'LS': 'LS'
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
            'GK': 'ARQ', 'RB': '4', 'RCB': '2', 'LCB': '6', 'LB': '3', 
            'CDM': '5', 'RCM': '8', 'LCM': '10', 'RW': '7', 'ST': '9', 'LW': '11',
            'CAM': '5', 'RWB': '4', 'LWB': '3', 'RS': '9', 'LS': '7'
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
formation = st.sidebar.selectbox(texts['form_sel'], ["4-4-2", "4-3-3", "3-5-2", "4-1-2-2-1"])

# COORDENADAS FIJAS
COORDS = {
    'GK': (10, 40), 'RB': (30, 70), 'RCB': (30, 50), 'LCB': (30, 30), 'LB': (30, 10),
    'RWB': (45, 70), 'LWB': (45, 10), 'CDM': (50, 40), 'RCM': (65, 55), 'LCM': (65, 25), 
    'CAM': (85, 40), 'RW': (100, 70), 'ST': (110, 40), 'LW': (100, 10),
    'RS': (105, 55), 'LS': (105, 25)
}

# DEFINICIÓN DE FORMACIONES
FORMATIONS = {
    "4-4-2": ['GK', 'RB', 'RCB', 'LCB', 'LB', 'RCM', 'LCM', 'RWB', 'LWB', 'RS', 'LS'],
    "4-3-3": ['GK', 'RB', 'RCB', 'LCB', 'LB', 'CDM', 'RCM', 'LCM', 'RW', 'ST', 'LW'],
    "3-5-2": ['GK', 'RCB', 'LCB', 'CDM', 'RWB', 'LWB', 'RCM', 'LCM', 'CAM', 'RS', 'LS'],
    "4-1-2-2-1": ['GK', 'RB', 'RCB', 'LCB', 'LB', 'CDM', 'RCM', 'LCM', 'RW', 'LW', 'ST']
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
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#2b3d2b', line_color='#c7d5cc', stripe=True)
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
