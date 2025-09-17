# Imports
import streamlit as st
import numpy as np

st.header('Collatz conjecture')

# Initialize caching 
if 'value' not in st.session_state:
    st.session_state.value = None
    st.session_state.started = False 
    button_label = 'Start'
else: 
    if st.session_state.value % 2 == 0:
        button_label = 'Half it'
    elif st.session_state.value == 1: 
        button_label = 'Success!'
    else: 
        button_label = 'Triple and add one'


# Button varies by state 
st.button(button_label, disabled=(st.session_state.value == 1))
if st.session_state.value == 1: 
    st.balloons()

# Output 
if not st.session_state.started: 
    st.write('Ready')
else:
    st.write(st.session_state.value)

# Change in values 
if not st.session_state.started:
    # First press: sample random integer and cache it
    st.session_state.started = True 
    st.session_state.value = np.random.randint(1, 101)
else:
    # Subsequent presses: update the value according to the rules
    if st.session_state.value % 2 == 0:
        st.session_state.value //= 2            # // integer division   
    else:
        st.session_state.value = int((st.session_state.value * 3) + 1)
