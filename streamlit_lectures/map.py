# import streamlit as st
# import plotly.express as px
# import pandas as pd
# import json
# import plotly.graph_objects as go

# # us_cities = pd.read_csv(
# #     "https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv"
# # )

# # fig = px.scatter_map(
# #     us_cities,
# #     lat="lat",
# #     lon="lon",
# #     hover_name="City",
# #     hover_data=["State", "Population"],
# #     color_discrete_sequence=["fuchsia"],
# #     zoom=3,
# #     height=300,
# #     width=600,
# # )

# with open(r'C:\Users\saraa\Documents\IND320_SMAA\project\data\file.geojson') as file:
#     priceAreas = json.load(file)



# fig = go.Figure()

# fig.update_layout(
#     map = {
#         'style': 'open-street-map',
#         'layers': priceAreas
#     }
# )


# # fig.update_layout(mapbox_style="open-street-map")
# # fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# # fig.update_layout(mapbox_bounds={"west": -180, "east": -50, "south": 20, "north": 90})

# st.plotly_chart(fig)


import streamlit as st
import plotly.express as px
import pandas as pd
import json
import plotly.graph_objects as go

# Load GeoJSON
with open(r'C:\Users\saraa\Documents\IND320_SMAA\project\data\file.geojson') as file:
    priceAreas = json.load(file)

# Create figure
fig = go.Figure()

# Add choropleth mapbox (even without data values, just for outlines)
fig.add_trace(go.Choroplethmapbox(
    geojson=priceAreas,
    locations=[],  # Empty since we just want outlines
    featureidkey="properties.id",  # Adjust based on your GeoJSON structure
    z=[],  # Empty data
    colorscale="Blues",  # Doesn't matter since no data
    showscale=False,  # Hide color scale
    marker_line_width=2,  # Outline width
    marker_opacity=0,  # Transparent fill
    marker_line_color="black"  # Outline color
))

# Update layout with mapbox style
fig.update_layout(
    mapbox_style="open-street-map",
    mapbox_zoom=10,
    mapbox_center={"lat": 40.7, "lat": -73.9},  # Adjust to your area
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.plotly_chart(fig)