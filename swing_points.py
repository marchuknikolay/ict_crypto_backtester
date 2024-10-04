import pandas as pd

'''def is_swing_high(df, index):
    if index < 2 or index > len(df) - 3:
        return False
    return df['High'][index] > max(df['High'][index-2:index]) and df['High'][index] > max(df['High'][index+1:index+3])

def is_swing_low(df, index):
    if index < 2 or index > len(df) - 3:
        return False
    return df['Low'][index] < min(df['Low'][index-2:index]) and df['Low'][index] < min(df['Low'][index+1:index+3])

def identify_swing_points(df):
    swings = []
    for i in range(2, len(df) - 2):
        if is_swing_high(df, i):
            swings.append({'Date': df['Open Time'][i], 'Price': df['High'][i], 'Type': 'Swing High'})
        elif is_swing_low(df, i):
            swings.append({'Date': df['Open Time'][i], 'Price': df['Low'][i], 'Type': 'Swing Low'})
    return pd.DataFrame(swings)'''

def is_swing_high(df, index):
    if index < 1 or index > len(df) - 2:
        return False
    return df['High'][index] > df['High'][index - 1] and df['High'][index] > df['High'][index + 1]

def is_swing_low(df, index):
    if index < 1 or index > len(df) - 2:
        return False
    return df['Low'][index] < df['Low'][index - 1] and df['Low'][index] < df['Low'][index + 1]

def identify_swing_points(df):
    swings = []
    for i in range(1, len(df) - 1):
        if is_swing_high(df, i):
            swings.append({'Date': df['Open Time'][i], 'Price': df['High'][i], 'Type': 'Swing High'})
        elif is_swing_low(df, i):
            swings.append({'Date': df['Open Time'][i], 'Price': df['Low'][i], 'Type': 'Swing Low'})
    return pd.DataFrame(swings)


def get_last_high_swing_point(df, bos_price):
    swing_points = identify_swing_points(df)
    swing_points = swing_points[(swing_points['Type'] == 'Swing High') & (swing_points['Price'] > bos_price)]
    if swing_points.empty:
        return None

    return swing_points.iloc[-1]

def get_last_low_swing_point(df, bos_price):
    swing_points = identify_swing_points(df)
    swing_points = swing_points[(swing_points['Type'] == 'Swing Low') & (swing_points['Price'] < bos_price)]
    if swing_points.empty:
        return None
        
    return swing_points.iloc[-1]