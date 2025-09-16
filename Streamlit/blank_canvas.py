# Import streamlit
import streamlit as st

# Add a header to the app
st.header("A simple Streamlit app")

# Add a button with a label 
if st.button("Press me!"):
    st.write("Yay!")

# Add a slider with a range from 0 to 100 in increments of 2, starting at 50
slider_value = st.slider('Select av value', min_value=0, max_value=100, value=50, step=2)
st.write('Slider value:', slider_value)