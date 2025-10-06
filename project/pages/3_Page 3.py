import streamlit as st
import pandas as pd

@st.cache_data
def read_data():
    data = pd.read_csv('project/data/open-meteo-subset.csv')
    return data

if 'data' not in st.session_state:
    st.session_state.data = read_data()

st.header('Page 3')

column = st.selectbox('Select column', 
                      ("temperature_2m (°C)", "precipitation (mm)", 
                       "wind_speed_10m (m/s)", "wind_gusts_10m (m/s)", 
                       "wind_direction_10m (°)", 'All'))

startMonth, endMonth = st.select_slider('Select months', 
                                        options=['January',
                                                 'February',
                                                 'March',
                                                 'April', 
                                                 'May',
                                                 'June',
                                                 'July',
                                                 'August',
                                                 'September',
                                                 'October',
                                                 'November',
                                                 'December'
                                                 ])
