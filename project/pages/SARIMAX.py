# necessary imports for this page
import streamlit as st
import datetime
import folium
from streamlit_folium import st_folium
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Importing self defined functions
from utils.common import (get_elhubdata,
                          _set_new_group,
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

c1, c2 = st.columns([1, 2])
with c1:
    energy_type = st.pills('Select energy type for prediction', ['production', 'consumption'], selection_mode='single', 
                            default='production')
with c2:
    if energy_type:
        groups = sorted(st.session_state[energy_type+'_data'][energy_type+'Group'].unique().tolist())
        groups_indices = {element: i for i, element in enumerate(groups)}
        group = st.selectbox(f'Select {energy_type} group', groups, 
                                index=groups_indices[st.session_state.GROUP],
                                key='group', on_change=_set_new_group)

st.subheader('SARIMAX parameters')
c1, c2, c3 = st.columns(3)
with c1:
    st.number_input('**p** (autoregressive order)', 0, 10, value=1, step=1)
with c2:
    st.number_input('**d** (degree of local differencing)', 0, 2, value=0, step=1)
with c3:
    st.number_input('**q** (moving average order)', 0, 10, value=0, step=1)

with c1:
    st.number_input('**P** (seasonal autoregressive order)', 0, 10, value=0, step=1)
with c2:
    st.number_input('**D** (degree of seasonal differencing)', 0, 2, value=0, step=1)
with c3:
    st.number_input('**Q** (seasonal moving average order)', 0, 10, value=0, step=1)

st.number_input('**s** (seasonal period length in days)', 0, 365, value=365, step=1)

# training data time frame
st.date_input('Start date for training the model', min_value=datetime.date(2021, 1, 1), max_value=datetime.date(2021, 3, 1), value=datetime.date(2021, 1, 1))
st.date_input('End date for training the model', min_value=datetime.date(2021, 3, 1), max_value=datetime.date(2021, 12, 31), value=datetime.date(2021, 7, 1))

# forecast horizon
st.number_input('Forecast horizon in days', min_value=1, max_value=21, value=7, step=1)

# selected exogenous variables 



mod = SARIMAX()

# plot, including confidence intervals 