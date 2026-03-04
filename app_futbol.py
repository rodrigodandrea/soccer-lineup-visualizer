import streamlit as st
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# App Configuration
st.set_page_config(page_title="Soccer Lineup Visualizer", layout="wide")

st.title("⚽ Soccer Lineup Visualizer")
st.markdown("Enter the names and select a formation to see your team on the pitch.")

# 1. Sidebar for Team Selection
st.sidebar.header("Team Settings")
formation = st.sidebar.selectbox("Select Formation", ["4-4-2", "4-3-3", "3-5-2", "4-1-2-2-1"])

# 2. Player Input Logic
st.subheader("Player Roster")
col1, col2 = st.columns(2)

players = []
with col1:
    for i in range(1, 10):
        name = st.text_input(f"Position {i}", f"Player {i}")
        players.append(name)
with col2:
    for i in range(10, 20):
        name = st.text_input(f"Position {i}", f"Player {i}")
        players.append(name)


def get_positions(form):
    # 1. Definimos las coordenadas fijas del campo
    # x: 0-120 (0 meta propia, 120 meta rival)
    # y: 0-80 (0 arriba, 80 abajo)
COORDS = {
    'GK': (10, 40),
    'RB': (30, 70), 'RCB': (30, 50), 'LCB': (30, 30), 'LB': (30, 10),
    'RWB': (45, 70), 'LWB': (45, 10),
    'CDM': (50, 40), 'RCM': (65, 55), 'LCM': (65, 25), 'CAM': (85, 40),
    'RW': (100, 70), 'ST': (110, 40), 'LW': (100, 10),
    'RS': (105, 55), 'LS': (105, 25)
}

# 2. Definimos qué posiciones usa cada formación
FORMATIONS = {
    "4-4-2": ['GK', 'RB', 'RCB', 'LCB', 'LB', 'RCM', 'LCM', 'RWB', 'LWB', 'RS', 'LS'],
    "4-3-3": ['GK', 'RB', 'RCB', 'LCB', 'LB', 'CDM', 'RCM', 'LCM', 'RW', 'ST', 'LW'],
    "3-5-2": ['GK', 'RCB', 'LCB', 'CDM', 'RWB', 'LWB', 'RCM', 'LCM', 'CAM', 'RS', 'LS'],
    "4-1-2-2-1": ['GK', 'RB', 'RCB', 'LCB', 'LB', 'CMD', 'RCM', 'LCM', 'RW', 'LW', 'ST']
}

# 3. En la parte de la carga de jugadores (Input)
st.subheader("Matchday Lineup")
col1, col2 = st.columns(2)
active_positions = FORMATIONS[form]
player_data = {}

for i, pos_name in enumerate(active_positions):
    with col1 if i < 6 else col2:
        name = st.text_input(f"{pos_name} Name", f"Player {i+1}")
        player_data[pos_name] = name

# 4. En la parte del dibujo (Generar vista)
if st.button("Generate Tactical View"):
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(12, 8))
    
    for pos_name, player_name in player_data.items():
        x, y = COORDS[pos_name]
        # Dibujamos el círculo
        pitch.scatter(x, y, s=800, c='#e21017', edgecolors='#ffffff', ax=ax)
        # Nombre del jugador
        pitch.annotate(player_name, xy=(x, y + 5), c='white', va='center', ha='center', size=11, ax=ax)
        # Sigla de la posición o número
        pitch.annotate(pos_name, xy=(x, y), c='white', va='center', ha='center', size=8, weight='bold', ax=ax)
    
    st.pyplot(fig)
