import streamlit as st
import pandas as pd

@st.cache_data
def read_data():
    data = pd.read_csv('project/data/open-meteo-subset.csv')
    return data

if 'data' not in st.session_state:
    st.session_state.data = read_data()

df = st.session_state.data

st.header('Page 2')

st.dataframe(df)



df_1month = pd.DataFrame({
    "column": df.columns[1:],
    "values": [df[column] for column in df.columns[1:] if '2020-01-01T00:00' <= df['time'] < '2020-02-01T00:00'
            #    df['temperature_2m (°C)'] if '2020-01-01T00:00' <= df['time'] < '2020-02-01T00:00',
            #    df['precipitation (mm)'] if '2020-01-01T00:00' <= df['time'] < '2020-02-01T00:00',
            #    df['wind_speed_10m (m/s)'] if '2020-01-01T00:00' <= df['time'] < '2020-02-01T00:00',
            #    df['wind_gusts_10m (m/s)'] if '2020-01-01T00:00' <= df['time'] < '2020-02-01T00:00',
            #    df['wind_direction_10m (°)'] if '2020-01-01T00:00' <= df['time'] < '2020-02-01T00:00'
               ]
})

st.data_editor(data=df_1month, 
               column_config={
                   'column': st.column_config.LineChartColumn(
                       'Utvikling'
                   )
                },
                hide_index=True
)

# st.dataframe(
#     df,
#     column_config={
#         "precipitation (mm)": st.column_config.LineChartColumn(
#             "Utvikling"
#         )
#     },
#     hide_index=True
# )

