# necessary imports for this page
import streamlit as st

# Importing self defined functions
from utils.common import (openmeteo_download,
                          SPC_outlier_plot,
                          LOF_stats_plot)


# session_state.area to use across pages for data extraction
if 'AREA' not in st.session_state:
    st.session_state.AREA = 'NO1'
# assigning session_state.weather_data if not in cache
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = openmeteo_download(area=st.session_state.AREA)


# storing data on this page for further use
df = st.session_state.weather_data


# page configuration
st.set_page_config(layout='wide')
st.header('Outliers and Anomalies')
st.write(f'Outlier and anomaly analysis of weather data from electrical price area {st.session_state.AREA}')


# Initializing tabs
tab1, tab2 = st.tabs(['Outlier/SPC analysis', 'Anomaly/LOF analysis'])

# tab1 -> SPC analysis with UI
with tab1:
    st.subheader(f'Outlier/SPC analysis of temperature in area {st.session_state.AREA}')

    # sliders divided into two columns
    c1, c2 = st.columns(2, gap='large')
    with c1:
        dct_cutoff = st.slider('Cutoff for DCT filter', 
                               0, 25, value=10, step=1)
    with c2: 
        n_std = st.slider('Number of standard deviations for calculating upper and lower bounds', 
                          0.5, 6.0, value=3.0, step=0.25)


    SPC_outlier_plot(df=df, column='temperature_2m (°C)', dct_cutoff=dct_cutoff, n_std=n_std)


# tab2 -> LOF analysis with UI
with tab2:
    st.subheader(f'Anomaly/LOF analysis of precipitation in area {st.session_state.AREA}')

    # sliders divided into two columns
    c1, c2 = st.columns(2, gap='large')
    with c1:
        contamination = st.slider('Proportion of outliers', 
                                  0.01, 0.5, value=0.01, step=0.01)
    with c2: 
        n_neighbors = st.slider('Number of neighbors', 
                                3, 50, value=20, step=1)

    LOF_stats_plot(df=df, column='precipitation (mm)', contamination=contamination, n_neighbors=n_neighbors)
