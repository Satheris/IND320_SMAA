# necessary imports for this page
import streamlit as st
import pandas as pd
import pymongo
import plotly.express as px

from utils.common import (generate_months,
                          month_start_converter,
                          month_end_converter)

st.set_page_config(layout="wide")

st.header('Elhub')


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["uri"])

client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    db = client['project']
    collection = db['data']
    items = collection.find()
    items = list(items)
    return items

items = get_data()

df = pd.DataFrame(items)

# Initializing columns
c1, c2 = st.columns(2, gap='medium')

# Filling column 1
with c1:
    st.subheader('Total energy production in 2021 by price area')

    areas = sorted(df["priceArea"].unique().tolist())
    area = c1.radio('Choose a geographic area', areas, horizontal=True)

    df_kwh_byArea = df[df['priceArea'] == area]\
        .groupby('productionGroup')\
            .agg({'quantityKwh': 'sum'})\
                .sort_values('quantityKwh', ascending=False)\
                    .reset_index()
        
    try:
        # Base figure
        fig = px.pie(
            df_kwh_byArea, 
            values='quantityKwh', 
            names='productionGroup',
            title=f'Total energy production in area {area} by production group',
            color='productionGroup')
        
        # Update hover info
        fig.update_traces(
            textposition='inside',
            textinfo='percent',
            hovertemplate='<b>%{label}</b><br>%{value} KWh<br>%{percent}')

        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")


# Filling column 2
with c2:
    st.subheader('Energy production progress')
    
    prods = sorted(df["productionGroup"].unique().tolist())
    prodgroups = st.pills("Select production group(s)", prods, selection_mode="multi", default=prods)

    months = generate_months()
    month = st.selectbox('Select month', months)

    df_month = df[(df['priceArea'] == area) & 
                  (df['startTime'] >= month_start_converter(month)) &
                  (df['startTime'] < month_end_converter(month))]
    df_month = df_month.sort_values(by='productionGroup').sort_values(by='startTime').reset_index()
    df_month['startTime'] = pd.to_datetime(df_month['startTime'])

    try: 
        fig = px.line(df_month[df_month['productionGroup'] in prodgroups], 
                      x='startTime', 
                      y='quantityKwh', 
                      color='productionGroup')

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
