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



fig = px.line(df, x='time', y=['precipitation (mm)', 'temperature_2m (°C)'], title='Weather parameters over time')
st.plotly_chart(fig)

# fig, ax = plt.subplots()
# ax.set_title('Plot')
# ax.set_ylabel('')
# ax.set_xlabel('Time')

# ax.plot(df['temperature_2m (°C)'])
# ax.legend()

# st.pyplot(fig)



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

