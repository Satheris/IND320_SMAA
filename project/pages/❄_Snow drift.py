# necessary imports for this page
import streamlit as st

# Importing self defined functions
from utils.common import (openmeteo_download_snowdrift,
                          _set_new_year_range
                          )
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

if 'START_YEAR' not in st.session_state:
    st.session_state.START_YEAR = 2021
if 'END_YEAR' not in st.session_state:
    st.session_state.END_YEAR = 2022



# page configuration
st.set_page_config(layout='wide')
st.header('Snow Drift analysis')
st.write(f'Snow drift direction diagram for location chosen on *map page*')

# c1, c2 = st.columns(2)
# with c1:
#     start_year = st.number_input('Start year', min_value=2000, max_value=2023, 
#                                  value=st.session_state.START_YEAR, step=1, 
#                                  key='start_year', on_change=_set_new_start_year)
# with c2:
#     end_year = st.number_input('End year', min_value=2001, max_value=2024, 
#                                value=st.session_state.END_YEAR, step=1, 
#                                key='end_year', on_change=_set_new_end_year)

 
if 'marker_location' in st.session_state:
    start_year, end_year = st.select_slider('Select year range for snow drift calculation',
                                        [i for i in range(2000, 2025, 1)],
                                        value=(st.session_state.START_YEAR, st.session_state.END_YEAR),
                                        key='year_range',
                                        on_change=_set_new_year_range)
    if start_year == end_year:
        st.error('Error: year range has to span at least two years.')
    else:
        snowdrift_plot()
else: 
    st.info('No location chosen on *map page*')