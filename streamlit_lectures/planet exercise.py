import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.header('Planets')

planets_df = pd.read_csv('../data/planets.csv')

planets_df['distance'] = planets_df['distance'].str.replace(' AU', '').astype(float)
planets_df['diameter'] = planets_df['diameter'].str.replace(' km', '').astype(float)

planets_df

planets_df.plot.bar(x='planet', y='distance', rot=0, color='red')

planets_df.plot.scatter(x='planet', y='distance', s=(planets_df['diameter']/4000)**2)
plt.show()