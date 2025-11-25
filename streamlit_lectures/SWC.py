import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd




# Assuming OilExchange is your DataFrame
# Calculate rolling correlation
PerEURO_ExpNatGas_SWC = OilExchange['PerEURO'].rolling(45, center=True).corr(OilExchange['ExpNatGas'])

# Streamlit app
st.title("Sliding Window Correlation Analysis")
st.markdown("Window size: 45 days")

# Create slider for center point
max_center = len(OilExchange) - 23
center = st.slider(
    "Select center point:",
    min_value=22,
    max_value=max_center,
    value=min(22, max_center),
    step=1
)

# Create subplots
fig = make_subplots(
    rows=3, cols=1,
    subplot_titles=('PerEURO', 'ExpNatGas', 'Sliding Window Correlation'),
    vertical_spacing=0.08,
    shared_xaxes=True
)

# Add PerEURO trace
fig.add_trace(
    go.Scatter(
        x=OilExchange.index,
        y=OilExchange['PerEURO'],
        mode='lines',
        name='PerEURO',
        line=dict(color='blue')
    ),
    row=1, col=1
)

# Highlight window for PerEURO
window_start = center - 22
window_end = center + 22
fig.add_trace(
    go.Scatter(
        x=OilExchange.index[window_start:window_end],
        y=OilExchange['PerEURO'].iloc[window_start:window_end],
        mode='lines',
        name='PerEURO Window',
        line=dict(color='red', width=2)
    ),
    row=1, col=1
)

# Add ExpNatGas trace
fig.add_trace(
    go.Scatter(
        x=OilExchange.index,
        y=OilExchange['ExpNatGas'],
        mode='lines',
        name='ExpNatGas',
        line=dict(color='green')
    ),
    row=2, col=1
)

# Highlight window for ExpNatGas
fig.add_trace(
    go.Scatter(
        x=OilExchange.index[window_start:window_end],
        y=OilExchange['ExpNatGas'].iloc[window_start:window_end],
        mode='lines',
        name='ExpNatGas Window',
        line=dict(color='red', width=2)
    ),
    row=2, col=1
)

# Add SWC trace
fig.add_trace(
    go.Scatter(
        x=OilExchange.index,
        y=PerEURO_ExpNatGas_SWC,
        mode='lines',
        name='SWC',
        line=dict(color='purple')
    ),
    row=3, col=1
)

# Add center point marker for SWC
fig.add_trace(
    go.Scatter(
        x=[OilExchange.index[center]],
        y=[PerEURO_ExpNatGas_SWC.iloc[center]],
        mode='markers',
        name='Center Point',
        marker=dict(color='red', size=8)
    ),
    row=3, col=1
)

# Add horizontal line at y=0 for SWC
fig.add_hline(
    y=0, 
    line_dash="dot", 
    line_color="gray",
    row=3, col=1
)

# Update layout
fig.update_layout(
    height=700,
    showlegend=True,
    title_text="Sliding Window Correlation Analysis",
    hovermode='x unified'
)

# Update y-axes
fig.update_yaxes(title_text="PerEURO", row=1, col=1)
fig.update_yaxes(title_text="ExpNatGas", row=2, col=1)
fig.update_yaxes(title_text="SWC", row=3, col=1, range=[-1, 1])
fig.update_xaxes(title_text="Time", row=3, col=1)

# Display the plot
st.plotly_chart(fig, use_container_width=True)

# Display correlation value at center point
st.metric(
    label=f"Correlation at center point ({OilExchange.index[center].strftime('%Y-%m-%d') if hasattr(OilExchange.index, 'strftime') else center})",
    value=f"{PerEURO_ExpNatGas_SWC.iloc[center]:.3f}"
)