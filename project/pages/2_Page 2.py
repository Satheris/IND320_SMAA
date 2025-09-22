import streamlit as st

st.header('Page 2')

st.write(st.session_state.data)

st.line_chart(st.session_state.data)