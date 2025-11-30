# necessary imports for this page
import streamlit as st
import pandas as pd

# importing self defined functions
from utils.common import openmeteo_download


# session_state.area to use across pages for data extraction
if 'AREA' not in st.session_state:
    st.session_state.AREA = 'NO1'
# assigning session_state.weather_data if not in cache
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = openmeteo_download()


# storing data on this page for further use
df = st.session_state.weather_data


# page configuration
st.set_page_config(layout='wide')
st.header('Weather data')
st.write(f'Weather data summary for electrical price area {st.session_state.AREA}')


# making a subset of the dataset with only the first month 
month_df = df[(df['time'] >= '2021-01-01T00:00') & (df['time'] < '2021-02-01T00:00')]

# making a dataframe on the necessary format, with arrays in single cells
chart_df = pd.DataFrame({
    "Variable": [
        "temperature (°C)",
        "precipitation (mm)",
        "wind speed 10m (m/s)",
        "wind gusts 10m (m/s)",
        "wind direction 10m (°)"
    ],
    "Values": [
        month_df["temperature_2m (°C)"].tolist(),
        month_df["precipitation (mm)"].tolist(),
        month_df["wind_speed_10m (m/s)"].tolist(),
        month_df["wind_gusts_10m (m/s)"].tolist(),
        month_df["wind_direction_10m (°)"].tolist()
    ]
})

# making table with LineChartColumn
st.data_editor(data=chart_df, 
               column_config={
                   'Values': st.column_config.LineChartColumn(
                       'Progression'
                   )
                },
                hide_index=True
)
