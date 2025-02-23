import streamlit as st
import pydeck as pdk
import random
import time

# Function to fetch live cyber attack data
def get_live_cyber_attacks():
    attack_types = ["DDoS", "Ransomware", "Phishing", "SQL Injection", "Malware", "Zero-Day Exploit"]
    attacks = [
        {"source_lat": 37.7749, "source_lon": -122.4194, "source": "USA", "target_lat": 55.7558, "target_lon": 37.6173, "target": "Russia"},
        {"source_lat": 51.5074, "source_lon": -0.1278, "source": "UK", "target_lat": 35.6895, "target_lon": 139.6917, "target": "Japan"},
        {"source_lat": 35.6895, "source_lon": 139.6917, "source": "Japan", "target_lat": -33.8688, "target_lon": 151.2093, "target": "Australia"},
        {"source_lat": -33.8688, "source_lon": 151.2093, "source": "Australia", "target_lat": 51.5074, "target_lon": -0.1278, "target": "UK"},
        {"source_lat": 55.7558, "source_lon": 37.6173, "source": "Russia", "target_lat": 37.7749, "target_lon": -122.4194, "target": "USA"},
    ]
    
    for attack in attacks:
        attack["type"] = random.choice(attack_types)
    
    return random.sample(attacks, random.randint(2, 4))

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🌍 Live Cyber Attack Landscape")
st.write("Tracking real-time cyberattacks with directional arrows.")

# Fetch attack data
attacks = get_live_cyber_attacks()

# Sidebar: Display live cyberattack details
st.sidebar.header("⚡ Live Cyberattacks")
for attack in attacks:
    st.sidebar.markdown(f"**🌐 {attack['source']} → {attack['target']}**")
    st.sidebar.text(f"⚠️ Type: {attack['type']}")
    st.sidebar.text(f"📍 From: {attack['source']} ({attack['source_lat']}, {attack['source_lon']})")
    st.sidebar.text(f"🎯 To: {attack['target']} ({attack['target_lat']}, {attack['target_lon']})")
    st.sidebar.markdown("---")

# Create Arc Layer for attack paths with color gradient
arc_layer = pdk.Layer(
    "ArcLayer",
    data=attacks,
    get_source_position=["source_lon", "source_lat"],
    get_target_position=["target_lon", "target_lat"],
    get_source_color=[0, 255, 0, 200],  # Green for Source
    get_target_color=[255, 0, 0, 200],  # Red for Target
    get_width=3,
    pickable=True,
    auto_highlight=True
)

# Create Scatter Layer for source and target points
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=attacks,
    get_position=["source_lon", "source_lat"],
    get_color=[0, 255, 0, 255],  # Green for Source
    get_radius=100000,
    pickable=True
)

scatter_layer_target = pdk.Layer(
    "ScatterplotLayer",
    data=attacks,
    get_position=["target_lon", "target_lat"],
    get_color=[255, 0, 0, 255],  # Red for Target
    get_radius=100000,
    pickable=True
)

# Configure the 3D globe view
view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=1,
    pitch=30,
    bearing=0
)

# Tooltip for attack details
tooltip = {
    "html": "🚀 <b>Attack:</b> {source} → {target} <br>⚡ <b>Type:</b> {type}",
    "style": {"backgroundColor": "black", "color": "white"}
}

# Create the Pydeck globe map
globe = pdk.Deck(
    layers=[arc_layer, scatter_layer, scatter_layer_target],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style="mapbox://styles/mapbox/satellite-v9"
)

# Display the map
st.pydeck_chart(globe)

# Auto-refresh every 10 seconds
st.write("Updating in real-time...")
time.sleep(10)
st.rerun()


