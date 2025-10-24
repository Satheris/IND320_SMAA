# necessary imports for this page
import streamlit as st
import pandas as pd


from utils.common import (read_data, 
                          init_connection, 
                          get_data)

if 'data' not in st.session_state:
    st.session_state.data = read_data()


st.header('Elhub')


# Initialize connection
client = init_connection()

# Pull data from the collection
items = get_data(client)

# Print results.
for item in items:
    st.write(f"{item['name']} is {item['age']} years old")