# necessary imports for this page
import streamlit as st
import pandas as pd
import pymongo
import plotly.express as px

# importing self defined functions
from utils.common import (openmeteo_download)


# session_state.area to use across pages for data extraction
if 'area' not in st.session_state:
    st.session_state.area = 'NO1'
# assigning session_state.data if not in cache
if 'data' not in st.session_state:
    st.session_state.data = openmeteo_download(area=st.session_state.AREA)

# storing data on this page for further use
df = st.session_state.data


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