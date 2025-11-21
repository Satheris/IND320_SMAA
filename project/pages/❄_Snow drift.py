# necessary imports for this page
import streamlit as st

# Importing self defined functions
from utils.common import (openmeteo_download_snowdrift)
from utils.snowdrift import snowdrift_plot


# session_state.area to use across pages for data extraction
if 'AREA' not in st.session_state:
    st.session_state.AREA = 'NO1'
# assigning session_state.marker_location if not in cache
if 'marker_location' not in st.session_state:
    st.session_state.marker_location = None
# assigning session_state.snow_data if not in cache
if 'snow_data' not in st.session_state:
    st.session_state.snow_data = None


# page configuration
st.set_page_config(layout='wide')
st.header('Snow Drift analysis')
st.write(f'Snow drift direction diagram for location chosen on *map page*')

try: 
    snowdrift_plot(st.session_state.snow_data)
except: 
    st.markdown('No location chosen on *map page*')