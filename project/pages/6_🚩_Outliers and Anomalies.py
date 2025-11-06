# necessary imports for this page
import streamlit as st
import pandas as pd
import pymongo
import plotly.express as px

# Importing self defined functions
from utils.common import (openmeteo_download,
                          SPC_outlier_plot,
                          LOF_stats_plot)


# session_state.area to use across pages for data extraction
if 'AREA' not in st.session_state:
    st.session_state.AREA = 'NO1'
# assigning session_state.data if not in cache
if 'data' not in st.session_state:
    st.session_state.data = openmeteo_download(area=st.session_state.AREA)

# storing data on this page for further use
df = st.session_state.data


# page configuration
st.set_page_config(layout='wide')
st.header('Outliers and Anomalies')
st.write(f'Outlier and anomaly analysis of weather data from electrical price area {st.session_state.AREA}')


# Initializing tabs
tab1, tab2 = st.tabs(['Outlier/SPC analysis', 'Anomaly/LOF analysis'])


# Filling tab1
with tab1:
    st.subheader('Outlier/SPC analysis')

    ## Put in User Inputs here

    SPC_outlier_plot(df=df, column="temperature_2m (°C)", dct_cutoff=10, n_std=3)


# Filling tab2
with tab2:
    st.subheader('Anomaly/LOF analysis')

    ## Put in User Inputs here

    LOF_stats_plot(df=df, column="temperature_2m (°C)", contamination=0.01, n_neighbors=20)

