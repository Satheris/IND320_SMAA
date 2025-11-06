# necessary imports for this page
import streamlit as st
import pandas as pd
import pymongo
import plotly.express as px

# importing self defined functions
from utils.common import (openmeteo_download)


st.set_page_config(layout='wide')

st.header('Decomposition')

# tab1, tab2 = st.tabs(["Cat", "Dog"])

# with tab1:
#     st.header("A cat")
#     st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
# with tab2:
#     st.header("A dog")
#     st.image("https://static.streamlit.io/examples/dog.jpg", width=200)