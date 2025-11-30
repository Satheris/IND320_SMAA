# necessary imports for this page
import streamlit as st

# importing self defined functions
from utils.common import (openmeteo_download,
                          get_elhubdata,
                          SWC_plot
                          )


# session_state.AREA to use across pages for data extraction
if 'AREA' not in st.session_state:
    st.session_state.AREA = 'NO1'
# assigning session_state.weather_data if not in cache
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = openmeteo_download()
# assigning session_state.production_data if not in cache
if 'production_data' not in st.session_state:
    st.session_state.production_data = get_elhubdata('production')
# assigning session_state.consumption_data if not in cache
if 'consumption_data' not in st.session_state:
    st.session_state.consumption_data = get_elhubdata('consumption')

if 'lag' not in st.session_state:
    st.session_state.lag = 0



# page configuration
st.set_page_config(layout='wide')
st.header('Sliding Window Correlation')
st.write('Correlation analysis between weather and energy production or consumption.') #  *Lag* optional.


c1, c2, c3 = st.columns([1, 2, 2], gap='medium')

with c1:
    energy_type = st.pills('Select energy type:', ['production', 'consumption'], selection_mode='single', default='production')

with c2:
    weather_variables = list(st.session_state.weather_data.columns)
    weather_variables.remove('time')
    weather_variable = st.selectbox('Select weather variable:', weather_variables)


with c3:
    window_length = st.slider('Select window length (in days):', min_value=10, max_value=70, value=45, step=1)

SWC_plot(weather_variable=weather_variable, energy_type=energy_type, window_length=window_length)