# necessary imports for this page
import streamlit as st

# Importing self defined functions
from utils.common import (openmeteo_download,
                          openmeteo_download_snowdrift)
from utils.snowdrift import snowdrift_plot


# session_state.area to use across pages for data extraction
if 'AREA' not in st.session_state:
    st.session_state.AREA = 'NO1'
# assigning session_state.weather_data if not in cache
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = openmeteo_download(area=st.session_state.AREA)

# page configuration
st.set_page_config(layout='wide')
st.header('Snow Drift analysis')
st.write(f'Snow drift direction diagram for location chosen on *map page*')


weather_data_snow = openmeteo_download_snowdrift(area=st.session_state.AREA, endYear=2022)

snowdrift_plot(weather_data_snow)