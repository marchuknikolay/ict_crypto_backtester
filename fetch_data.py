import warnings
import pytz
import pandas as pd
import logging

from binance.client import Client
from binance.exceptions import BinanceAPIException

from constants import *

# Ignore specific warnings related to DataFrame concatenation
warnings.filterwarnings(
    'ignore', '.*DataFrame concatenation with empty or all-NA entries.*')

# Initialize logging for better debugging
logging.basicConfig(level=logging.ERROR)


def create_binance_client(api_key, api_secret):
    """Create and return a Binance Client instance."""
    try:
        client = Client(api_key=api_key, api_secret=api_secret)
        return client
    except Exception as e:
        logging.error(f"Error while creating Binance client: {e}")
        return None


def fetch_binance_data(symbol, interval, start_date, end_date):
    """
    Download historical cryptocurrency data from Binance.

    Parameters:
        symbol (str): Cryptocurrency symbol (e.g., 'BTCUSDT').
        interval (str): Kline interval (e.g., '1d', '1h').
        start_date (str): Start date in format 'YYYY-MM-DD'.
        end_date (str): End date in format 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: Historical data with columns for 'Open', 'High', 'Low', 'Close', 'Volume', etc.
    """
    # Create Binance client
    client = create_binance_client(API_KEY, API_SECRET)
    if not client:
        return pd.DataFrame()

    # Convert start and end dates to milliseconds
    start_ms = int(pd.to_datetime(start_date).timestamp() * 1000)
    end_ms = int(pd.to_datetime(end_date).timestamp() * 1000)

    logging.debug(
        f"Fetching data from {start_date} to {end_date} UTC for {symbol}.")

    try:
        # Fetch historical klines
        klines = client.futures_historical_klines(
            symbol, interval, start_ms, end_ms)
    except BinanceAPIException as e:
        logging.error(f"Error while fetching data from Binance: {e}")
        return pd.DataFrame()
    finally:
        client.close_connection()

    if not klines:
        logging.warning("No data fetched from Binance.")
        return pd.DataFrame()

    logging.debug(f"Successfully fetched {len(klines)} records.")

    # Define the column names
    columns = [
        'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote asset volume',
        'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
    ]

    # Create DataFrame
    data = pd.DataFrame(klines, columns=columns)

    # Convert timestamps to datetime and adjust timezone
    utc_zone = pytz.utc
    london_zone = pytz.timezone('Europe/Kyiv')

    data['Open Time'] = pd.to_datetime(data['Open Time'], unit='ms').dt.tz_localize(
        utc_zone).dt.tz_convert(london_zone)
    data['Close Time'] = pd.to_datetime(data['Close Time'], unit='ms').dt.tz_localize(
        utc_zone).dt.tz_convert(london_zone)

    # Convert numeric columns to float
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    data[numeric_columns] = data[numeric_columns].astype(float)

    return data
