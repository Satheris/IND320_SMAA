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


st.pills('Select energy type', ['production', 'consumption'], selection_mode='single', 
                            default='production')

st.subheader('SARIMAX parameters')
# p, d, q, P, D, Q, s
c1, c2, c3 = st.columns(3)
with c1:
    st.number_input('p', 0, 10, value=1, step=1, horisontal=True)
with c2:
    st.number_input('d', 0, 2, value=0, step=1)
with c3:
    st.number_input('q', 0, 10, value=0, step=1)

with c1:
    st.number_input('P', 0, 10, value=0, step=1)
with c2:
    st.number_input('D', 0, 2, value=0, step=1)
with c3:
    st.number_input('Q', 0, 10, value=0, step=1)
st.number_input('s', 0, 365, value=365, step=1)

# training data time frame

# forecast horizon

# selected exogenous variables 





# plot, including confidence intervals 