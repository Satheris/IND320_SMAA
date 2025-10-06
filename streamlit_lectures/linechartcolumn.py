import streamlit as st
import pandas as pd

# Eksempeldata: hver rad har en liten tidsserie
df = pd.DataFrame({
    "Navn": ["Serie A", "Serie B", "Serie C"],
    "Verdier": [
        [1, 3, 2, 4, 5],
        [2, 2, 3, 3, 4],
        [5, 4, 3, 2, 1]
    ]
})

df

st.dataframe(
    df,
    column_config={
        "Verdier": st.column_config.LineChartColumn(
            "Utvikling",
            y_min=0,
            y_max=6
        )
    },
    hide_index=True
)
