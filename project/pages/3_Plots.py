# necessary imports for this page
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.common import read_data

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
                                                 'December'],
                                                 value=('January', 'January'))

#making dictionaries to convert months into datetime values
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


# using values given above to make plots
if column == 'All':
    fig = px.line(df[(df['time'] >= startConverter[startMonth]) & (df['time'] < endConverter[endMonth])], 
                  x='time', y=df.columns.drop('time'), title='All weather parameters over time')
    st.plotly_chart(fig)

else: 
    fig = px.line(df[(df['time'] >= startConverter[startMonth]) & (df['time'] < endConverter[endMonth])], 
                  x='time', y=column, title=f'{column} over time')
    st.plotly_chart(fig)
