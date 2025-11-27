# necessary imports for this page
import streamlit as st

# Importing self defined functions
from utils.common import (_set_new_year_range
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
st.write(f'Snow drift direction diagram for location chosen on *map page*.')



if st.session_state.marker_location:
    start_year, end_year = st.select_slider('Select year range for snow drift calculation',
                                [i for i in range(2000, 2025, 1)],
                                value=(st.session_state.START_YEAR, st.session_state.END_YEAR),
                                key='year_range',
                                on_change=_set_new_year_range)
    if st.session_state.snow_data is not None:
        snowdrift_plot()

else:
    st.info('No location chosen on *map page*.')
