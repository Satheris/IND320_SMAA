# utils/common.py

import streamlit as st
import pandas as pd
import pymongo
import numpy as np
import json

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

import openmeteo_requests
import requests_cache
from retry_requests import retry

from scipy.fft import dct, idct
from scipy.stats import median_abs_deviation
from scipy.signal import stft
from statsmodels.tsa.seasonal import STL
from sklearn.neighbors import LocalOutlierFactor


# ----------------------------------------------------------------
# DOWNLOADS
# ----------------------------------------------------------------

@st.cache_data(show_spinner=True)
def read_data() -> pd.DataFrame:
    data = pd.read_csv('project/data/open-meteo-subset.csv')
    data['time'] = pd.to_datetime(data['time'])
    return data


@st.cache_data(show_spinner=True)
def openmeteo_download(area, year=2021) -> pd.DataFrame:
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    longitude, latitude = area_to_geoplacement(area)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": f"{year}-01-01",
        "end_date": f"{year}-12-31",
        "hourly": ["temperature_2m", "wind_direction_10m", "wind_speed_10m", "wind_gusts_10m", "precipitation"],
        "models": "era5",
        "timezone": "Europe/Berlin",
        "wind_speed_unit": "ms"}
    
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]    

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(1).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(3).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()

    hourly_data = {"time": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True).tz_convert('Europe/Oslo'),
        end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True).tz_convert('Europe/Oslo'),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left")}

    hourly_data["temperature_2m (°C)"] = hourly_temperature_2m
    hourly_data["wind_direction_10m (°)"] = hourly_wind_direction_10m
    hourly_data["wind_speed_10m (m/s)"] = hourly_wind_speed_10m
    hourly_data["wind_gusts_10m (m/s)"] = hourly_wind_gusts_10m
    hourly_data["precipitation (mm)"] = hourly_precipitation

    df = pd.DataFrame(data = hourly_data)

    return df


@st.cache_data(show_spinner=True)
def openmeteo_download_snowdrift(location, startYear=2021, endYear=2022) -> pd.DataFrame:
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    latitude, longitude = location

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": f"{startYear}-07-01",
        "end_date": f"{endYear}-06-30",
        "hourly": ["temperature_2m", "wind_direction_10m", "wind_speed_10m", "wind_gusts_10m", "precipitation"],
        "models": "era5",
        "timezone": "Europe/Berlin",
        "wind_speed_unit": "ms"}
    
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]    

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(1).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(3).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()

    hourly_data = {"time": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True), # .tz_convert('Europe/Oslo'),
        end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True), # .tz_convert('Europe/Oslo'),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left")}
    
    hourly_data['time'] = pd.to_datetime(hourly_data['time']).tz_localize(None) + pd.Timedelta(hours=1)

    hourly_data["temperature_2m (°C)"] = hourly_temperature_2m
    hourly_data["wind_direction_10m (°)"] = hourly_wind_direction_10m
    hourly_data["wind_speed_10m (m/s)"] = hourly_wind_speed_10m
    hourly_data["wind_gusts_10m (m/s)"] = hourly_wind_gusts_10m
    hourly_data["precipitation (mm)"] = hourly_precipitation

    df = pd.DataFrame(data = hourly_data)

    return df    


@st.cache_resource
def init_connection() -> pymongo.MongoClient:
    return pymongo.MongoClient(st.secrets['mongo']['uri'])


# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_elhubdata(energy_type) -> pd.DataFrame:
    client = init_connection()
    db = client['project']
    collection = db['elhub_' + energy_type]
    items = collection.find()
    items = list(items)

    # Converting data to dataframe and doing type conversion
    df_elhub = pd.DataFrame(items)
    df_elhub['startTime'] = pd.to_datetime(df_elhub['startTime'], errors='coerce', utc=True)
    df_elhub['quantityKwh'] = pd.to_numeric(df_elhub['quantityKwh'], errors='coerce')
    df_elhub['month'] = df_elhub['startTime'].dt.month
    df_elhub['year'] = df_elhub['startTime'].dt.year

    df_elhub = df_elhub[df_elhub['year'] == 2021]

    return df_elhub



# ----------------------------------------------------------------
# REPLACE st.sesstion_state
# ----------------------------------------------------------------

def _set_new_area() -> None:
    st.session_state.AREA = st.session_state.area
    _download_new_area()

def _download_new_area() -> None:
    st.session_state.data = openmeteo_download(area=st.session_state.AREA)

def _set_new_group(groups) -> None:
    st.session_state.GROUP_INDEX = groups.index(st.session_state.group)



# ----------------------------------------------------------------
# ANALYSIS PLOTTERS
# ----------------------------------------------------------------

def STL_plotter(df_elhub, area='NO1', prodGroup='hydro', periodLength=24*7, 
                seasonalSmoother=13, trendSmoother=365, robust=True):

    sub_df_elhub = make_elhub_subset(df_elhub, area, prodGroup)

    stl = STL(sub_df_elhub['quantityKwh'], period=periodLength, 
            seasonal=seasonalSmoother, trend=trendSmoother, robust=robust)
    res = stl.fit()

    #plotting with plotly
    fig = make_subplots(
            rows=4, cols=1, 
            subplot_titles=["Observed", "Trend", "Seasonal", "Residuals"])
    fig.add_trace(
        go.Scatter(x=res.seasonal.index, y=res.observed, mode='lines', line=dict(color="#a234e7")),
            row=1, col=1)
    fig.add_trace(
        go.Scatter(x=res.trend.index, y=res.trend, mode='lines', line=dict(color="#19a222")),
            row=2, col=1)
    fig.add_trace(
        go.Scatter(x=res.seasonal.index, y=res.seasonal, mode='lines', line=dict(color="#28a8ed")),
            row=3, col=1)
    fig.add_trace(
        go.Scatter(x=res.resid.index, y=res.resid, mode='lines', line=dict(color="#c22535")),
            row=4, col=1)
    fig.update_layout(title_text=f'STL analysis for Energy Production in area {area} for {prodGroup}',
                      autosize=False,
                      width=300,
                      height=700,
                      margin=dict(l=60, r=60, t=20, b=20, pad=5))

    st.plotly_chart(fig)


def STFT_plotter(df_elhub, area='NO1', prodGroup='wind', fs=1/3600, nperseg=24*7, noverlap=None):

    sub_df_elhub = make_elhub_subset(df_elhub, area, prodGroup)

    # Extract the values for STFT
    data = sub_df_elhub['quantityKwh'].values

    # Compute STFT
    frequencies, times, Zxx = stft(data, fs=fs, nperseg=nperseg, noverlap=noverlap, window='hann')

    # Convert magnitude to dB scale for better visualization
    magnitude = np.abs(Zxx)
    magnitude_db = 20 * np.log10(magnitude + 1e-10)  # Add small value to avoid log(0)

    # Create the spectrogram plot
    fig = go.Figure()

    # Create the heatmap (spectrogram)
    fig.add_trace(go.Heatmap(
        x=times / (24 * 3600),  # Convert seconds to days for x-axis
        y=frequencies * (24 * 3600),  # Convert Hz to cycles per day for y-axis
        z=magnitude_db,
        colorscale='Viridis',
        colorbar=dict(title="Magnitude (dB)"),
        hovertemplate='Time: %{x:.1f} days<br>Frequency: %{y:.3f} cycles/day<br>Magnitude: %{z:.2f} dB<extra></extra>'
    ))

    # Update layout
    fig.update_layout(
        title=f'Spectrogram of Energy Production in area {area} for {prodGroup}',
        xaxis_title='Time (days)',
        yaxis_title='Frequency (cycles per day)',
        height=500, 
        width=800,
    )

    # Show the plot
    st.plotly_chart(fig)


def SPC_outlier_plot(df, column, dct_cutoff=10, n_std=3):
    # DCT of chosen variable -> transform to frequency domain
    df_copy = df.copy()
    dct_coefs = dct(df_copy[column])

    # saving seasonal variation in low-pass filtering -> transform back to signal domain
    dct_coefs_lowpass = dct_coefs.copy()
    dct_coefs_lowpass[dct_cutoff:] = 0
    seasonal_variation = idct(dct_coefs_lowpass)

    # performing high-pass filtering -> transform back to signal domain
    dct_coefs_highpass = dct_coefs.copy()
    dct_coefs_highpass[:dct_cutoff] = 0
    satv = idct(dct_coefs_highpass)

    # finding the median absolute deviation (MAD) based on SATV
    MAD = median_abs_deviation(satv)

    # finding lower and upper bounds for the expected variation in year scale
    df_copy['upper_bound'] = np.add(seasonal_variation, n_std*MAD)
    df_copy['lower_bound'] = np.add(seasonal_variation, (-n_std)*MAD)

    # marking outliers in a separate column and removing data from inlier positions
    df_copy['outliers'] = df_copy[column].copy()
    df_copy.loc[((df_copy[column] < df_copy['upper_bound']) & 
                    (df_copy[column] > df_copy['lower_bound'])), 
                    'outliers'] = None

    # line plot with temperature in original scale, upper and lower outlier bounds in original scale and outliers marked
    fig = px.line(df_copy, x='time', y=[column, 'outliers', 'upper_bound', 'lower_bound'], template='plotly')
    st.plotly_chart(fig)

    # output statistics
    st.write(f'Number of outliers found: {(df_copy["outliers"].count())}')
    st.write(f'Percentage of outliers: {(df_copy["outliers"].count())/len(df_copy["outliers"]):.3f}%')


def LOF_stats_plot(df:pd.DataFrame, column, contamination=0.01, n_neighbors=20):
    lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)

    # making a reduced dataframe for analysis
    df_reduced = pd.DataFrame(df[column])
    df_reduced['date'] = df['time']
    df_reduced['hour'] = pd.to_datetime(df_reduced['date']).dt.hour
    df_reduced['day_of_year'] = pd.to_datetime(df_reduced['date']).dt.dayofyear

    # Use both precipitation and time features (else LOF gets confused)
    features = df_reduced[[column, 'hour', 'day_of_year']]
    pred_labels = lof.fit_predict(features)

    # convert (-1) to 0 -> bincount needs non-negative numbers
    pred_labels[pred_labels == -1] = 0
    
    # converting outlier information into dataframe format
    df_reduced['category'] = pred_labels
    df_reduced['outliers'] = df_reduced[column].copy()
    df_reduced.loc[(df_reduced['category'] == 1), 'outliers'] = None

    # plotting with the outlier data
    fig = px.scatter(df_reduced, x='date', y=[column, 'outliers'], template='plotly')
    st.plotly_chart(fig)

    # print for analysis results
    counts = np.bincount(pred_labels)
    st.write(f'LocalOutlierFactor found {counts[0]} outliers out of {sum(counts)} data points')
    st.write(f'The proportion of outliers is {counts[0]/sum(counts)*100:.3f}%')    


def SWC_plot(weather_variable, energy_type, window_length):

    agg_data = st.session_state[energy_type+'_data'].groupby('startTime').sum().reset_index()
    energyKwh = agg_data['quantityKwh']


    weather_series = st.session_state['weather_data'][weather_variable]

    # Calculate rolling correlation
    Quantity_weather_SWC = energyKwh.rolling(window_length, center=True).corr(weather_series)


    # Create slider for center point
    max_center = len(energyKwh) - window_length//2
    center = st.slider(
        "Select center point:",
        min_value=window_length//2,
        max_value=max_center,
        value=min(window_length//2, max_center),
        step=1
    )

    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(energy_type, weather_variable, 'Sliding Window Correlation'),
        vertical_spacing=0.08,
        shared_xaxes=True
    )

    # Add PerEURO trace
    fig.add_trace(
        go.Scatter(
            x=energyKwh.index,
            y=energyKwh,
            mode='lines',
            name=energy_type,
            line=dict(color='blue')
        ),
        row=1, col=1
    )

    # Highlight window for PerEURO
    window_start = center - 22
    window_end = center + 22
    fig.add_trace(
        go.Scatter(
            x=energyKwh.index[window_start:window_end],
            y=energyKwh.iloc[window_start:window_end],
            mode='lines',
            name=f'{energy_type} Window',
            line=dict(color='red', width=2)
        ),
        row=1, col=1
    )

    # Add ExpNatGas trace
    fig.add_trace(
        go.Scatter(
            x=weather_series.index,
            y=weather_series,
            mode='lines',
            name=weather_variable,
            line=dict(color='green')
        ),
        row=2, col=1
    )

    # Highlight window for ExpNatGas
    fig.add_trace(
        go.Scatter(
            x=weather_series.index[window_start:window_end],
            y=weather_series.iloc[window_start:window_end],
            mode='lines',
            name=f'{weather_variable} Window',
            line=dict(color='red', width=2)
        ),
        row=2, col=1
    )

    # Add SWC trace
    fig.add_trace(
        go.Scatter(
            x=energyKwh.index,
            y=Quantity_weather_SWC,
            mode='lines',
            name='SWC',
            line=dict(color='purple')
        ),
        row=3, col=1
    )

    # Add center point marker for SWC
    fig.add_trace(
        go.Scatter(
            x=[energyKwh.index[center]],
            y=[Quantity_weather_SWC.iloc[center]],
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
    fig.update_yaxes(title_text=f"{energy_type}", row=1, col=1)
    fig.update_yaxes(title_text=f"{weather_variable}", row=2, col=1)
    fig.update_yaxes(title_text="SWC", row=3, col=1, range=[-1, 1])
    fig.update_xaxes(title_text="Time", row=3, col=1)

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Display correlation value at center point
    # st.metric(
    #     label=f"Correlation at center point ({OilExchange.index[center].strftime('%Y-%m-%d') if hasattr(OilExchange.index, 'strftime') else center})",
    #     value=f"{PerEURO_ExpNatGas_SWC.iloc[center]:.3f}"
    # )




# ----------------------------------------------------------------
# MAP HELPERS
# ----------------------------------------------------------------

def map_outline(df=None):
    with open(r'project/data/file.geojson') as file:
        priceAreas = json.load(file)

    if df == None:
        # making dummy df with area identifiers
        area_ids = [feature['properties']['OBJECTID'] for feature in priceAreas['features']]
        area_names = [feature['properties']['ElSpotOmr'] for feature in priceAreas['features']]
        df = pd.DataFrame({'area_id': area_ids, 
                        'dummy_value': [1]*len(area_ids),
                        'area_names': area_names})

    # Create the map
    fig = px.choropleth_map(
        df,
        geojson=priceAreas,
        locations='area_id',
        featureidkey="properties.OBJECTID",
        color='dummy_value',
        color_continuous_scale=[(0, "rgba(0,0,0,0)"), (1, "rgba(0,0,0,0)")],  # Transparent colors
        map_style="open-street-map",
        zoom=3.5,
        center={"lat": 65.0, "lon": 16.0},
        labels={'dummy_value': ''},
        hover_data={'area_names':True}
        )

    # Customize outlines
    fig.update_traces(
        marker_line_width=2,
        marker_line_color="#e8862a",
        )
    
    fig.update_traces(
        selected=dict(marker=dict(opacity=0.7)), #color="#2ca02c", 
        unselected=dict(marker=dict(opacity=0))
    )
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      coloraxis_showscale=False,  # Explicitly hide color scale in layout
                      height=575,
                      width=450
                      )

    return fig


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



# ----------------------------------------------------------------
# SUBSET HELPER
# ----------------------------------------------------------------

def make_elhub_subset(df_elhub, area='NO1', prodGroup='hydro') -> pd.DataFrame:
    # making subset of data 
    sub_df_elhub = df_elhub[(df_elhub['priceArea'] == area) & (df_elhub['productionGroup'] == prodGroup)]
    sub_df_elhub = pd.DataFrame(sub_df_elhub[['quantityKwh', 'startTime']])
    sub_df_elhub['startTime'] = pd.to_datetime(sub_df_elhub['startTime'], utc=True, errors='coerce').dt.tz_localize(None)

    # adding 1 hour because (utc=True) displaced the time
    sub_df_elhub['startTime'] = sub_df_elhub['startTime'] + pd.Timedelta(hours=1)

    # Let's make sure the index is properly set as datetime
    if not isinstance(sub_df_elhub.index, pd.DatetimeIndex):
        # If your time column is called 'startTime' and it's not the index
        sub_df_elhub = sub_df_elhub.set_index('startTime')
        
    # Ensure the index is timezone-naive if it has timezone info
    if sub_df_elhub.index.tz is not None:
        sub_df_elhub.index = sub_df_elhub.index.tz_localize(None)


    # Ensure the data is sorted by time and has regular hourly frequency
    sub_df_elhub = sub_df_elhub.sort_index()
    sub_df_elhub = sub_df_elhub.asfreq('h')  # Ensure hourly frequency

    # Handle any missing values if necessary
    sub_df_elhub['quantityKwh'] = sub_df_elhub['quantityKwh'].interpolate()

    return sub_df_elhub



# ----------------------------------------------------------------
# GEO HELPER
# ----------------------------------------------------------------

def area_to_geoplacement(area):
    geo_dict = {'NO1': {'long': 10.7461, 'lat': 59.9127},
                'NO2': {'long': 7.9956, 'lat': 58.1467},
                'NO3': {'long': 5.3242, 'lat': 60.393},
                'NO4': {'long': 18.9551, 'lat': 69.6489},
                'NO5': {'long': 10.3951, 'lat': 63.4305}}
    
    return geo_dict[area]['long'], geo_dict[area]['lat']



# ----------------------------------------------------------------
# MONTH HELPERS
# ----------------------------------------------------------------

def generate_months() -> list:
    months =   ['January', 'February', 'March',
                'April', 'May', 'June',
                'July', 'August', 'September',
                'October', 'November', 'December']
    return months

def month_start_converter(month_text: str) -> str:
    month_dict = {'January': '2021-01-01',
                    'February': '2021-02-01',
                    'March': '2021-03-01',
                    'April': '2021-04-01', 
                    'May': '2021-05-01',
                    'June': '2021-06-01',
                    'July': '2021-07-01',
                    'August': '2021-08-01',
                    'September': '2021-09-01',
                    'October': '2021-10-01',
                    'November': '2021-11-01',
                    'December': '2021-12-01'}
    return month_dict[month_text]

def month_end_converter(month_text: str) -> str:
    month_dict = {'January': '2021-02-01',
                    'February': '2021-03-01',
                    'March': '2021-04-01',
                    'April': '2021-05-01', 
                    'May': '2021-06-01',
                    'June': '2021-07-01',
                    'July': '2021-08-01',
                    'August': '2021-09-01',
                    'September': '2021-10-01',
                    'October': '2021-11-01',
                    'November': '2021-12-01',
                    'December': '2021-01-01'}
    return month_dict[month_text]

def month_number_converter(month_text: str) -> int:
    month_dict = {'January': 1,
                    'February': 2,
                    'March': 3,
                    'April': 4,
                    'May': 5,
                    'June': 6,
                    'July': 7,
                    'August': 8,
                    'September': 9,
                    'October': 10,
                    'November': 11,
                    'December': 12}
    return month_dict[month_text]