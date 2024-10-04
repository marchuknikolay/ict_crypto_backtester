import numpy as np
import pandas as pd
import logging
from swing_points import *

def identify_break_of_structure(df, swing_points):
    """
    Identify Break of Structure (BOS) when a candle closes above a swing high
    or below a swing low. Ensures only one BOS per swing point.

    Parameters:
    - df (pd.DataFrame): The historical price data.
    - swing_points (pd.DataFrame): Identified swing points.

    Returns:
    - pd.DataFrame: DataFrame containing BOS events.
    """
    bos_events = []

    for i, swing in swing_points.iterrows():
        # Filter subsequent candles after the swing point
        subsequent_candles = df[df['Open Time'] > swing['Date']].reset_index(drop=True)

        if swing['Type'] == 'Swing High':
            # Find the first candle where Close > swing['Price']
            bos_candles = subsequent_candles[subsequent_candles['Close'] > swing['Price']]
            if not bos_candles.empty:
                bos_candle = bos_candles.iloc[0]
                bos_events.append({
                    'BOS DateTime': swing['Date'],
                    'BOS Price': swing['Price'],
                    'BOS Type': swing['Type'],
                    'Break DateTime': bos_candle['Open Time'],
                    'Break Price': bos_candle['Close'],
                    'Break Type': 'BOS High'
                })
                logging.debug(f"BOS High detected for swing on {swing['Date']} at price {swing['Price']}.")

        elif swing['Type'] == 'Swing Low':
            # Find the first candle where Close < swing['Price']
            bos_candles = subsequent_candles[subsequent_candles['Close'] < swing['Price']]
            if not bos_candles.empty:
                bos_candle = bos_candles.iloc[0]
                bos_events.append({
                    'BOS DateTime': swing['Date'],
                    'BOS Price': swing['Price'],
                    'BOS Type': swing['Type'],
                    'Break DateTime': bos_candle['Open Time'],
                    'Break Price': bos_candle['Close'],
                    'Break Type': 'BOS Low'
                })
                logging.debug(f"BOS Low detected for swing on {swing['Date']} at price {swing['Price']}.")

    # Convert the list of BOS events to a DataFrame
    bos_df = pd.DataFrame(bos_events)

    # Optional: Reset index for clarity
    bos_df.reset_index(drop=True, inplace=True)

    logging.info(f"Identified {len(bos_df)} Break of Structure events.")
    return bos_df

def get_first_bullish_bos(df):
    current_swing_high = None  # Initialize to ensure it's defined before use

    for i in range(0, len(df) - 1):
        if current_swing_high is not None and df['Close'][i] > current_swing_high['High']:
            return {
                'Bos Date': df['Open Time'][i + 1],
                'Bos Price': current_swing_high['High'],
                'Candle Close Price': df['Close'][i]
            }

        if is_swing_high(df, i):
            current_swing_high = df.iloc[i]

def get_first_bearish_bos(df):
    current_swing_low = None  # Initialize to ensure it's defined before use

    for i in range(0, len(df) - 1):
        if current_swing_low is not None and df['Close'][i] < current_swing_low['Low']:
            return {
                'Bos Date': df['Open Time'][i + 1],
                'Bos Price': current_swing_low['Low'],
                'Candle Close Price': df['Close'][i]
            }

        if is_swing_low(df, i):
            current_swing_low = df.iloc[i]

