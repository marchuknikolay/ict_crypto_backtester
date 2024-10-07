from swing_points import is_swing_high, is_swing_low
from constants import FRACTAL

def get_first_bullish_bos(df):
    """
    Identify the first bullish Break of Structure (BoS).

    A BoS occurs when the price closes above a prior swing high.

    Parameters:
        df (pd.DataFrame): DataFrame containing price data with 'Open Time', 'High', and 'Close' columns.

    Returns:
        dict: Details of the bullish BoS, including the BoS date, BoS price, and candle close price.
    """
    current_swing_high = None

    for i in range(len(df) - 1):
        # Check if there's a BoS (close above swing high)
        if current_swing_high is not None and df['Close'][i] > current_swing_high['High']:
            return {
                'Bos Date': df['Open Time'][i + 1],
                'Bos Price': current_swing_high['High'],
                'Candle Close Price': df['Close'][i]
            }

        # Update current swing high if a new one is identified
        if is_swing_high(df, i, FRACTAL):
            current_swing_high = df.iloc[i]

    return None  # Return None if no bullish BoS is found

def get_first_bearish_bos(df):
    """
    Identify the first bearish Break of Structure (BoS).

    A BoS occurs when the price closes below a prior swing low.

    Parameters:
        df (pd.DataFrame): DataFrame containing price data with 'Open Time', 'Low', and 'Close' columns.

    Returns:
        dict: Details of the bearish BoS, including the BoS date, BoS price, and candle close price.
    """
    current_swing_low = None

    for i in range(len(df) - 1):
        # Check if there's a BoS (close below swing low)
        if current_swing_low is not None and df['Close'][i] < current_swing_low['Low']:
            return {
                'Bos Date': df['Open Time'][i + 1],
                'Bos Price': current_swing_low['Low'],
                'Candle Close Price': df['Close'][i]
            }

        # Update current swing low if a new one is identified
        if is_swing_low(df, i, FRACTAL):
            current_swing_low = df.iloc[i]

    return None  # Return None if no bearish BoS is found