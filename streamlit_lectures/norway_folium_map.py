# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# import json

# # Set page configuration
# st.set_page_config(page_title='Norway Location Picker', layout='wide')

# # Initialize session state to store map state
# if 'marker_location' not in st.session_state:
#     st.session_state.marker_location = None  # No initial marker
# if 'zoom' not in st.session_state:
#     st.session_state.zoom = 5  # Zoom level to show all Norway
# if 'map_center' not in st.session_state:
#     st.session_state.map_center = [64.0, 11.0]  # Initial center on Norway

# st.title('🇳🇴 Norway Location Picker')
# st.write('Click anywhere on the map to mark a location')

# # Load and add GeoJSON regions
# try:
#     # Load the GeoJSON file
#     with open(r'C:\Users\saraa\Documents\IND320_SMAA\project\data\file.geojson', 'r', encoding='utf-8') as f:
#         geojson_data = json.load(f)
    
#     # Create the base map
#     m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)
    
#     # Add GeoJSON layer to the map with custom styling
#     folium.GeoJson(
#         geojson_data,
#         # style_function=style_function,
#         style_function=lambda feature: {
#             'fillColor': 'lightblue',
#             'color': "#e8862a",  # Border color
#             'weight': 2,      # Border width
#             'fillOpacity': 0.1,  # Transparency of the fill
#         },
#         tooltip=folium.GeoJsonTooltip(
#             fields=['ElSpotOmr'],
#             aliases=['Region:'],
#             localize=True
#         ),
#         # Disable highlight/click behavior
#         highlight_function=lambda feature: {
#             'fillColor': 'lightblue',  # Keep the same color on hover/click
#             'color': '#e8862a',           # Keep the same border color
#             'weight': 2,               # Keep the same border width
#             'fillOpacity': 0.1,        # Keep the same transparency
#         },
#         # Alternative: completely disable interactions with the GeoJSON
#         # interactive=False
#     ).add_to(m)


    
# except FileNotFoundError:
#     st.error("GeoJSON file not found. Please make sure 'file.geojson' exists in the same directory.")
#     # Create map without GeoJSON if file not found
#     m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)
# except Exception as e:
#     st.error(f"Error loading GeoJSON file: {e}")
#     m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)

# # Add marker only if a location has been clicked
# if st.session_state.marker_location is not None:
#     # Use CircleMarker for precise positioning
#     folium.CircleMarker(
#         location=st.session_state.marker_location,
#         radius=8,
#         popup=f"Coordinates: {st.session_state.marker_location}",
#         color="red",
#         fillColor="red",
#         fillOpacity=0.7,
#         weight=2
#     ).add_to(m)

# # Render the map and capture interactions
# map_data = st_folium(m, width=450, height=575, key='norway_map')

# # Update marker position and map state if user interacted with the map
# if map_data.get('last_clicked'):
#     # Update marker location
#     lat, lng = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
#     st.session_state.marker_location = [lat, lng]
    
#     # Update map view state to maintain current view
#     if map_data.get('center'):
#         st.session_state.map_center = [map_data['center']['lat'], map_data['center']['lng']]
#     if map_data.get('zoom'):
#         st.session_state.zoom = map_data['zoom']
    
#     # Use Streamlit's rerun to update the map immediately
#     st.rerun()

# # Display coordinates if a marker exists
# if st.session_state.marker_location is not None:
#     st.success(f'**Selected Coordinates:** {st.session_state.marker_location}')
    
#     # Add some useful information
#     col1, col2 = st.columns(2)
#     with col1:
#         st.write(f'**Latitude:** {st.session_state.marker_location[0]:.6f}')
#     with col2:
#         st.write(f'**Longitude:** {st.session_state.marker_location[1]:.6f}')
# else:
#     st.info('No location selected yet. Click on the map to choose a location.')









# # # import streamlit as st
# # # import folium
# # # from streamlit_folium import st_folium
# # # import json

# # # # Set page configuration
# # # st.set_page_config(page_title='Norway Location Picker', layout='wide')

# # # # Initialize session state to store map state
# # # if 'marker_location' not in st.session_state:
# # #     st.session_state.marker_location = None  # No initial marker
# # # if 'zoom' not in st.session_state:
# # #     st.session_state.zoom = 5  # Zoom level to show all Norway
# # # if 'map_center' not in st.session_state:
# # #     st.session_state.map_center = [64.0, 11.0]  # Initial center on Norway
# # # if 'selected_region' not in st.session_state:
# # #     st.session_state.selected_region = None  # No region selected initially

# # # st.title('🇳🇴 Norway Location Picker')
# # # st.write('Click anywhere on the map to mark a location')

# # # # Load and add GeoJSON regions
# # # try:
# # #     # Load the GeoJSON file
# # #     with open(r'C:\Users\saraa\Documents\IND320_SMAA\project\data\file.geojson', 'r', encoding='utf-8') as f:
# # #         geojson_data = json.load(f)
    
# # #     # Create the base map
# # #     m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)

# # #     # Add CSS to specifically remove the black box highlight without affecting our custom styles
# # #     m.get_root().header.add_child(folium.Element("""
# # #     <style>
# # #     /* Remove the black box highlight on click while preserving our custom styles */
# # #     /* Target only the default Leaflet highlight effect */
# # #     .leaflet-interactive.leaflet-touch-drag {
# # #         stroke-dasharray: none !important;
# # #         stroke-dashoffset: 0 !important;
# # #     }
    
# # #     /* Remove focus outline without affecting stroke color */
# # #     .leaflet-interactive:focus {
# # #         outline: none !important;
# # #     }
    
# # #     /* Preserve our custom styles by not overriding stroke and stroke-width */
# # #     /* Let the style_function handle these properties */
# # #     </style>
# # #     """))
    
# # #     # Function to style regions based on whether they are selected
# # #     def style_function(feature):
# # #         # Check if this feature is the selected one
# # #         if st.session_state.selected_region is not None:
# # #             # Compare feature properties to identify the selected region
# # #             # You might need to adjust this based on your GeoJSON structure
# # #             if 'ElSpotOmr' in feature['properties']:
# # #                 if feature['properties']['ElSpotOmr'] == st.session_state.selected_region:
# # #                     return {
# # #                         'fillColor': 'orange',  # Highlight color for selected region
# # #                         'color': 'red',  # Border color for selected region
# # #                         'weight': 3,            # Thicker border for selected region
# # #                         'fillOpacity': 0,     # More opaque for selected region
# # #                     }
        
# # #         # Default style for non-selected regions
# # #         return {
# # #             'fillColor': 'lightblue',
# # #             'color': '#e8862a',      # Border color
# # #             'weight': 2,          # Border width
# # #             'fillOpacity': 0,   # Transparency of the fill
# # #         }
    
# # #     # Add GeoJSON layer to the map with dynamic styling
# # #     geojson_layer = folium.GeoJson(
# # #         geojson_data,
# # #         style_function=style_function,
# # #         tooltip=folium.GeoJsonTooltip(
# # #             fields=['ElSpotOmr'],
# # #             aliases=['Region:'],
# # #             localize=True
# # #         ),
# # #         highlight_function=style_function,
# # #         # highlight_function=lambda feature: {
# # #         #     'fillColor': 'lightblue',
# # #         #     'color': '#e8862a',
# # #         #     'weight': 2,
# # #         #     'fillOpacity': 0.1,
# # #         # }
# # #     ).add_to(m)
    
# # #     # Store the GeoJSON layer in session state for region detection
# # #     st.session_state.geojson_data = geojson_data
    
# # # except FileNotFoundError:
# # #     st.error("GeoJSON file not found. Please make sure 'file.geojson' exists in the same directory.")
# # #     # Create map without GeoJSON if file not found
# # #     m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)
# # # except Exception as e:
# # #     st.error(f"Error loading GeoJSON file: {e}")
# # #     m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)

# # # # Add marker only if a location has been clicked
# # # if st.session_state.marker_location is not None:
# # #     # Use CircleMarker for precise positioning
# # #     folium.CircleMarker(
# # #         location=st.session_state.marker_location,
# # #         radius=8,
# # #         popup=f"Coordinates: {st.session_state.marker_location}",
# # #         color="red",
# # #         fillColor="red",
# # #         fillOpacity=0.7,
# # #         weight=2
# # #     ).add_to(m)

# # # # Render the map and capture interactions
# # # map_data = st_folium(m, width=700, height=500, key='norway_map')

# # # # Function to check if a point is inside a polygon
# # # def point_in_polygon(point, polygon):
# # #     # Simple point-in-polygon check
# # #     # For production use, you might want to use a more robust algorithm
# # #     x, y = point
# # #     inside = False
# # #     n = len(polygon)
# # #     p1x, p1y = polygon[0]
# # #     for i in range(1, n + 1):
# # #         p2x, p2y = polygon[i % n]
# # #         if y > min(p1y, p2y):
# # #             if y <= max(p1y, p2y):
# # #                 if x <= max(p1x, p2x):
# # #                     if p1y != p2y:
# # #                         xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
# # #                     if p1x == p2x or x <= xinters:
# # #                         inside = not inside
# # #         p1x, p1y = p2x, p2y
# # #     return inside

# # # # Function to find which region contains the clicked point
# # # def find_region_for_point(lat, lng, geojson_data):
# # #     for feature in geojson_data['features']:
# # #         geometry = feature['geometry']
# # #         if geometry['type'] == 'Polygon':
# # #             for polygon in geometry['coordinates']:
# # #                 if point_in_polygon([lng, lat], polygon):
# # #                     return feature['properties'].get('ElSpotOmr', 'Unknown Region')
# # #         elif geometry['type'] == 'MultiPolygon':
# # #             for multipolygon in geometry['coordinates']:
# # #                 for polygon in multipolygon:
# # #                     if point_in_polygon([lng, lat], polygon):
# # #                         return feature['properties'].get('ElSpotOmr', 'Unknown Region')
# # #     return None

# # # # Update marker position, map state, and selected region if user interacted with the map
# # # if map_data.get('last_clicked'):
# # #     # Update marker location
# # #     lat, lng = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
# # #     st.session_state.marker_location = [lat, lng]
    
# # #     # Find which region contains the clicked point
# # #     if 'geojson_data' in st.session_state:
# # #         region_name = find_region_for_point(lat, lng, st.session_state.geojson_data)
# # #         st.session_state.selected_region = region_name
    
# # #     # Update map view state to maintain current view
# # #     if map_data.get('center'):
# # #         st.session_state.map_center = [map_data['center']['lat'], map_data['center']['lng']]
# # #     if map_data.get('zoom'):
# # #         st.session_state.zoom = map_data['zoom']
    
# # #     # Use Streamlit's rerun to update the map immediately
# # #     st.rerun()

# # # # Display coordinates and region information if a marker exists
# # # if st.session_state.marker_location is not None:
# # #     st.success(f'**Selected Coordinates:** {st.session_state.marker_location}')
    
# # #     # Add some useful information
# # #     col1, col2 = st.columns(2)
# # #     with col1:
# # #         st.write(f'**Latitude:** {st.session_state.marker_location[0]:.6f}')
# # #     with col2:
# # #         st.write(f'**Longitude:** {st.session_state.marker_location[1]:.6f}')
    
# # #     # Display region information if available
# # #     if st.session_state.selected_region:
# # #         st.info(f'**Selected Region:** {st.session_state.selected_region}')
# # #     else:
# # #         st.warning('The selected location is not within any defined region.')
# # # else:
# # #     st.info('No location selected yet. Click on the map to choose a location.')











# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# import json

# # Set page configuration
# st.set_page_config(page_title='Norway Location Picker', layout='wide')

# # Initialize session state to store map state
# if 'marker_location' not in st.session_state:
#     st.session_state.marker_location = None  # No initial marker
# if 'zoom' not in st.session_state:
#     st.session_state.zoom = 5  # Zoom level to show all Norway
# if 'map_center' not in st.session_state:
#     st.session_state.map_center = [64.0, 11.0]  # Initial center on Norway
# if 'selected_region' not in st.session_state:
#     st.session_state.selected_region = None  # No region selected initially

# st.title('🇳🇴 Norway Location Picker')
# st.write('Click anywhere on the map to mark a location')

# # Load and add GeoJSON regions
# try:
#     # Load the GeoJSON file
#     with open(r'C:\Users\saraa\Documents\IND320_SMAA\project\data\file.geojson', 'r', encoding='utf-8') as f:
#         geojson_data = json.load(f)
    
#     # Create the base map
#     m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)
    
#     # Function to style regions based on whether they are selected
#     def style_function(feature):
#         # Check if this feature is the selected one
#         if st.session_state.selected_region is not None:
#             # Compare feature properties to identify the selected region
#             if 'name' in feature['properties']:
#                 if feature['properties']['name'] == st.session_state.selected_region:
#                     return {
#                         'fillColor': 'orange',  # Highlight color for selected region
#                         'color': 'darkorange',  # Border color for selected region
#                         'weight': 3,            # Thicker border for selected region
#                         'fillOpacity': 0.5,     # More opaque for selected region
#                     }
        
#         # Default style for non-selected regions
#         return {
#             'fillColor': 'lightblue',
#             'color': 'blue',      # Border color
#             'weight': 2,          # Border width
#             'fillOpacity': 0.1,   # Transparency of the fill
#         }
    
#     # Add GeoJSON layer to the map with custom styling
#     # Use a different approach to completely disable the black box
#     geojson_layer = folium.GeoJson(
#         geojson_data,
#         style_function=style_function,
#         tooltip=folium.GeoJsonTooltip(
#             fields=['ElSpotOmr'],
#             aliases=['Region:'],
#             localize=True
#         )
#     ).add_to(m)
    
#     # IMPORTANT: Add JavaScript to disable the default highlight behavior
#     # This is the key to removing the black box completely
#     m.get_root().html.add_child(folium.Element("""
#     <script>
#     // Wait for the map to load
#     window.addEventListener('load', function() {
#         setTimeout(function() {
#             // Find all GeoJSON paths and remove click events that cause highlighting
#             var paths = document.querySelectorAll('path.leaflet-interactive');
#             paths.forEach(function(path) {
#                 // Remove mouse event listeners that cause highlighting
#                 path.style.pointerEvents = 'none';
#             });
#         }, 1000);
#     });
#     </script>
#     """))
    
#     # Store the GeoJSON layer in session state for region detection
#     st.session_state.geojson_data = geojson_data
    
# except FileNotFoundError:
#     st.error("GeoJSON file not found. Please make sure 'file.geojson' exists in the same directory.")
#     # Create map without GeoJSON if file not found
#     m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)
# except Exception as e:
#     st.error(f"Error loading GeoJSON file: {e}")
#     m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)

# # Add marker only if a location has been clicked
# if st.session_state.marker_location is not None:
#     # Use CircleMarker for precise positioning
#     folium.CircleMarker(
#         location=st.session_state.marker_location,
#         radius=8,
#         popup=f"Coordinates: {st.session_state.marker_location}",
#         color="red",
#         fillColor="red",
#         fillOpacity=0.7,
#         weight=2
#     ).add_to(m)

# # Render the map and capture interactions
# map_data = st_folium(m, width=700, height=500, key='norway_map')

# # Function to check if a point is inside a polygon
# def point_in_polygon(point, polygon):
#     # Simple point-in-polygon check
#     x, y = point
#     inside = False
#     n = len(polygon)
#     p1x, p1y = polygon[0]
#     for i in range(1, n + 1):
#         p2x, p2y = polygon[i % n]
#         if y > min(p1y, p2y):
#             if y <= max(p1y, p2y):
#                 if x <= max(p1x, p2x):
#                     if p1y != p2y:
#                         xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
#                     if p1x == p2x or x <= xinters:
#                         inside = not inside
#         p1x, p1y = p2x, p2y
#     return inside

# # Function to find which region contains the clicked point
# def find_region_for_point(lat, lng, geojson_data):
#     for feature in geojson_data['features']:
#         geometry = feature['geometry']
#         if geometry['type'] == 'Polygon':
#             for polygon in geometry['coordinates']:
#                 if point_in_polygon([lng, lat], polygon):
#                     return feature['properties'].get('ElSpotOmr', 'Unknown Region')
#         elif geometry['type'] == 'MultiPolygon':
#             for multipolygon in geometry['coordinates']:
#                 for polygon in multipolygon:
#                     if point_in_polygon([lng, lat], polygon):
#                         return feature['properties'].get('ElSpotOmr', 'Unknown Region')
#     return None

# # Update marker position, map state, and selected region if user interacted with the map
# if map_data.get('last_clicked'):
#     # Update marker location
#     lat, lng = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
#     st.session_state.marker_location = [lat, lng]
    
#     # Find which region contains the clicked point
#     if 'geojson_data' in st.session_state:
#         region_name = find_region_for_point(lat, lng, st.session_state.geojson_data)
#         st.session_state.selected_region = region_name
    
#     # Update map view state to maintain current view
#     if map_data.get('center'):
#         st.session_state.map_center = [map_data['center']['lat'], map_data['center']['lng']]
#     if map_data.get('zoom'):
#         st.session_state.zoom = map_data['zoom']
    
#     # Use Streamlit's rerun to update the map immediately
#     st.rerun()

# # Display coordinates and region information if a marker exists
# if st.session_state.marker_location is not None:
#     st.success(f'**Selected Coordinates:** {st.session_state.marker_location}')
    
#     # Add some useful information
#     col1, col2 = st.columns(2)
#     with col1:
#         st.write(f'**Latitude:** {st.session_state.marker_location[0]:.6f}')
#     with col2:
#         st.write(f'**Longitude:** {st.session_state.marker_location[1]:.6f}')
    
#     # Display region information if available
#     if st.session_state.selected_region:
#         st.info(f'**Selected Region:** {st.session_state.selected_region}')
#     else:
#         st.warning('The selected location is not within any defined region.')
# else:
#     st.info('No location selected yet. Click on the map to choose a location.')









import streamlit as st
import folium
from streamlit_folium import st_folium
import json

# Set page configuration
st.set_page_config(page_title='Norway Location Picker', layout='wide')

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

st.title('🇳🇴 Norway Location Picker')
st.write('Click anywhere on the map to mark a location')

# Load and add GeoJSON regions
try:
    # Load the GeoJSON file
    with open(r'C:\Users\saraa\Documents\IND320_SMAA\project\data\file.geojson', 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    
    # Create the base map
    m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)
    
    # Add base GeoJSON layer with default styling (no highlighting)
    base_geojson = folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': 'lightblue',
            'color': 'blue',
            'weight': 2,
            'fillOpacity': 0.1,
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
                'color': 'darkorange',
                'weight': 4,  # Thicker border for emphasis
                'fillOpacity': 0.3,  # Slightly more opaque but still transparent
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

# Render the map and capture interactions
map_data = st_folium(m, width=700, height=500, key='norway_map')

# Function to check if a point is inside a polygon
def point_in_polygon(point, polygon):
    # Simple point-in-polygon check
    x, y = point
    inside = False
    n = len(polygon)
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Function to find which region contains the clicked point
def find_region_for_point(lat, lng, geojson_data):
    for feature in geojson_data['features']:
        geometry = feature['geometry']
        if geometry['type'] == 'Polygon':
            for polygon in geometry['coordinates']:
                if point_in_polygon([lng, lat], polygon):
                    return feature['properties'].get('ElSpotOmr', 'Unknown Region'), feature
        elif geometry['type'] == 'MultiPolygon':
            for multipolygon in geometry['coordinates']:
                for polygon in multipolygon:
                    if point_in_polygon([lng, lat], polygon):
                        return feature['properties'].get('ElSpotOmr', 'Unknown Region'), feature
    return None, None

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