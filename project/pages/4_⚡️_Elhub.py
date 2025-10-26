# necessary imports for this page
import streamlit as st
import pandas as pd
import pymongo
import plotly.express as px


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


c1, c2 = st.columns(2, gap='medium')


with c1:
    st.subheader('Total energy production in 2021 by price area')

    areas = sorted(df["priceArea"].unique().tolist())
    area = c1.radio('Choose a geographic area', areas, horizontal=True)

    df_kwh_byArea = df[df['priceArea'] == area].groupby('productionGroup').agg({'quantityKwh': 'sum'}).sort_values('quantityKwh').reset_index()
    
    try:
        # Simple version first
        fig = px.pie(
            df_kwh_byArea, 
            values='quantityKwh', 
            names='productionGroup',
            title=f'Total energy production in area {area} by production group',
            color='productionGroup')
        
        # Optional: Improve layout
        # fig.update_traces(textposition='inside', textinfo='percent+label')
        # fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")


with c2:
    st.subheader('Energy production progress')


