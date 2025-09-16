# Imports
import streamlit as st
import numpy as np

st.header('Collatz conjecture')

if 'value' not in st.session_state:
    st.session_state.value = 0

def update():
    if st.session_state.value:
        return st.session_state.value


@st.cache_data
def value():
    v = np.random.randint(1, 101)


button = st.button('Start')

if not button:
    st.write('Ready')

if button:
    v = value()
    button = st.button('Next')
    st.write(v)