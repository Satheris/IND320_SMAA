# utils/common.py
import streamlit as st
import pandas as pd
import pymongo


@st.cache_data(show_spinner=True)
def read_data() -> pd.DataFrame:
    data = pd.read_csv('project/data/open-meteo-subset.csv')
    data['time'] = pd.to_datetime(data['time'])
    return data

def generate_months():
    months =   ['January',
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
                'December']
    return months

