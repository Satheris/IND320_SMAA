# necessary imports for this page
import streamlit as st
import datetime
import folium
from streamlit_folium import st_folium

# Importing self defined functions
from utils.common import (get_elhubdata,
                          openmeteo_download_snowdrift,
                          find_region_for_point,
                          _set_new_group,
                          _set_new_energy_type,
                          make_choropleth_subset,
                          read_geojson,
                          _set_new_start_date,
                          _set_new_end_date
                          )


# data session_state
# assigning session_state.production_data if not in cache
if 'production_data' not in st.session_state:
    st.session_state.production_data = get_elhubdata('production')
# assigning session_state.consumption_data if not in cache
if 'consumption_data' not in st.session_state:
    st.session_state.consumption_data = get_elhubdata('consumption')
# assigning session_state.snow_data if not in cache
if 'snow_data' not in st.session_state:
    st.session_state.snow_data = None


# map specific session_state features
if 'marker_location' not in st.session_state:
    st.session_state.marker_location = None  # No initial marker
if 'zoom' not in st.session_state:
    st.session_state.zoom = 4.5  # Zoom level to show all Norway
if 'map_center' not in st.session_state:
    st.session_state.map_center = [64.0, 11.0]  # Initial center on Norway
if 'selected_region' not in st.session_state:
    st.session_state.selected_region = None  # No region selected initially
if 'selected_region_feature' not in st.session_state:
    st.session_state.selected_region_feature = None  # Store the actual feature data
if 'ENERGY_TYPE' not in st.session_state:
    st.session_state.ENERGY_TYPE = None
if 'GROUP' not in st.session_state:
    st.session_state.GROUP = None

# date caches
if 'min_date' not in st.session_state:
    st.session_state.min_date = datetime.date(2021, 1, 1)
if 'START_DATE' not in st.session_state:
    st.session_state.START_DATE = datetime.date(2021, 1, 1)
if 'max_date' not in st.session_state:
    st.session_state.max_date = datetime.date(2021, 12, 31)
if 'END_DATE' not in st.session_state:
    st.session_state.END_DATE = datetime.date(2021, 1, 5)




# page configuration
st.set_page_config(layout='wide')
st.header('Map')
st.write(f"Map covering Norway's electrical price areas. Click a location for snow drift calculation on *snow drift page*.")


# Load and add GeoJSON regions
# try:
#     # Load the GeoJSON file
#     with open(r'project/data/file.geojson', 'r', encoding='utf-8') as f:
#         geojson_data = json.load(f)

#     for features_list in geojson_data['features']:
#         splitted = features_list['properties']['ElSpotOmr'].split(' ')
#         features_list['properties']['ElSpotOmr'] = splitted[0]+splitted[1]
    
geojson_data = read_geojson()

# Create the base map
m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)

# ADD CHOROPLETH LAYER HERE
if st.session_state['GROUP'] is not None:
    df_agg = make_choropleth_subset()
    
    folium.Choropleth(
        geo_data=geojson_data,  # Your GeoJSON data
        data=df_agg,   # Aggregated energy data
        columns=["priceArea", "quantityKwh"],  # Region ID and value columns
        key_on="feature.properties.ElSpotOmr",  # Match GeoJSON property to your data
        fill_color="YlGn",      # Color scheme
        fill_opacity=0.6,       # Adjust opacity as needed
        line_opacity=0.2,
        legend_name=f"{st.session_state['ENERGY_TYPE']} Energy Production (Kwh)",
        nan_fill_color="purple",  # Color for regions with no data
        nan_fill_opacity=0.4,
    ).add_to(m)

    m.render() # to trigger the script
    m.get_root().script.render().replace("topright", "bottomleft")

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
            'color': "#e82a2a", #rgba(0,0,0,0)
            'weight': 3,  # Thicker border for emphasis
            'fillOpacity': 0, 
            'dashArray': '0'  # Ensure no dashes
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['ElSpotOmr'],
            aliases=['Region:'],
            localize=True
        ),
        name="Selected Region"
    ).add_to(m)



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

# except FileNotFoundError:
#     st.error("GeoJSON file not found. Please make sure 'file.geojson' exists in the same directory.")
#     # Create map without GeoJSON if file not found
#     m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)
# except Exception as e:
#     st.error(f"Error loading GeoJSON file: {e}")
#     m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.zoom)



c1, c2 = st.columns(2, gap='medium')


with c1: 
    # Render the map and capture interactions
    map_data = st_folium(m, width=450, height=575, key='norway_map')
    # st.plotly_chart(map_outline(), key='location', on_select='rerun')


# Update marker position, map state, and selected region if user interacted with the map
if map_data.get('last_clicked'):
    # Update marker location
    lat, lng = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
    st.session_state.marker_location = [lat, lng]

    st.session_state.snow_data = openmeteo_download_snowdrift(st.session_state.marker_location)


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


with c2:
    # Display coordinates and region information if a marker exists
    if st.session_state.marker_location is not None:

        # Display region information if available
        if st.session_state.selected_region:
            st.info(f'**Selected Region:** {st.session_state.selected_region}')
        else:
            st.warning('The selected location is not within any defined region.')

        # Printing chosen values
        col1, col2 = st.columns(2)
        with col1:
            st.write(f'**Latitude:** {st.session_state.marker_location[0]:.6f}')
        with col2:
            st.write(f'**Longitude:** {st.session_state.marker_location[1]:.6f}')
        
    else:
        st.info('No location selected yet. Click on the map to choose a location.')

    
    st.subheader('Selections for choropleth layer')


    energy_type = st.pills('Select energy type', ['production', 'consumption'], selection_mode='single', 
                            default=st.session_state.ENERGY_TYPE, key='energy_type',
                            on_change=_set_new_energy_type)

    if energy_type:
        groups = sorted(st.session_state[energy_type+'_data'][energy_type+'Group'].unique().tolist())
        groups_indices = {element: i for i, element in enumerate(groups)}
        group = st.selectbox(f'Select {energy_type} group', groups, 
                             index=groups_indices[st.session_state.GROUP],
                             key='group', on_change=_set_new_group)


        col1, col2 = st.columns(2)
        with col1: 
            start_date = st.date_input('Start date', min_value=st.session_state.min_date, 
                                    max_value=st.session_state.max_date, value=st.session_state.START_DATE, 
                                    format="DD/MM/YYYY", key='start_date', on_change=_set_new_start_date)
        with col2:
            end_date = st.date_input('End date', min_value=st.session_state.min_date, 
                                    max_value=st.session_state.max_date, value=st.session_state.END_DATE, 
                                    format="DD/MM/YYYY", key='end_date', on_change=_set_new_end_date)
        if start_date < end_date:
            st.success(f'Start date: {start_date}\n\nEnd date: {end_date}')
        else:
            st.error('Error: End date must fall after start date.')