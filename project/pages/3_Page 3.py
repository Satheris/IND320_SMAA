import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

@st.cache_data
def read_data():
    data = pd.read_csv('project/data/open-meteo-subset.csv')
    data['time'] = pd.to_datetime(data['time'])
    return data

if 'data' not in st.session_state:
    st.session_state.data = read_data()

st.header('Page 3')


df = st.session_state.data




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
                                                 ],
                                                 value=('January', 'January'))


if column == 'All':
    fig = px.line(df, x='time', y=df.columns.drop('time'), title='All weather parameters over time')
    st.plotly_chart(fig)

else: 
    fig = px.line(df, x='time', y=column, title=f'{column} over time')
    st.plotly_chart(fig)
