# necessary imports for this page
import streamlit as st
import pandas as pd

st.header('This is my app!')

# chaching to make experience smoother
@st.cache_data
def read_data():
    data = pd.read_csv('project/data/open-meteo-subset.csv')
    data['time'] = pd.to_datetime(data['time'])
    return data

if 'data' not in st.session_state:
    st.session_state.data = read_data()