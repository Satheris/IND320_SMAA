# necessary imports for this page
import streamlit as st
import pandas as pd
import pymongo
import plotly.exceptions as px


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


c1, c2 = st.columns(2)

c1.subheader('Total energy production in 2021 by price area')

area = c1.radio('Choose a geographic area', ['NO1', 'NO2', 'NO3', 'NO4', 'NO5'])

df_kwh_byArea = df[df['priceArea'] == area].groupby('productionGroup').agg({'quantityKwh': 'sum'})

fig = px.pie(df_kwh_byArea, values='sum(quantityKwh)', names='productionGroup', 
             title=f'Total energy production in area {area} by groduction group', 
             color='productionGroup')
fig.show()



# for i, item in enumerate(items):
#     if i < 10: 
#         c1.write(item)