# necessary imports for this page
import streamlit as st
import folium
import streamlit_folium as st_folium
import json

# Importing self defined functions
from utils.common import (map_outline)
from utils.map import (find_region_for_point)


# Initialize session state to store map state
if 'marker_location' not in st.session_state:
    st.session_state.marker_location = None  # No initial marker
if 'zoom' not in st.session_state:
    st.session_state.zoom = 5  # Zoom level to show all Norway
if 'map_center' not in st.session_state:
    st.session_state.map_center = [64.0, 11.0]  # Initial center on Norway
if 'selected_region' not in st.session_state:
    st.session_state.selected_region = None  # No region selected initially
if 'selected_region_feature' not in st.session_state:
    st.session_state.selected_region_feature = None  # Store the actual feature data


# page configuration
st.set_page_config(layout='wide')
st.header('Map')
st.write(f"Map covering Norway's electrical price areas. Click a location for snow drift calculation on *snow drift page*")


# Load and add GeoJSON regions
try:
    # Load the GeoJSON file
    with open(r'project/data/file.geojson', 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    
    # Create the base map
    m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)
    
    # Add base GeoJSON layer with default styling (no highlighting)
    base_geojson = folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': 'lightblue',
            'color': '#e8862a',
            'weight': 2,
            'fillOpacity': 0,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['ElSpotOmr'],
            aliases=['Region:'],
            localize=True
        ),
        name="Base Regions"  # Give it a name for layer control
    ).add_to(m)
    
    # Add a separate overlay layer for the highlighted region
    if st.session_state.selected_region_feature is not None:
        highlight_geojson = folium.GeoJson(
            st.session_state.selected_region_feature,
            style_function=lambda feature: {
                'fillColor': 'orange',
                'color': "#60e82a",
                'weight': 4,  # Thicker border for emphasis
                'fillOpacity': 0, 
                'dashArray': '0'  # Ensure no dashes
            },
            name="Selected Region"
        ).add_to(m)
    
    # Add CSS to remove the black box highlight
    m.get_root().header.add_child(folium.Element("""
    <style>
    /* Remove the black box highlight on click */
    .leaflet-interactive.leaflet-touch-drag {
        stroke-dasharray: none !important;
        stroke-dashoffset: 0 !important;
    }
    
    /* Remove focus outline without affecting stroke color */
    .leaflet-interactive:focus {
        outline: none !important;
    }
    </style>
    """))
    
    # Store the GeoJSON data in session state for region detection
    st.session_state.geojson_data = geojson_data
    
except FileNotFoundError:
    st.error("GeoJSON file not found. Please make sure 'file.geojson' exists in the same directory.")
    # Create map without GeoJSON if file not found
    m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)
except Exception as e:
    st.error(f"Error loading GeoJSON file: {e}")
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


c1, c2 = st.columns([2, 1], gap='medium')

with c1: 
    # Render the map and capture interactions
    map_data = st_folium(m, width=450, height=575, key='norway_map')
    # st.plotly_chart(map_outline(), key='location', on_select='rerun')

with c2:
    # Update marker position, map state, and selected region if user interacted with the map
    if map_data.get('last_clicked'):
        # Update marker location
        lat, lng = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
        st.session_state.marker_location = [lat, lng]
        
        # Find which region contains the clicked point
        if 'geojson_data' in st.session_state:
            region_name, region_feature = find_region_for_point(lat, lng, st.session_state.geojson_data)
            st.session_state.selected_region = region_name
            st.session_state.selected_region_feature = region_feature
        
        # Update map view state to maintain current view
        if map_data.get('center'):
            st.session_state.map_center = [map_data['center']['lat'], map_data['center']['lng']]
        if map_data.get('zoom'):
            st.session_state.zoom = map_data['zoom']
        
        # Use Streamlit's rerun to update the map immediately
        st.rerun()

    # Display coordinates and region information if a marker exists
    if st.session_state.marker_location is not None:
        st.success(f'**Selected Coordinates:** {st.session_state.marker_location}')
        
        # Add some useful information
        col1, col2 = st.columns(2)
        with col1:
            st.write(f'**Latitude:** {st.session_state.marker_location[0]:.6f}')
        with col2:
            st.write(f'**Longitude:** {st.session_state.marker_location[1]:.6f}')
        
        # Display region information if available
        if st.session_state.selected_region:
            st.info(f'**Selected Region:** {st.session_state.selected_region}')
        else:
            st.warning('The selected location is not within any defined region.')
    else:
        st.info('No location selected yet. Click on the map to choose a location.')