# necessary imports for this page
import streamlit as st
import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX
import plotly.graph_objects as go

# Importing self defined functions
from utils.common import (get_elhubdata,
                          _set_new_group,
                          _set_new_energy_type,
                          make_sarimax_subset,
                          SARIMAX_plot
                          )


# data session_state
# assigning session_state.production_data if not in cache
if 'production_data' not in st.session_state:
    st.session_state.production_data = get_elhubdata('production')
# assigning session_state.consumption_data if not in cache
if 'consumption_data' not in st.session_state:
    st.session_state.consumption_data = get_elhubdata('consumption')

if 'ENERGY_TYPE' not in st.session_state:
    st.session_state.ENERGY_TYPE = None
if 'GROUP' not in st.session_state:
    st.session_state.GROUP = None



# page configuration
st.set_page_config(layout='wide')
st.header('SARIMAX')
st.write(f"")

c1, c2 = st.columns([1, 2])
with c1:
    energy_type = st.pills('Select energy type for prediction', ['production', 'consumption'], selection_mode='single', 
                            default=st.session_state.ENERGY_TYPE, key='energy_type', on_change=_set_new_energy_type)
with c2:
    if energy_type:
        groups = sorted(st.session_state[energy_type+'_data'][energy_type+'Group'].unique().tolist())
        groups_indices = {element: i for i, element in enumerate(groups)}
        group = st.selectbox(f'Select {energy_type} group', groups, 
                                index=groups_indices[st.session_state.GROUP],
                                key='group', on_change=_set_new_group)
    else:
        st.error('Error: the user must choose an energy type to forecast.')


st.subheader('SARIMAX parameters')
c1, c2, c3 = st.columns(3)
with c1:
    p = st.number_input('**p** (autoregressive order)', 0, 10, value=1, step=1, key='p')
with c2:
    d = st.number_input('**d** (degree of local differencing)', 0, 2, value=0, step=1, key='d')
with c3:
    q = st.number_input('**q** (moving average order)', 0, 10, value=0, step=1, key='q')

with c1:
    P = st.number_input('**P** (seasonal autoregressive order)', 0, 10, value=0, step=1, key='P', disabled=True)
with c2:
    D = st.number_input('**D** (degree of seasonal differencing)', 0, 2, value=0, step=1, key='D', disabled=True)
with c3:
    Q = st.number_input('**Q** (seasonal moving average order)', 0, 10, value=0, step=1, key='Q', disabled=True)

s = st.number_input('**s** (seasonal period length in days)', 0, 365, value=365, step=1, key='s')


c1, c2, c3 = st.columns(3)
with c1:
    train_start_date = st.date_input('Start date for training the model', 
                                     min_value=datetime.date(2021, 1, 1), max_value=datetime.date(2022, 12, 31),
                                     value=datetime.date(2021, 1, 1))
with c2:
    train_end_date = st.date_input('End date for training the model', 
                                   min_value=datetime.date(2022, 1, 1), max_value=datetime.date(2024, 12, 31), 
                                   value=datetime.date(2022, 1, 1))

with c3:
    forecast_horizon = st.number_input('Forecast horizon in days', min_value=1, max_value=(365*2), value=365, step=1)

forecast_end_date = train_end_date + datetime.timedelta(days=forecast_horizon)

if str(train_start_date) < str(train_end_date):
    try: 
        # selected exogenous variables 
        groups_list = sorted(st.session_state[energy_type+'_data'][energy_type+'Group'].unique().tolist())
        groups_list.remove(st.session_state.GROUP)
        exog_vars = st.pills('Exogenous variables', 
                        groups_list,
                        selection_mode='multi',
                        default=None)
        
        df_sarimax = make_sarimax_subset()

        SARIMAX_plot(df_sarimax, train_start_date, train_end_date, forecast_end_date, exog_vars)


    except:
        st.error('Error: no energy type has been selected.')

else:
    st.error('Error: End date must be after Start date.')

