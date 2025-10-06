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

st.data_editor(data=df.transpose(), 
               column_config=st.column_config.LineChartColumn())


st.dataframe(
    df,
    column_config={
        "precipitation (mm)": st.column_config.LineChartColumn(
            "Utvikling"
        )
    },
    hide_index=True
)



# st.line_chart()