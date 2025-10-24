# necessary imports for this page
import streamlit as st
import pandas as pd

from utils.common import read_data

if 'data' not in st.session_state:
    st.session_state.data = read_data()


st.header('Elhub')