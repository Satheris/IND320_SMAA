# necessary imports for this page
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.common import (read_data, 
                          generate_months,
                          month_start_converter,
                          month_end_converter)

st.set_page_config(layout="wide")

if 'data' not in st.session_state:
    st.session_state.data = read_data()

# storing data on this page for further use
df = st.session_state.data


st.header('Plots')


# initiating selectbox for variable selection
column = st.selectbox('Select column', 
                      ('temperature_2m (°C)', 'precipitation (mm)', 
                       'wind_speed_10m (m/s)', 'wind_gusts_10m (m/s)', 
                       'wind_direction_10m (°)', 'all'))

# initiating selectslider for month selection
months = generate_months()
startMonth, endMonth = st.select_slider('Select months', 
                                        options=months,
                                                 value=(months[0], months[0]))


# using values given above to make plots
if column == 'all':
    fig = px.line(df[(df['time'] >= month_start_converter(startMonth)) & (df['time'] < month_end_converter(endMonth))], 
                  x='time', y=df.columns.drop('time'), title='All weather parameters over time')
    st.plotly_chart(fig)

else: 
    fig = px.line(df[(df['time'] >= month_start_converter(startMonth)) & (df['time'] < month_end_converter(endMonth))], 
                  x='time', y=column, title=f'{column} over time')
    st.plotly_chart(fig)
