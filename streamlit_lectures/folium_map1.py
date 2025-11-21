import streamlit as st
import folium
from streamlit_folium import folium_static
from streamlit_folium import st_folium

if 'center' not in st.session_state:
    st.session_state.center = [46.903354, 1.888334]
# Initialize session state to store clicked points
if 'location' not in st.session_state:
    st.session_state.location = folium.Marker(st.session_state.center)

# Create a Folium map
m = folium.Map(location=[46.903354, 1.888334], zoom_start=6)
fg = folium.FeatureGroup(name="Markers")
fg.add_child(st.session_state.location)

# When the user interacts with the map
map_state_change = st_folium(
    m,
    feature_group_to_add=fg,
    width=620, height=580,
    returned_objects=['last_clicked'],
    key="folium_map"
)

if map_state_change['last_clicked']:
    loc = map_state_change['last_clicked']
    st.session_state.location = folium.Marker([loc['lat'], loc['lng']])
    fg.clear_layers()  # Clear existing markers
    fg.add_child(st.session_state.location)  # Add the new marker
    folium_static(m)