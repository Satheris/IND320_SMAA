# import streamlit as st
# import pydeck as pdk
# import pandas as pd

# # Set page configuration
# st.set_page_config(page_title="Norway Location Picker", layout="wide")

# # Initialize session state
# if "marker_location" not in st.session_state:
#     st.session_state.marker_location = None

# st.title("🇳🇴 Norway Location Picker")
# st.write("Click anywhere on the map to mark a location")

# # Create Pydeck view
# view_state = pdk.ViewState(
#     latitude=64.0,
#     longitude=11.0,
#     zoom=5,
#     pitch=0
# )

# # Create layer for existing marker
# layers = []
# if st.session_state.marker_location is not None:
#     marker_df = pd.DataFrame({
#         'lat': [st.session_state.marker_location[0]],
#         'lon': [st.session_state.marker_location[1]]
#     })
    
#     layers.append(
#         pdk.Layer(
#             'ScatterplotLayer',
#             data=marker_df,
#             get_position=['lon', 'lat'],
#             get_color=[255, 0, 0, 160],
#             get_radius=50000,  # Radius in meters
#             pickable=True
#         )
#     )

# # Create the deck
# deck = pdk.Deck(
#     map_style='mapbox://styles/mapbox/light-v9',
#     initial_view_state=view_state,
#     layers=layers,
#     tooltip={"text": "Lat: {lat}, Lon: {lon}"}
# )

# # Display the map
# deck_result = st.pydeck_chart(deck, use_container_width=False)

# # Pydeck click handling is more reliable
# if deck_result is not None and deck_result.last_clicked:
#     coords = deck_result.last_clicked['coords']
#     st.session_state.marker_location = [coords['lat'], coords['lon']]
#     st.rerun()

# if st.session_state.marker_location is not None:
#     st.success(f"**Selected Coordinates:** {st.session_state.marker_location}")
# else:
#     st.info("No location selected yet. Click on the map to choose a location.")





# import streamlit as st
# import pydeck as pdk
# import pandas as pd

# # Set page configuration
# st.set_page_config(page_title="Norway Location Picker", layout="wide")

# # Initialize session state
# if "marker_location" not in st.session_state:
#     st.session_state.marker_location = None
#     st.session_state.view_state = pdk.ViewState(
#         latitude=64.0,
#         longitude=11.0,
#         zoom=5,
#         pitch=0
#     )

# st.title("🇳🇴 Norway Location Picker")
# st.write("Click anywhere on the map to mark a location")

# # Create layer for existing marker
# layers = []
# if st.session_state.marker_location is not None:
#     marker_df = pd.DataFrame({
#         'lat': [st.session_state.marker_location[0]],
#         'lon': [st.session_state.marker_location[1]]
#     })
    
#     layers.append(
#         pdk.Layer(
#             'ScatterplotLayer',
#             data=marker_df,
#             get_position=['lon', 'lat'],
#             get_color=[255, 0, 0, 160],
#             get_radius=50000,
#             pickable=True
#         )
#     )

# # Create the deck
# deck = pdk.Deck(
#     map_style='mapbox://styles/mapbox/light-v9',
#     initial_view_state=st.session_state.view_state,
#     layers=layers,
#     tooltip={"text": "Lat: {lat}, Lon: {lon}"}
# )

# # Display the map - st.pydeck_chart doesn't return click data in the way we need
# # We'll use a different approach with session state
# st.pydeck_chart(deck, use_container_width=True)

# # Alternative approach: Let's use Streamlit's built-in map for better click handling
# st.subheader("Alternative: Use Streamlit's Native Map")
# st.write("Click on the map below to select a location (more reliable positioning)")

# # Use st.map which has better click handling
# if st.session_state.marker_location is not None:
#     map_data = pd.DataFrame({
#         'lat': [st.session_state.marker_location[0]],
#         'lon': [st.session_state.marker_location[1]]
#     })
# else:
#     map_data = pd.DataFrame({
#         'lat': [64.0],
#         'lon': [11.0]
#     })

# # Display the map
# st.map(map_data, zoom=5)

# # Add manual coordinate input as a reliable fallback
# st.subheader("Manual Coordinate Input")
# col1, col2 = st.columns(2)
# with col1:
#     lat = st.number_input("Latitude", value=st.session_state.marker_location[0] if st.session_state.marker_location else 64.0, format="%.6f")
# with col2:
#     lon = st.number_input("Longitude", value=st.session_state.marker_location[1] if st.session_state.marker_location else 11.0, format="%.6f")

# if st.button("Set Marker at These Coordinates"):
#     st.session_state.marker_location = [lat, lon]
#     st.rerun()

# if st.session_state.marker_location is not None:
#     st.success(f"**Selected Coordinates:** {st.session_state.marker_location}")
# else:
#     st.info("No location selected yet. Use the manual input above.")










import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="Norway Location Picker", layout="wide")

# Initialize session state
if "marker_location" not in st.session_state:
    st.session_state.marker_location = None

st.title("🇳🇴 Norway Location Picker")
st.write("Click anywhere on the map to mark a location")

# Prepare data for the map
if st.session_state.marker_location is not None:
    map_data = pd.DataFrame({
        'lat': [st.session_state.marker_location[0]],
        'lon': [st.session_state.marker_location[1]]
    })
else:
    # Default view of Norway
    map_data = pd.DataFrame({
        'lat': [64.0],
        'lon': [11.0]
    })

# Display the map - Streamlit's native map has better click handling
clicked = st.map(map_data, zoom=5)

# Check if user clicked on the map
if hasattr(clicked, 'last_clicked') and clicked.last_clicked:
    lat = clicked.last_clicked['lat']
    lon = clicked.last_clicked['lng']
    st.session_state.marker_location = [lat, lon]
    st.rerun()

# Manual coordinate input as backup
st.subheader("Manual Coordinate Input (Most Reliable)")
col1, col2 = st.columns(2)
with col1:
    manual_lat = st.number_input(
        "Latitude", 
        value=st.session_state.marker_location[0] if st.session_state.marker_location else 64.0, 
        format="%.6f"
    )
with col2:
    manual_lon = st.number_input(
        "Longitude", 
        value=st.session_state.marker_location[1] if st.session_state.marker_location else 11.0, 
        format="%.6f"
    )

if st.button("Set Marker at Manual Coordinates"):
    st.session_state.marker_location = [manual_lat, manual_lon]
    st.rerun()

# Display current selection
if st.session_state.marker_location is not None:
    st.success(f"**Selected Coordinates:** {st.session_state.marker_location}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Latitude:** {st.session_state.marker_location[0]:.6f}")
    with col2:
        st.write(f"**Longitude:** {st.session_state.marker_location[1]:.6f}")
else:
    st.info("No location selected yet. Click on the map or use manual input above.")

# Debug information
with st.expander("Debug Info"):
    st.write("If the map click isn't working precisely, use the manual input above.")
    st.write("Streamlit's native map should have better positioning than Folium.")