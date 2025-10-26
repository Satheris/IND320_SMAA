# necessary imports for this page
import streamlit as st
import pandas as pd
import pymongo


from utils.common import (read_data)

st.set_page_config(layout="wide")


if 'data' not in st.session_state:
    st.session_state.data = read_data()


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

for i, item in enumerate(items):
    if i < 10: 
        print(item)