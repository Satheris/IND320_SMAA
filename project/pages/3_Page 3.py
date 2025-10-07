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

startConverter = {'January': '2020-01-01',
                  'February': '2020-02-01',
                  'March': '2020-03-01',
                  'April': '2020-04-01', 
                  'May': '2020-05-01',
                  'June': '2020-06-01',
                  'July': '2020-07-01',
                  'August': '2020-08-01',
                  'September': '2020-09-01',
                  'October': '2020-10-01',
                  'November': '2020-11-01',
                  'December': '2020-12-01'
                  }

endConverter = {'January': '2020-02-01',
                  'February': '2020-03-01',
                  'March': '2020-04-01',
                  'April': '2020-05-01', 
                  'May': '2020-06-01',
                  'June': '2020-07-01',
                  'July': '2020-08-01',
                  'August': '2020-09-01',
                  'September': '2020-10-01',
                  'October': '2020-11-01',
                  'November': '2020-12-01',
                  'December': '2021-01-01'
                  }

if column == 'All':
    fig = px.line(df[(df['time'] >= startConverter[startMonth]) & (df['time'] < endConverter[endMonth])], 
                  x='time', y=df.columns.drop('time'), title='All weather parameters over time')
    st.plotly_chart(fig)

else: 
    fig = px.line(df[(df['time'] >= startConverter[startMonth]) & (df['time'] < endConverter[endMonth])], 
                  x='time', y=column, title=f'{column} over time')
    st.plotly_chart(fig)
