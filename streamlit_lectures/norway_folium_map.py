import streamlit as st
import folium
from streamlit_folium import st_folium

# Set page configuration
st.set_page_config(page_title='Norway Location Picker', layout='wide')

# st.markdown("""
#     <style>
#     /* Fix for folium map positioning */
#     .folium-map {
#         position: relative !important;
#     }
#     /* Ensure proper positioning of map container */
#     .element-container {
#         position: relative;
#     }
#     </style>
# """, unsafe_allow_html=True)

# Initialize session state to store map state
if 'marker_location' not in st.session_state:
    st.session_state.marker_location = None  # No initial marker
if 'zoom' not in st.session_state:
    st.session_state.zoom = 5  # Zoom level to show all Norway
if 'map_center' not in st.session_state:
    st.session_state.map_center = [64.0, 11.0]  # Initial center on Norway

st.title('🇳🇴 Norway Location Picker')
st.write('Click anywhere on the map to mark a location')



# Create the base map - always centered on Norway
m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)

# Add marker only if a location has been clicked
if st.session_state.marker_location is not None:
    # Use CircleMarker for precise positioning
    folium.CircleMarker(
        location=st.session_state.marker_location,
        radius=8,
        popup=f"Coordinates: {st.session_state.marker_location}",
        color="red",
        fillColor="red",
        fillOpacity=0.7,
        weight=2
    ).add_to(m)

# Render the map and capture interactions
map_data = st_folium(m, width=700, height=500, key='norway_map')




# # Create a container for the map to help with positioning
# map_container = st.container()

# with map_container:
#     # Create the base map using the current map center from session state
#     m = folium.Map(
#         location=st.session_state.map_center, 
#         zoom_start=st.session_state.zoom,
#         # Disable scroll wheel zoom to reduce positioning issues
#         # scrollWheelZoom=False
#     )

#     # Add marker only if a location has been clicked
#     if st.session_state.marker_location is not None:
#         # Use a simple circle marker for precise positioning
#         folium.CircleMarker(
#             location=st.session_state.marker_location,
#             radius=10,
#             popup=f"Coordinates: {st.session_state.marker_location}",
#             color="#3186cc",
#             fillColor="#3186cc",
#             fillOpacity=0.7,
#             weight=2
#         ).add_to(m)

#     # Render the map with specific height and use_container_width for better positioning
#     map_data = st_folium(
#         m, 
#         height=500, 
#         width=700,
#         use_container_width=False,  # Use fixed width to avoid container issues
#         key="norway_map",
#         returned_objects=["last_clicked", "zoom", "center"]
#     )





# Update marker position and map state if user interacted with the map
if map_data.get('last_clicked'):
    # Update marker location
    lat, lng = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
    st.session_state.marker_location = [lat, lng]
    
    # Update map view state to maintain current view
    if map_data.get('center'):
        st.session_state.map_center = [map_data['center']['lat'], map_data['center']['lng']]
    if map_data.get('zoom'):
        st.session_state.zoom = map_data['zoom']
    
    # Use Streamlit's rerun to update the map immediately
    st.rerun()

# Display coordinates if a marker exists
if st.session_state.marker_location is not None:
    st.success(f'**Selected Coordinates:** {st.session_state.marker_location}')
    
    # Add some useful information
    col1, col2 = st.columns(2)
    with col1:
        st.write(f'**Latitude:** {st.session_state.marker_location[0]:.6f}')
    with col2:
        st.write(f'**Longitude:** {st.session_state.marker_location[1]:.6f}')
else:
    st.info('No location selected yet. Click on the map to choose a location.')



