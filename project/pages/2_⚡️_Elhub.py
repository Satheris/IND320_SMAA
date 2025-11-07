# necessary imports for this page
import streamlit as st
import pandas as pd
import pymongo
import plotly.express as px

# importing self defined functions
from utils.common import (generate_months,
                          month_number_converter,
                          openmeteo_download,
                          get_elhubdata)


# session_state.area to use across pages for data extraction
if 'AREA' not in st.session_state:
    st.session_state.AREA = 'NO1'
# assigning session_state.data if not in cache
if 'data' not in st.session_state:
    st.session_state.data = openmeteo_download(area=st.session_state.AREA)

def _download_new_area():
    st.session_state.data = openmeteo_download(area=st.session_state.AREA)

def _set_new_area():
    st.session_state.AREA = st.session_state.area
    _download_new_area()



# page configuration
st.set_page_config(layout='wide')
st.header('Elhub')


# # Initialize connection.
# # Uses st.cache_resource to only run once.
# @st.cache_resource
# def init_connection():
#     return pymongo.MongoClient(st.secrets['mongo']['uri'])

# client = init_connection()


# # Pull data from the collection.
# # Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
# def get_data():
#     db = client['project']
#     collection = db['data']
#     items = collection.find()
#     items = list(items)
#     return items

# items = get_data()


# # Converting data to dataframe and doing type conversion
# df_elhub = pd.DataFrame(items)
# df_elhub['startTime'] = pd.to_datetime(df_elhub['startTime'], errors='coerce', utc=True)
# df_elhub['quantityKwh'] = pd.to_numeric(df_elhub['quantityKwh'], errors='coerce')
# df_elhub['month'] = df_elhub['startTime'].dt.month
# df_elhub['year'] = df_elhub['startTime'].dt.year

# df_elhub = df_elhub[df_elhub['year'] == 2021]

df_elhub = get_elhubdata()

# Initializing columns
c1, c2 = st.columns(2, gap='medium')

# Filling column 1
with c1:
    st.subheader('Total energy production in 2021 by price area')

    # Initiating radio selection for price areas
    areas = sorted(df_elhub['priceArea'].unique().tolist())
    area_index = {element: i for i, element in enumerate(areas)}
    area = st.radio('Choose a geographic area', areas, index=area_index[st.session_state.AREA],
                    horizontal=True, key='area', on_change=_set_new_area)

    # st.session_state.area = area

    # Making reduced dataset
    df_elhub_kwh_byArea = df_elhub[df_elhub['priceArea'] == area]\
        .groupby('productionGroup')\
            .agg({'quantityKwh': 'sum'})\
                .sort_values('quantityKwh', ascending=False)\
                    .reset_index()

    # try, except block to catch errors without crashing  
    try:
        # Base figure
        fig = px.pie(
            df_elhub_kwh_byArea, 
            values='quantityKwh', 
            names='productionGroup',
            title=f'Total energy production in area {area} in 2021',
            color='productionGroup')
        
        # Update hover info
        fig.update_traces(
            textposition='inside',
            textinfo='percent',
            hovertemplate='<b>%{label}</b><br>%{value} KWh<br>%{percent}')

        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f'Error creating chart: {str(e)}')


# Filling column 2
with c2:
    st.subheader('Energy production by month')
    
    # Initiating pill selection for production groups
    prods = sorted(df_elhub['productionGroup'].unique().tolist())
    prodgroups = st.pills('Select production group(s)', prods, selection_mode='multi', default=prods)

    # Initiating selectbox for month selction
    months = generate_months()
    month = st.selectbox('Select month', months)

    # Reducing dataset
    df_elhub_month = df_elhub[(df_elhub['priceArea'] == area) & 
                  (df_elhub['month'] == month_number_converter(month)) &
                  (df_elhub['productionGroup'].isin(prodgroups))]
    df_elhub_month = df_elhub_month.sort_values(by='productionGroup').sort_values(by='startTime').reset_index()

    # try, except block to catch errors without crashing  
    try: 
        fig = px.line(df_elhub_month, 
                        x='startTime', 
                        y='quantityKwh', 
                        color='productionGroup',
                        title=f'Energy production in area {area} in {month}')

        st.plotly_chart(fig)

    except Exception as e:
        st.error(f'Error creating chart: {str(e)}')

# End columns


# Expander with info on the data
expander = st.expander('Source of the data')
expander.write('''
    The plots are based on data collected from Elhub Energy Data API, \
               regarding energy production in Norway across price areas NO1 through NO5. \
               The data covers energy production from hydro, wind, thermal and solar production \
               specifically, and other sources jointly. 
    
               API link: https://api.elhub.no/energy-data-api
               
    On the left column is a pie chart describing the yearly energy production by \
               price area chosen in the radio widget. You will find that hovering on a section \
               will give a legend box marking the production group, total energy produced \
               in that production group and the percentage of the active groups. \
               Because the plot is made with plotly, the legend is interactive, \
               and you can mark which production groups to include in the plot and calculation.

    On the right column is a line chart describing the energy production in the same \
               price area as on the right, but for only the chosen month from the selectbox \
               and for the marked production groups from the pill selection. \
               Again, plotly innately produces an interactive plot where you can mark out \
               specific areas of the plot to study closer. A guide appears when hovering over the chart.
    ''')