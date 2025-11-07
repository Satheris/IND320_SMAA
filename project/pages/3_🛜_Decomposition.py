# necessary imports for this page
import streamlit as st
import pandas as pd
import pymongo
import plotly.express as px

# importing self defined functions
from utils.common import (openmeteo_download,
                          get_elhubdata)


# session_state.area to use across pages for data extraction
if 'AREA' not in st.session_state:
    st.session_state.AREA = 'NO1'
# assigning session_state.weather_data if not in cache
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = openmeteo_download(area=st.session_state.AREA)
# assigning session_state.elhub_data if not in cache
if 'elhub_data' not in st.session_state:
    st.session_state.elhub_data = get_elhubdata()


# storing data on this page for further use
df_elhub = st.session_state.elhub_data


# page configuration
st.set_page_config(layout='wide')
st.header('Decomposition')
st.write(f'Decomposition analyses of Elhub data from electrical price area {st.session_state.AREA}')


# initializing tabs 
tab1, tab2 = st.tabs(['STL analysis', 'Spectrogram'])

# filling tab 1
with tab1:
    st.header('Seasonal-Trend decomposition with LOESS')

# filling tab 2
with tab2:
    st.header('Spectrogram')