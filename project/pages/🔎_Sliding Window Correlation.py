# necessary imports for this page
import streamlit as st
import pandas as pd

# importing self defined functions
from utils.common import (generate_months,
                          month_number_converter,
                          openmeteo_download,
                          get_elhubdata,
                          _set_new_area)


# session_state.AREA to use across pages for data extraction
if 'AREA' not in st.session_state:
    st.session_state.AREA = 'NO1'
# assigning session_state.weather_data if not in cache
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = openmeteo_download(area=st.session_state.AREA)
# assigning session_state.production_data if not in cache
if 'production_data' not in st.session_state:
    st.session_state.production_data = get_elhubdata('production')
# assigning session_state.consumption_data if not in cache
if 'consumption_data' not in st.session_state:
    st.session_state.consumption_data = get_elhubdata('consumption')



# page configuration
st.set_page_config(layout='wide')
st.header('Sliding Window Correlation')
st.write('Correlation analysis between weather and energy production or consumption. *Lag* optional.')



energy_type = st.pills('Select energy type', ['production', 'consumption'], selection_mode='single', default=None, key='energy_type')


weather_variable = st.selectbox('Select weather variable', list(st.session_state.weather_data.columns.)remove('time'))