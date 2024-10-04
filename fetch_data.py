import time
import warnings
from datetime import timedelta, datetime
import pytz

import numpy as np
from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd
import logging

# ignore certain warnings
warnings.filterwarnings('ignore', '.*DataFrame concatenation with empty or all-NA entries.*', )

def fetch_binance_data(symbol, interval, start_date, end_date):
    """Download historical cryptocurrency data from Binance."""
    # Initialize the Binance client
    try:
        client = Client(api_key='oNKmJsFdyUF0vlM029zXAtiDf6ndz9CoWQEnklsavqLIfcSKjmMru8tAGILm4Ao7', api_secret='dOKdybi7Uidh3bVyzgvM87nzqR4ExxdCdVczDWN831Gtl4f2irEoggB68YCZqvPD')
    except Exception as e:
        print(f"Error encountered while creating client: {e}")
        return pd.DataFrame()
        
    # Convert start_date to milliseconds
    start_str = int(pd.to_datetime(start_date).timestamp() * 1000)

    # Convert end_date to milliseconds
    end_str = int(pd.to_datetime(end_date).timestamp() * 1000)

    logging.debug(f"Fetching data from {start_date} to {end_date} UTC")

    try:
        # Fetch klines for the specified symbol and interval
        klines = client.futures_historical_klines(symbol, interval, start_str, end_str)

        client.close_connection()

    except BinanceAPIException as e:
        print(f"Error encountered while fetching data: {e}")
        # return just the empty dataframe
        return pd.DataFrame()

    if klines:
        logging.debug(f"Data fetched successfully: {len(klines)} records.")
    else:
        logging.debug("No data fetched.")
        
    # Convert to DataFrame
    columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time','Quote asset volume', 'Number of trades', 'Taker buy base asset volume','Taker buy quote asset volume', 'Ignore']    
    data = pd.DataFrame(klines, columns=columns)

    # Convert timestamp to datetime in UTC and then convert to London timezone
    utc_zone = pytz.utc
    london_zone = pytz.timezone('Europe/London')

    data['Open Time'] = pd.to_datetime(data['Open Time'], unit='ms').dt.tz_localize(utc_zone).dt.tz_convert(london_zone)
    data['Close Time'] = pd.to_datetime(data['Close Time'], unit='ms').dt.tz_localize(utc_zone).dt.tz_convert(london_zone)

    # Convert numeric columns to floats
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    data[numeric_columns] = data[numeric_columns].astype(float)

    return data