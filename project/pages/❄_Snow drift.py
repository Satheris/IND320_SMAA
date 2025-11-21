# necessary imports for this page
import streamlit as st

# Importing self defined functions
from utils.common import (openmeteo_download,
                          openmeteo_download_snowdrift)
from utils.snowdrift import snowdrift_plot


# session_state.area to use across pages for data extraction
if 'AREA' not in st.session_state:
    st.session_state.AREA = 'NO1'
# assigning session_state.marker_location if not in cache
if 'marker_location' not in st.session_state:
    st.session_state.marker_location = None



# page configuration
st.set_page_config(layout='wide')
st.header('Snow Drift analysis')
st.write(f'Snow drift direction diagram for location chosen on *map page*')

try: 
    weather_data_snow = openmeteo_download_snowdrift(area=st.session_state.marker_location, endYear=2022)
    snowdrift_plot(weather_data_snow)
except: 
    st.markdown('No location chosen on *map page*')