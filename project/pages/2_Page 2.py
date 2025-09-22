import streamlit as st

@st.cache_data
def read_data():
    data = pd.read_csv('project/data/open-meteo-subset.csv')
    return data

if 'data' not in st.session_state:
    st.session_state.data = read_data()

st.header('Page 2')

st.dataframe(st.session_state.data)

# st.line_chart()