# necessary imports for this page
import streamlit as st
import pandas as pd
import pymongo
import plotly.express as px

# importing self defined functions
from utils.common import (openmeteo_download,
                          get_elhubdata,
                          STL_plotter,
                          STFT_plotter)


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


# need prodgroups for radio widgets in tabs
prodGroups = sorted(df_elhub['productionGroup'].unique().tolist())


# initializing tabs 
tab1, tab2 = st.tabs(['STL analysis', 'Spectrogram'])

# filling tab 1
with tab1:
    st.header('Seasonal-Trend decomposition with LOESS')

    c1, c2 = st.columns(2, gap='large')
    
    with c1: 
        prodGroup = st.radio('Choose a production group', prodGroups, horizontal=True, key='stl_prodGroup')

        seasonalSmoother = st.slider('Seasonal smoother', 3, 21, value=3, step=2)
        
        periodFlag = st.checkbox('')
        periodLength = st.slider('Length of a period', 1, 21, value=12, step=1)

    with c2:
        # button = st.button('None')
        trendSmoother = None

        robust = None

    STL_plotter(df_elhub=df_elhub, 
                area=st.session_state.AREA, 
                prodGroup=prodGroup, 
                periodLength=periodLength, 
                seasonalSmoother=seasonalSmoother, 
                trendSmoother=trendSmoother, 
                robust=robust)

# filling tab 2
with tab2:
    st.header('Spectrogram')

    prodGroup = st.radio('Choose a production group', prodGroups, horizontal=True, key='stft_prodGroup')


    fs = 1/3600
    nperseg = 24*7
    noverlap = None

    STFT_plotter(df_elhub=df_elhub,
                 area=st.session_state.AREA,
                 prodGroup=prodGroup,
                 fs=fs,
                 nperseg=nperseg,
                 noverlap=noverlap)