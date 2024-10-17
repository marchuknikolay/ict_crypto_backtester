import pandas as pd
from constants import *


def is_swing_point(df, index, price_column, comparison_fn, window_size):
    """
    Generic function to check if the price at the given index is a swing point (high or low).

    Parameters:
    df (pd.DataFrame): Dataframe containing price data.
    index (int): Current index being evaluated.
    price_column (str): Column name ('High' or 'Low') to evaluate.
    comparison_fn (callable): Function to compare the current price with surrounding values (max or min).
    window_size (int): Number of candles to check before and after (fractal size).

    Returns:
    bool: True if the current index is a swing point, False otherwise.
    """
    if index < window_size - 1 or index > len(df) - window_size:
        return False

    return df[price_column][index] == comparison_fn(df[price_column][index - (window_size - 1):index + window_size])


def is_swing_high(df, index, fractal):
    """
    Check if the price at the given index is a swing high.

    Parameters:
    df (pd.DataFrame): Dataframe containing 'High' column.
    index (int): Current index being evaluated.
    fractal (Fractal): Fractal size (Fractal.THREE or Fractal.FIVE).

    Returns:
    bool: True if the current index is a swing high, False otherwise.
    """
    if fractal == Fractal.THREE:
        window_size = 2
    elif fractal == Fractal.FIVE:
        window_size = 3
    else:
        raise ValueError(
            'Unsupported fractal value. Use Fractal.THREE or Fractal.FIVE.')

    return is_swing_point(df, index, 'High', max, window_size)


def is_swing_low(df, index, fractal):
    """
    Check if the price at the given index is a swing low.

    Parameters:
    df (pd.DataFrame): Dataframe containing 'Low' column.
    index (int): Current index being evaluated.
    fractal (Fractal): Fractal size (Fractal.THREE or Fractal.FIVE).

    Returns:
    bool: True if the current index is a swing low, False otherwise.
    """
    if fractal == Fractal.THREE:
        window_size = 2
    elif fractal == Fractal.FIVE:
        window_size = 3
    else:
        raise ValueError(
            'Unsupported fractal value. Use Fractal.THREE or Fractal.FIVE.')

    return is_swing_point(df, index, 'Low', min, window_size)


def identify_swing_points(df, fractal):
    """
    Identify and return swing high and swing low points in the data.

    Parameters:
    df (pd.DataFrame): Dataframe containing 'High', 'Low', and 'Open Time' columns.
    fractal (Fractal): Fractal size (Fractal.THREE or Fractal.FIVE).

    Returns:
    pd.DataFrame: Dataframe containing swing points with columns 'Date', 'Price', and 'Type'.
    """
    if fractal not in Fractal:
        raise ValueError(
            'Unsupported fractal value. Use Fractal.THREE or Fractal.FIVE.')

    swing_points = []
    window = 1 if fractal == Fractal.THREE else 2

    for i in range(window, len(df) - window):
        if is_swing_high(df, i, fractal):
            swing_points.append(
                {'Date': df['Open Time'][i], 'Price': df['High'][i], 'Type': 'Swing High'})
        if is_swing_low(df, i, fractal):
            swing_points.append(
                {'Date': df['Open Time'][i], 'Price': df['Low'][i], 'Type': 'Swing Low'})

    return pd.DataFrame(swing_points)


def get_last_swing_point(df, bos_price, swing_type, price_condition):
    """
    Get the last swing point of the specified type (High or Low) that meets the price condition.

    Parameters:
    df (pd.DataFrame): Dataframe containing the market data.
    bos_price (float): Break of structure price used to filter swing points.
    swing_type (str): Either 'Swing High' or 'Swing Low' to specify the type of swing point.
    price_condition (callable): A lambda function that defines the price condition to filter swing points.

    Returns:
    pd.Series or None: The last swing point that meets the conditions, or None if none are found.
    """
    swing_points = identify_swing_points(df, FRACTAL)
    swing_points = swing_points[(swing_points['Type'] == swing_type) & (
        price_condition(swing_points['Price'], bos_price))]

    if swing_points.empty:
        return None

    return swing_points.iloc[-1]


def get_last_high_swing_point(df, bos_price):
    """
    Get the last 'Swing High' where the price is greater than the Break of Structure (bos_price).

    Parameters:
    df (pd.DataFrame): Dataframe containing the market data.
    bos_price (float): Break of structure price used to filter swing points.

    Returns:
    pd.Series or None: The last 'Swing High' that is greater than bos_price, or None if none found.
    """
    return get_last_swing_point(df, bos_price, 'Swing High', lambda price, bos_price: price > bos_price)


def get_last_low_swing_point(df, bos_price):
    """
    Get the last 'Swing Low' where the price is less than the Break of Structure (bos_price).

    Parameters:
    df (pd.DataFrame): Dataframe containing the market data.
    bos_price (float): Break of structure price used to filter swing points.

    Returns:
    pd.Series or None: The last 'Swing Low' that is less than bos_price, or None if none found.
    """
    return get_last_swing_point(df, bos_price, 'Swing Low', lambda price, bos_price: price < bos_price)
