# necessary imports for this page
import streamlit as st
import datetime
import folium
from streamlit_folium import st_folium
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Importing self defined functions
from utils.common import (get_elhubdata,
                          )


# data session_state
# assigning session_state.production_data if not in cache
if 'production_data' not in st.session_state:
    st.session_state.production_data = get_elhubdata('production')
# assigning session_state.consumption_data if not in cache
if 'consumption_data' not in st.session_state:
    st.session_state.consumption_data = get_elhubdata('consumption')



# page configuration
st.set_page_config(layout='wide')
st.header('SARIMAX')
st.write(f"")