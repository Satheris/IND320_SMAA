# Imports
import streamlit as st
import numpy as np

st.header('Collatz conjecture')

@st.dialog('Continue?', dismissible=True)
def stoprun(count):
    st.write(f'You have not reached 1 after {count} clicks. Do you still want to continue?')
    if st.button('No, I want to try again.'):
        del st.session_state.value
        del st.session_state.started
        del st.session_state.count
        st.rerun()
    elif st.button('Yes, I want to keep going!'):
        st.rerun()


# Initialize caching 
if 'value' not in st.session_state:
    st.session_state.value = None
    st.session_state.started = False 
    st.session_state.count = 0
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
    st.session_state.count += 1
    # Subsequent presses: update the value according to the rules
    if st.session_state.value % 2 == 0:
        st.session_state.value //= 2            # // integer division   
    else:
        st.session_state.value = int((st.session_state.value * 3) + 1)

if st.session_state.count == 5:
    stoprun(st.session_state.count)
