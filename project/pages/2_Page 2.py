# necessary imports for this page
import streamlit as st
import pandas as pd

@st.cache_data
def read_data():
    data = pd.read_csv('project/data/open-meteo-subset.csv')
    data['time'] = pd.to_datetime(data['time'])
    return data

if 'data' not in st.session_state:
    st.session_state.data = read_data()

# storing data on this page for further use
df = st.session_state.data


st.header('Page 2')


# making a subset of the dataset with only the first month 
month_df = df[(df['time'] >= '2020-01-01T00:00') & (df['time'] < '2020-02-01T00:00')]

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
