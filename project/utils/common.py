# utils/common.py
import streamlit as st
import pandas as pd
import pymongo

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

import openmeteo_requests
import requests_cache
from retry_requests import retry

from scipy.fft import dct, idct
from scipy.stats import median_abs_deviation
from statsmodels.tsa.seasonal import STL
# from sklearn.neighbors import LocalOutlierFactor


# ----------------------------------------------------------------
# DOWNLOADS
# ----------------------------------------------------------------
@st.cache_data(show_spinner=True)
def read_data() -> pd.DataFrame:
    data = pd.read_csv('project/data/open-meteo-subset.csv')
    data['time'] = pd.to_datetime(data['time'])
    return data


@st.cache_data(show_spinner=True)
def openmeteo_download(area, year=2021):
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
        "hourly": ["temperature_2m", "precipitation", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
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

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
    hourly_data["precipitation"] = hourly_precipitation

    df = pd.DataFrame(data = hourly_data)

    return df



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
    month_dict = {'January': '2020-01-01',
                    'February': '2020-02-01',
                    'March': '2020-03-01',
                    'April': '2020-04-01', 
                    'May': '2020-05-01',
                    'June': '2020-06-01',
                    'July': '2020-07-01',
                    'August': '2020-08-01',
                    'September': '2020-09-01',
                    'October': '2020-10-01',
                    'November': '2020-11-01',
                    'December': '2020-12-01'}
    return month_dict[month_text]

def month_end_converter(month_text: str) -> str:
    month_dict = {'January': '2020-02-01',
                    'February': '2020-03-01',
                    'March': '2020-04-01',
                    'April': '2020-05-01', 
                    'May': '2020-06-01',
                    'June': '2020-07-01',
                    'July': '2020-08-01',
                    'August': '2020-09-01',
                    'September': '2020-10-01',
                    'October': '2020-11-01',
                    'November': '2020-12-01',
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