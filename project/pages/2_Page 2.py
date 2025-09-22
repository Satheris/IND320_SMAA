import streamlit as st

st.header('Page 2')

st.dataframe(st.session_state.data)

# st.line_chart()