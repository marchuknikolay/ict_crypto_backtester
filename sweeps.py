import pandas as pd

def identify_liquidity_sweeps(df, swing_points):
    """
    Identifies liquidity sweeps by comparing swing points (highs and lows) with subsequent price movements.

    Parameters:
        df (pd.DataFrame): DataFrame containing the price data with 'Open Time', 'High', 'Low', 'Close', and 'Close Time' columns.
        swing_points (pd.DataFrame): DataFrame containing identified swing points with 'Date', 'Price', and 'Type' columns.

    Returns:
        pd.DataFrame: DataFrame containing information about the identified liquidity sweeps.
    """
    sweeps = []
    for _, swing in swing_points.iterrows():
        # Filter for subsequent candles after the current swing point
        subsequent_candles = df[df['Open Time'] > swing['Date']].reset_index(drop=True)
        
        if swing['Type'] == 'Swing High':
            # Cumulative max of 'High' prices after the swing point
            cum_high_below_swing = subsequent_candles['High'].cummax() <= swing['Price']

            # Find the first index where the cumulative max exceeds the swing price
            first_breach_idx = cum_high_below_swing.idxmin() if not cum_high_below_swing.all() else None

            # Check for liquidity sweep conditions (price breach and subsequent close below swing price)
            if first_breach_idx is not None and subsequent_candles.at[first_breach_idx, 'High'] > swing['Price'] and subsequent_candles.at[first_breach_idx, 'Close'] < swing['Price']:
                sweeps.append({
                    'Swept DateTime': swing['Date'],
                    'Swept Price': swing['Price'],
                    'Swept Type': swing['Type'],
                    'Sweep DateTime': subsequent_candles.at[first_breach_idx, 'Close Time'],
                    'Sweep Price': subsequent_candles.at[first_breach_idx, 'High'],
                    'Sweep Type': 'Liquidity Sweep High'
                })

        elif swing['Type'] == 'Swing Low':
            # Cumulative min of 'Low' prices after the swing point
            cum_low_above_swing = subsequent_candles['Low'].cummin() >= swing['Price']
            
            # Find the first index where the cumulative min goes below the swing price
            first_breach_idx = cum_low_above_swing.idxmin() if not cum_low_above_swing.all() else None

            # Check for liquidity sweep conditions (price breach and subsequent close above swing price)
            if first_breach_idx is not None and subsequent_candles.at[first_breach_idx, 'Low'] < swing['Price'] and subsequent_candles.at[first_breach_idx, 'Close'] > swing['Price']:
                sweeps.append({
                    'Swept DateTime': swing['Date'],
                    'Swept Price': swing['Price'],
                    'Swept Type': swing['Type'],
                    'Sweep DateTime': subsequent_candles.at[first_breach_idx, 'Close Time'],
                    'Sweep Price': subsequent_candles.at[first_breach_idx, 'Low'],
                    'Sweep Type': 'Liquidity Sweep Low'
                })

    return pd.DataFrame(sweeps)
