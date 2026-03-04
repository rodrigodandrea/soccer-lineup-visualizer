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

# 3. Coordinates logic based on formation
# (x=0 is Goal, x=120 is Opponent Goal | y=0 is Top, y=80 is Bottom)
def get_positions(form):
    pos = {
        "4-4-2": [
            (5, 40), # GK
            (25, 15), (25, 32), (25, 48), (25, 65), # Defense
            (55, 15), (55, 32), (55, 48), (55, 65), # Midfield
            (80, 30), (80, 50) # Attack
        ],
        "4-3-3": [
            (5, 40), # GK
            (25, 15), (25, 32), (25, 48), (25, 65), # Defense
            (55, 25), (55, 40), (55, 55), # Midfield
            (80, 20), (80, 40), (80, 60) # Attack
        ],
        "3-5-2": [
            (5, 40), # GK
            (25, 20), (25, 40), (25, 60), # Defense
            (55, 10), (55, 25), (55, 40), (55, 55), (55, 70), # Midfield
            (80, 30), (80, 50) # Attack
        ],
        "4-1-2-2-1": [
            (5, 40), # GK
            (25, 15), (25, 32), (25, 48), (25, 65), # Defense
            (40, 40), # 5
            (55, 25), (55, 55), # Midfield
            (70, 10), (70, 70), 
            (80, 40) # Attack
        ]
    }
    return pos.get(form)

# 4. Generate Visualization
if st.button("Generate Tactical View"):
    coords = get_positions(formation)
    
    # Draw Pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(12, 8), constrained_layout=True, tight_layout=False)
    fig.set_facecolor('#22312b')

    # Scatter Players and Annotate Names
    for i, (x, y) in enumerate(coords):
        # Draw the jersey/circle
        pitch.scatter(x, y, s=800, c='#e21017', edgecolors='#ffffff', linewidth=2, alpha=1, ax=ax)
        # Add player name
        pitch.annotate(players[i], xy=(x, y + 4), c='white', va='center',
                       ha='center', size=12, weight='bold', ax=ax)
        # Add number
        pitch.annotate(str(i+1), xy=(x, y), c='white', va='center',
                       ha='center', size=10, ax=ax)

    st.pyplot(fig)
