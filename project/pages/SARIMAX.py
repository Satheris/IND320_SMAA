# necessary imports for this page
import streamlit as st
import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX
import plotly.graph_objects as go

# Importing self defined functions
from utils.common import (get_elhubdata,
                          _set_new_group,
                          _set_new_energy_type,
                          make_sarimax_subset
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
    p = st.number_input('**p** (autoregressive order)', 0, 10, value=1, step=1)
with c2:
    d = st.number_input('**d** (degree of local differencing)', 0, 2, value=0, step=1)
with c3:
    q = st.number_input('**q** (moving average order)', 0, 10, value=0, step=1)

with c1:
    P = st.number_input('**P** (seasonal autoregressive order)', 0, 10, value=0, step=1)
with c2:
    D = st.number_input('**D** (degree of seasonal differencing)', 0, 2, value=0, step=1)
with c3:
    Q = st.number_input('**Q** (seasonal moving average order)', 0, 10, value=0, step=1)

s = st.number_input('**s** (seasonal period length in days)', 0, 365, value=365, step=1)


c1, c2, c3 = st.columns(3)
with c1:
    train_start_date = st.date_input('Start date for training the model', 
                                     min_value=datetime.date(2021, 1, 1), max_value=datetime.date(2021, 3, 1), 
                                     value=datetime.date(2021, 1, 1))
with c2:
    train_end_date = st.date_input('End date for training the model', 
                                   min_value=datetime.date(2021, 3, 1), max_value=datetime.date(2021, 12, 31), 
                                   value=datetime.date(2021, 7, 1))

with c3:
    st.number_input('Forecast horizon in days', min_value=1, max_value=21, value=7, step=1)

try: 
    # selected exogenous variables 
    groups_list = sorted(st.session_state[energy_type+'_data'][energy_type+'Group'].unique().tolist())
    groups_list.remove(st.session_state.GROUP)
    exog = st.pills('Exogenous variables', 
                    groups_list,
                    selection_mode='multi',
                    default=None)
except:
    st.error('Error: no energy type has been selected.')


df_sarimax = make_sarimax_subset()

mod = SARIMAX(endog=df_sarimax['quantityKwh'][df_sarimax[st.session_state['ENERGY_TYPE']+'Group'] == st.session_state['GROUP']].loc[str(train_start_date):str(train_end_date)],
            #   exog=df_sarimax['quantityKwh'][df_sarimax[st.session_state['ENERGY_TYPE']+'Group'] in exog].loc[train_start_date:train_end_date],
            #   exog=df_sarimax.loc[df_sarimax[st.session_state['ENERGY_TYPE']+'Group'].isin(exog),  [st.session_state['ENERGY_TYPE']+'Group', 'quantityKwh']],
                exog = df_sarimax.loc[(df_sarimax.index >= str(train_start_date)) & 
                                      (df_sarimax.index < str(train_end_date)) & 
                                      (df_sarimax[st.session_state['ENERGY_TYPE']+'Group'].isin(exog)),
                                      [st.session_state['ENERGY_TYPE']+'Group', 'quantityKwh']
                                      ],
              trend='c',
              order=(p, d, q),
              seasonal_order=(P, D, Q, s)
              )

res = mod.fit(disp=False)


mod = SARIMAX(endog=df_sarimax['quantityKwh'][df_sarimax[st.session_state['ENERGY_TYPE']+'Group'] == st.session_state['GROUP']],
            #   exog=df_sarimax['quantityKwh'][df_sarimax[st.session_state['ENERGY_TYPE']+'Group'] in exog],
                exog = df_sarimax.loc[#(df_sarimax.index >= str(train_start_date)) & 
                                      #(df_sarimax.index < str(train_end_date)) & 
                                      (df_sarimax[st.session_state['ENERGY_TYPE']+'Group'].isin(exog)),
                                      [st.session_state['ENERGY_TYPE']+'Group', 'quantityKwh']
                                      ],
              trend='c',
              order=(p, d, q),
              seasonal_order=(P, D, Q, s)
              )

res = mod.filter(res.params)

# In-sample one-step-ahead prediction wrapper function
predict = res.get_prediction()
predict_ci = predict.conf_int()

# Dynamic predictions starting from chosen train_end_date
predict_dy = res.get_prediction(dynamic=str(train_end_date))
predict_dy_ci = predict_dy.conf_int()


# Create the plotly figure
fig = go.Figure()

# Add observed data
fig.add_trace(go.Scatter(
    x=df_sarimax['quantityKwh'][df_sarimax[st.session_state['ENERGY_TYPE']+'Group'] == st.session_state['GROUP']].loc[str(train_start_date):].index,
    y=df_sarimax['quantityKwh'][df_sarimax[st.session_state['ENERGY_TYPE']+'Group'] == st.session_state['GROUP']].loc[str(train_start_date):],
    mode='markers',
    name='Observed',
    marker=dict(symbol='circle')
))

# Add one-step-ahead forecast
fig.add_trace(go.Scatter(
    x=predict.predicted_mean.loc[str(train_start_date):].index,
    y=predict.predicted_mean.loc[str(train_start_date):],
    mode='lines',
    line=dict(dash='dash', color='red'),
    name='One-step-ahead forecast'
))

# Add one-step-ahead confidence interval
ci = predict_ci.loc[str(train_end_date):]
fig.add_trace(go.Scatter(
    x=ci.index.tolist() + ci.index.tolist()[::-1],
    y=ci.iloc[:, 0].tolist() + ci.iloc[:, 1].tolist()[::-1],
    fill='toself',
    fillcolor='rgba(255,0,0,0.1)',
    line=dict(color='rgba(255,255,255,0)'),
    name='One-step CI',
    showlegend=True
))

# Add dynamic forecast
fig.add_trace(go.Scatter(
    x=predict_dy.predicted_mean.loc[str(train_start_date):].index,
    y=predict_dy.predicted_mean.loc[str(train_start_date):],
    mode='lines',
    line=dict(color='green'),
    name='Dynamic forecast (2013)'
))

# Add dynamic forecast confidence interval
ci_dy = predict_dy_ci.loc[str(train_start_date):]
fig.add_trace(go.Scatter(
    x=ci_dy.index.tolist() + ci_dy.index.tolist()[::-1],
    y=ci_dy.iloc[:, 0].tolist() + ci_dy.iloc[:, 1].tolist()[::-1],
    fill='toself',
    fillcolor='rgba(0,255,0,0.1)',
    line=dict(color='rgba(255,255,255,0)'),
    name='Dynamic CI',
    showlegend=True
))

# Update layout
fig.update_layout(
    title=f'{st.session_state.GROUP} forecast',
    xaxis_title='Date',
    yaxis_title=f'{st.session_state.GROUP} kWh',
    legend=dict(x=0.01, y=0.01),
    hovermode='x unified'
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)
