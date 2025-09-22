import streamlit as st
import pandas as pd

@st.cache_data
def read_data():
    data = pd.read_csv('project/data/open-meteo-subset.csv')
    return data

if 'data' not in st.session_state:
    st.session_state.data = read_data()

st.header('Page 2')

st.dataframe(st.session_state.data)

for column in st.session_state.data:
    st.data_editor(data=st.session_state.data, 
                   column_config={column:st.column_config.LineChartColumn()}, 
                   hide_index=False)


# st.line_chart()