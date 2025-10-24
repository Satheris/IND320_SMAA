# necessary imports for this page
import streamlit as st
import pandas as pd
import pymongo


from utils.common import (read_data)

if 'data' not in st.session_state:
    st.session_state.data = read_data()


st.header('Elhub')


# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["uri"])

# Initialize connection
client = init_connection()


# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data(_client):
    db = _client['example']
    collection = db['data']
    items = collection.find()
    items = list(items)
    return items


# Pull data from the collection
items = get_data(client)

# Print results.
for item in items:
    st.write(f"{item['name']} is {item['age']} years old")