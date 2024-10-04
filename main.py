from fetch_data import *
from swing_points import *
from sweeps import *
from boses import *
from constants import *

symbol = 'BTCUSDT'
htf = '1h'
ltf = '1m'
start_date = '2024-09-29'
end_date = '2024-10-01'
coefficient = 3

def get_largest_winstreak(df):
    max_streak = 0
    current_streak = 0
    
    for i, entry in df.iterrows():
        if entry['Result'] == 'Win':
            current_streak += 1
        else:
            if current_streak > max_streak:
                max_streak = current_streak
            current_streak = 0
    
    # Check the final streak
    if current_streak > max_streak:
        max_streak = current_streak
    
    return max_streak

def get_largest_losestreak(df):
    max_streak = 0
    current_streak = 0
    
    for i, entry in df.iterrows():
        if entry['Result'] == 'Lose':
            current_streak += 1
        else:
            if current_streak > max_streak:
                max_streak = current_streak
            current_streak = 0
    
    # Check the final streak
    if current_streak > max_streak:
        max_streak = current_streak
    
    return max_streak

def get_long_winrate(df):
    count = 0
    win_count = 0

    for i, entry in df.iterrows():
        if entry['Entry Type'] == 'Long':
            count += 1

            if entry['Result'] == 'Win':
                win_count += 1

    if win_count == 0:
        return 0

    return round(win_count / count * 100)

def get_short_winrate(df):
    count = 0
    win_count = 0

    for i, entry in df.iterrows():
        if entry['Entry Type'] == 'Short':
            count += 1

            if entry['Result'] == 'Win':
                win_count += 1

    if win_count == 0:
        return 0

    return round(win_count / count * 100)

def get_take_profit(entry_price, stop_loss):
    diff = abs(entry_price - stop_loss)

    if (entry_price < stop_loss):
        return entry_price - coefficient * diff
    else:
        return entry_price + coefficient * diff

def get_trade_result(df, entry_type, take_profit, stop_loss):
    if entry_type == 'Short':
        take_profit_reached = df[df['Low'] <= take_profit].reset_index(drop=True)
        stop_loss_reached = df[df['High'] >= stop_loss].reset_index(drop=True)

        # Check if take_profit_reached has data
        if not take_profit_reached.empty:
            take_profit_reached = take_profit_reached.iloc[0]
        else:
            take_profit_reached = None
        
        # Check if stop_loss_reached has data
        if not stop_loss_reached.empty:
            stop_loss_reached = stop_loss_reached.iloc[0]
        else:
            stop_loss_reached = None

        # Logic to determine the result
        if take_profit_reached is not None and stop_loss_reached is not None:
            if take_profit_reached['Open Time'] < stop_loss_reached['Open Time']:
                return {'Result': 'Win', 'Result Date': take_profit_reached['Open Time']}
            else:
                return {'Result': 'Lose', 'Result Date': stop_loss_reached['Open Time']}
        elif take_profit_reached is not None:
            return {'Result': 'Win', 'Result Date': take_profit_reached['Open Time']}
        elif stop_loss_reached is not None:
            return {'Result': 'Lose', 'Result Date': stop_loss_reached['Open Time']}
        else:
            return None

    if entry_type == 'Long':
        take_profit_reached = df[df['High'] >= take_profit].reset_index(drop=True)
        stop_loss_reached = df[df['Low'] <= stop_loss].reset_index(drop=True)

        # Check if take_profit_reached has data
        if not take_profit_reached.empty:
            take_profit_reached = take_profit_reached.iloc[0]
        else:
            take_profit_reached = None
        
        # Check if stop_loss_reached has data
        if not stop_loss_reached.empty:
            stop_loss_reached = stop_loss_reached.iloc[0]
        else:
            stop_loss_reached = None

        # Logic to determine the result
        if take_profit_reached is not None and stop_loss_reached is not None:
            if take_profit_reached['Open Time'] < stop_loss_reached['Open Time']:
                return {'Result': 'Win', 'Result Date': take_profit_reached['Open Time']}
            else:
                return {'Result': 'Lose', 'Result Date': stop_loss_reached['Open Time']}
        elif take_profit_reached is not None:
            return {'Result': 'Win', 'Result Date': take_profit_reached['Open Time']}
        elif stop_loss_reached is not None:
            return {'Result': 'Lose', 'Result Date': stop_loss_reached['Open Time']}
        else:
            return None

def get_entries():
    # fetch data for high timeframe
    data1h = fetch_binance_data(symbol, htf, start_date, end_date)

    # identify swing points
    swing_points = identify_swing_points(data1h, FRACTAL)
    print(swing_points)

    # identify liquidity sweeps
    liq_sweeps = identify_liquidity_sweeps(data1h, swing_points)
    liq_sweeps.drop_duplicates(subset=['Sweep Price'], keep='first', inplace=True)
    print(liq_sweeps)

    # fetch data for low timeframe
    data15m = fetch_binance_data(symbol, ltf, start_date, end_date)

    entries = []

    for i, sweep in liq_sweeps.iterrows():
        if sweep['Sweep Type'] == 'Liquidity Sweep High':
            bearish_bos = get_first_bearish_bos(data15m[data15m['Open Time'] > sweep['Sweep DateTime']].reset_index(drop=True))
            if bearish_bos is None:
                continue

            #last_high_swing_point = get_last_high_swing_point(data15m[data15m['Open Time'] <= bearish_bos['Bos Date']].reset_index(drop=True))
            last_high_swing_point = get_last_high_swing_point(data1h[data1h['Open Time'] <= bearish_bos['Bos Date']].reset_index(drop=True), bearish_bos['Bos Price'])
            print(last_high_swing_point)
            if last_high_swing_point is None:
                continue

            take_profit = get_take_profit(bearish_bos['Candle Close Price'], last_high_swing_point['Price'])
            result = get_trade_result(data15m[data15m['Open Time'] > bearish_bos['Bos Date']].reset_index(drop=True), 'Short', take_profit, last_high_swing_point['Price'])
            if result is None:
                continue

            entries.append({
                    'Entry Type': 'Short',
                    'Sweep Date': sweep['Sweep DateTime'],
                    'Sweep Price': sweep['Sweep Price'],
                    'Bos Price': bearish_bos['Bos Price'],
                    'Entry Date': bearish_bos['Bos Date'],
                    'Entry Price': bearish_bos['Candle Close Price'],
                    'Take Profit': take_profit,
                    'Stop Loss': last_high_swing_point['Price'],
                    'Result': result['Result'],
                    'Result Date': result['Result Date']
                })

        if sweep['Sweep Type'] == 'Liquidity Sweep Low':
            bullish_bos = get_first_bullish_bos(data15m[data15m['Open Time'] > sweep['Sweep DateTime']].reset_index(drop=True))
            if bullish_bos is None:
                continue

            #last_low_swing_point = get_last_low_swing_point(data15m[data15m['Open Time'] <= bullish_bos['Bos Date']].reset_index(drop=True))
            last_low_swing_point = get_last_low_swing_point(data1h[data1h['Open Time'] <= bullish_bos['Bos Date']].reset_index(drop=True), bullish_bos['Bos Price'])
            print(last_low_swing_point)
            if last_low_swing_point is None:
                continue

            take_profit = get_take_profit(bullish_bos['Candle Close Price'], last_low_swing_point['Price'])
            result = get_trade_result(data15m[data15m['Open Time'] > bullish_bos['Bos Date']].reset_index(drop=True), 'Long', take_profit, last_low_swing_point['Price'])
            if result is None:
                continue

            entries.append({
                    'Entry Type': 'Long',
                    'Sweep Date': sweep['Sweep DateTime'],
                    'Sweep Price': sweep['Sweep Price'],
                    'Bos Price': bullish_bos['Bos Price'],
                    'Entry Date': bullish_bos['Bos Date'],
                    'Entry Price': bullish_bos['Candle Close Price'],
                    'Take Profit': take_profit,
                    'Stop Loss': last_low_swing_point['Price'],
                    'Result': result['Result'],
                    'Result Date': result['Result Date']
                })

    return pd.DataFrame(entries)

if __name__ == "__main__":
    pd.set_option('display.max_rows', None)

    entries = get_entries()
    '''print(entries)
    print('----------------------------------------------------------------------------')

    result = 0;
    wins = 0;
    for i, entry in entries.iterrows():
        if entry['Result'] == 'Win':
            result += coefficient
            wins += 1
        if entry['Result'] == 'Lose':
            result -= 1;

    if not entries.empty: 
        print('Ticker: ', symbol)
        print('Strategy: ', htf, ltf)
        print('TP: ', coefficient)
        print('Winrate: ', round(wins/entries.shape[0] * 100), '%')
        print('Profit: ', result, '%')
        print('Long winrate: ', get_long_winrate(entries), '%')
        print('Short winrate: ', get_short_winrate(entries), '%')
        print('Number of trades: ', entries.shape[0])
        print('Number of wins: ', wins)
        print('Max lose streak: ', get_largest_losestreak(entries))
        print('Max win streak: ', get_largest_winstreak(entries))'''
