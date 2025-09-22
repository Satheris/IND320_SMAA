import streamlit as st
import pandas as pd

st.header('This is my app!')

@st.cache_data
def read_data():
    data = pd.read_csv('data/open-meteo-subset.csv')
    return data

st.session_state.data = read_data()