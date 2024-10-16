from fetch_data import *
from swing_points import *
from sweeps import *
from boses import *
from constants import *

def get_largest_streak(df, result_type):
    """
    Identifies the largest streak of consecutive 'Win' or 'Lose' results.

    Parameters:
        df (pd.DataFrame): DataFrame containing the 'Result' column with 'Win' or 'Lose' entries.
        result_type (str): The result type to evaluate ('Win' or 'Lose').

    Returns:
        int: The length of the largest consecutive streak of the specified result type.
    """
    max_streak = 0
    current_streak = 0

    for _, entry in df.iterrows():
        if entry['Result'] == result_type:
            current_streak += 1
        else:
            max_streak = max(max_streak, current_streak)
            current_streak = 0

    # Final check for the last streak
    return max(max_streak, current_streak)

def get_largest_winstreak(df):
    """
    Identifies the largest winning streak.

    Parameters:
        df (pd.DataFrame): DataFrame containing the 'Result' column.

    Returns:
        int: The length of the largest consecutive winning streak.
    """
    return get_largest_streak(df, 'Win')

def get_largest_losestreak(df):
    """
    Identifies the largest losing streak.

    Parameters:
        df (pd.DataFrame): DataFrame containing the 'Result' column.

    Returns:
        int: The length of the largest consecutive losing streak.
    """
    return get_largest_streak(df, 'Lose')

def get_winrate(df, entry_type):
    """
    Calculates the win rate for a specific entry type ('Long' or 'Short').

    Parameters:
        df (pd.DataFrame): DataFrame containing 'Entry Type' and 'Result' columns.
        entry_type (str): The type of entry to evaluate ('Long' or 'Short').

    Returns:
        int: The win rate as a percentage (rounded to the nearest integer).
    """
    count = 0
    win_count = 0

    for _, entry in df.iterrows():
        if entry['Entry Type'] == entry_type:
            count += 1
            if entry['Result'] == 'Win':
                win_count += 1

    if count == 0:
        return 0

    return round(win_count / count * 100)

def get_long_winrate(df):
    """
    Calculates the win rate for 'Long' entries.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'Entry Type' and 'Result' columns.

    Returns:
        int: The win rate for 'Long' entries as a percentage.
    """
    return get_winrate(df, 'Long')

def get_short_winrate(df):
    """
    Calculates the win rate for 'Short' entries.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'Entry Type' and 'Result' columns.

    Returns:
        int: The win rate for 'Short' entries as a percentage.
    """
    return get_winrate(df, 'Short')

def get_take_profit(entry_price, stop_loss, coefficient):
    """
    Calculates the take profit level based on the entry price, stop loss, and a risk reward coefficient.

    Parameters:
        entry_price (float): The entry price of the trade.
        stop_loss (float): The stop loss price.
        coefficient (float): The risk reward coefficient.

    Returns:
        float: The calculated take profit price.
    """
    diff = coefficient * abs(entry_price - stop_loss)
    return entry_price - diff if entry_price < stop_loss else entry_price + diff

def get_trade_result(df, entry_type, take_profit, stop_loss):
    """
    Determines the result of a trade based on the entry type, take profit, and stop loss levels.

    Parameters:
        df (pd.DataFrame): DataFrame containing market data with 'High', 'Low', and 'Open Time' columns.
        entry_type (str): The type of trade entry ('Long' or 'Short').
        take_profit (float): The take profit price level.
        stop_loss (float): The stop loss price level.

    Returns:
        dict or None: A dictionary containing the trade result and result date, or None if no result.
    """
    # Set conditions based on entry type
    if entry_type == 'Short':
        tp_condition = df['Low'] <= take_profit
        sl_condition = df['High'] >= stop_loss
    elif entry_type == 'Long':
        tp_condition = df['High'] >= take_profit
        sl_condition = df['Low'] <= stop_loss
    else:
        return None  # Invalid entry type

    # Find the first occurrence of take profit or stop loss
    take_profit_reached = df[tp_condition].reset_index(drop=True).iloc[0] if not df[tp_condition].empty else None
    stop_loss_reached = df[sl_condition].reset_index(drop=True).iloc[0] if not df[sl_condition].empty else None

    # Determine the trade outcome
    if take_profit_reached is not None and stop_loss_reached is not None:
        if take_profit_reached['Open Time'] < stop_loss_reached['Open Time']:
            return {'Result': 'Win', 'Result Date': take_profit_reached['Open Time']}
        else:
            return {'Result': 'Lose', 'Result Date': stop_loss_reached['Open Time']}
    elif take_profit_reached is not None:
        return {'Result': 'Win', 'Result Date': take_profit_reached['Open Time']}
    elif stop_loss_reached is not None:
        return {'Result': 'Lose', 'Result Date': stop_loss_reached['Open Time']}
    
    return None

def get_entries(htf, ltf, coefficient):
    """
    Generate trade entries based on liquidity sweeps and break of structure (BOS).

    Parameters:
    htf (str): High timeframe.
    ltf (str): Low timeframe.
    coefficient (float): Coefficient for calculating take profit.

    Returns:
    pd.DataFrame: DataFrame containing the generated trade entries.
    """
    # Fetch data for high and low timeframes
    data_htf = fetch_binance_data(TICKER, htf, START_DATE, END_DATE)
    data_ltf = fetch_binance_data(TICKER, ltf, START_DATE, END_DATE)

    # Identify swing points and liquidity sweeps
    swing_points = identify_swing_points(data_htf, FRACTAL)
    liq_sweeps = identify_liquidity_sweeps(data_htf, swing_points).drop_duplicates(subset=['Sweep Price'], keep='first')

    # Mapping for sweep types to corresponding BOS and swing point functions
    sweep_config = {
        'Liquidity Sweep High': {
            'bos_func': get_first_bearish_bos,
            'swing_func': get_last_high_swing_point,
            'entry_type': 'Short'
        },
        'Liquidity Sweep Low': {
            'bos_func': get_first_bullish_bos,
            'swing_func': get_last_low_swing_point,
            'entry_type': 'Long'
        }
    }

    entries = []

    # Process each liquidity sweep
    for _, sweep in liq_sweeps.iterrows():
        sweep_type = sweep['Sweep Type']
        config = sweep_config.get(sweep_type)

        if not config:
            continue

        # Get BOS data
        bos_data = config['bos_func'](data_ltf[data_ltf['Open Time'] > sweep['Sweep DateTime']].reset_index(drop=True))
        if bos_data is None:
            continue

        # Get the last swing point before BOS date
        swing_point = config['swing_func'](
            data_htf[data_htf['Open Time'] <= bos_data['Bos Date']].reset_index(drop=True), 
            bos_data['Bos Price']
        )
        if swing_point is None:
            continue

        # Calculate take profit and determine trade result
        take_profit = get_take_profit(bos_data['Candle Close Price'], swing_point['Price'], coefficient)
        result = get_trade_result(
            data_ltf[data_ltf['Open Time'] > bos_data['Bos Date']].reset_index(drop=True),
            config['entry_type'], 
            take_profit, 
            swing_point['Price']
        )
        if result is None:
            continue

        # Append entry data
        entries.append({
            'Entry Type': config['entry_type'],
            'Sweep Date': sweep['Sweep DateTime'],
            'Sweep Price': sweep['Sweep Price'],
            'Bos Price': bos_data['Bos Price'],
            'Entry Date': bos_data['Bos Date'],
            'Entry Price': bos_data['Candle Close Price'],
            'Take Profit': take_profit,
            'Stop Loss': swing_point['Price'],
            'Result': result['Result'],
            'Result Date': result['Result Date']
        })

    return pd.DataFrame(entries)
