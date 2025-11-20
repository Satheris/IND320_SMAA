# necessary imports for this page
import streamlit as st

# Importing self defined functions
from utils.common import (map_outline)
from utils.snowdrift import snowdrift_plot


# assigning session_state.location
if 'location' not in st.session_state:
    st.session_state.location = {'lat': None, 'lon': None}


# page configuration
st.set_page_config(layout='wide')
st.header('Map')
st.write(f"Map covering Norway's electrical price areas")


c1, c2 = st.columns(2, gap='medium')

with c1: 
    st.plotly_chart(map_outline(), key='location', on_select='rerun')

with c2:
    st.write(st.session_state.location)