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
    months =   ['January', 'February', 'March',
                'April', 'May', 'June',
                'July', 'August', 'September',
                'October', 'November', 'December']
    return months

def month_start_converter(month_text: str) -> str:
    month_dict = {'January': '2020-01-01',
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
                    'December': '2020-12-01'}
    return month_dict[month_text]