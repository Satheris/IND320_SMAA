import streamlit as st
import folium
from streamlit_folium import st_folium
import json



# Function to check if a point is inside a polygon
def point_in_polygon(point, polygon):
    # Simple point-in-polygon check
    x, y = point
    inside = False
    n = len(polygon)
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Function to find which region contains the clicked point
def find_region_for_point(lat, lng, geojson_data):
    for feature in geojson_data['features']:
        geometry = feature['geometry']
        if geometry['type'] == 'Polygon':
            for polygon in geometry['coordinates']:
                if point_in_polygon([lng, lat], polygon):
                    return feature['properties'].get('ElSpotOmr', 'Unknown Region'), feature
        elif geometry['type'] == 'MultiPolygon':
            for multipolygon in geometry['coordinates']:
                for polygon in multipolygon:
                    if point_in_polygon([lng, lat], polygon):
                        return feature['properties'].get('ElSpotOmr', 'Unknown Region'), feature
    return None, None