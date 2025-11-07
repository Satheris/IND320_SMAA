# necessary imports for this page
import streamlit as st

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


# page configuration
st.set_page_config(layout='wide')
st.header('Decomposition')
st.write(f'Decomposition analyses of Elhub data from electrical price area {st.session_state.AREA}')


# storing data on this page for further use
df_elhub = st.session_state.elhub_data


# production group selector for analyses below
prodGroups = sorted(df_elhub['productionGroup'].unique().tolist())
prodGroup = st.selectbox('Select production group', prodGroups)


# initializing tabs 
tab1, tab2 = st.tabs(['STL analysis', 'Spectrogram'])

# filling tab 1
with tab1:
    st.subheader('Seasonal-Trend decomposition with LOESS')

    c1, c2 = st.columns(2, gap='large')
    
    with c1: 

        seasonalSmoother = st.number_input('Seasonal smoother', 3, 31, value=13, step=2)

        trendSmoother = st.number_input('Trend smoother', 3, 730, value=365, step=2)


    with c2:
        robust = st.radio('Use weighted analysis that is robust to some forms of outliers', 
                          [True, False], horizontal=True)        
        
        periodLength = st.number_input('Length of a period (hours)', 1, 1000, value=24*7, step=1)


    STL_plotter(df_elhub=df_elhub, 
                area=st.session_state.AREA, 
                prodGroup=prodGroup, 
                periodLength=periodLength, 
                seasonalSmoother=seasonalSmoother, 
                trendSmoother=trendSmoother, 
                robust=robust)

# filling tab 2
with tab2:
    st.subheader('Spectrogram')


    fs = 1/3600
    nperseg = 24*7
    noverlap = None

    STFT_plotter(df_elhub=df_elhub,
                 area=st.session_state.AREA,
                 prodGroup=prodGroup,
                 fs=fs,
                 nperseg=nperseg,
                 noverlap=noverlap)