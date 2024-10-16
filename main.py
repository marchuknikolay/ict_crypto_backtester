from fetch_data import *
from swing_points import *
from sweeps import *
from boses import *
from constants import *
from trade import *

def get_entries(htf, ltf, coefficient):
    # fetch data for high timeframe
    data1h = fetch_binance_data(TICKER, htf, START_DATE, END_DATE)

    # identify swing points
    swing_points = identify_swing_points(data1h, FRACTAL)
    #print(swing_points)

    # identify liquidity sweeps
    liq_sweeps = identify_liquidity_sweeps(data1h, swing_points)
    liq_sweeps.drop_duplicates(subset=['Sweep Price'], keep='first', inplace=True)
    #print(liq_sweeps.to_string(index=False))

    # fetch data for low timeframe
    data15m = fetch_binance_data(TICKER, ltf, START_DATE, END_DATE)

    entries = []

    for i, sweep in liq_sweeps.iterrows():
        if sweep['Sweep Type'] == 'Liquidity Sweep High':
            bearish_bos = get_first_bearish_bos(data15m[data15m['Open Time'] > sweep['Sweep DateTime']].reset_index(drop=True))
            #print(bearish_bos)
            if bearish_bos is None:
                continue

            if bearish_bos['Bos Price'] > sweep['Sweep Price']:
                continue

            #last_high_swing_point = get_last_high_swing_point(data15m[data15m['Open Time'] <= bearish_bos['Bos Date']].reset_index(drop=True), bearish_bos['Bos Price'])
            last_high_swing_point = get_last_high_swing_point(data1h[data1h['Open Time'] <= bearish_bos['Bos Date']].reset_index(drop=True), bearish_bos['Bos Price'])
            '''last_high_swing_point = None
            if sweep['Sweep Price'] > bearish_bos['Bos Price']:
                last_high_swing_point = {'Price': sweep['Sweep Price']}

            candles = data1h[(data1h['Open Time'] > sweep['Sweep DateTime']) & (data1h['Open Time'] < bearish_bos['Bos Date']) & (data1h['High'] > sweep['Sweep Price'])]
            if not candles.empty:
                continue'''

            if last_high_swing_point is None:
                continue

            #print(last_high_swing_point)

            take_profit = get_take_profit(bearish_bos['Candle Close Price'], last_high_swing_point['Price'], coefficient)
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
            #print(bullish_bos)
            if bullish_bos is None:
                continue

            if bullish_bos['Bos Price'] < sweep['Sweep Price']:
                continue

            #last_low_swing_point = get_last_low_swing_point(data15m[data15m['Open Time'] <= bullish_bos['Bos Date']].reset_index(drop=True), bullish_bos['Bos Price'])
            last_low_swing_point = get_last_low_swing_point(data1h[data1h['Open Time'] <= bullish_bos['Bos Date']].reset_index(drop=True), bullish_bos['Bos Price'])
            '''last_low_swing_point = None
            if sweep['Sweep Price'] < bullish_bos['Bos Price']:
                last_low_swing_point = {'Price': sweep['Sweep Price']}

            candles = data1h[(data1h['Open Time'] > sweep['Sweep DateTime']) & (data1h['Open Time'] < bullish_bos['Bos Date']) & (data1h['Low'] < sweep['Sweep Price'])]
            if not candles.empty:
                continue'''

            if last_low_swing_point is None:
                continue

            #print(last_low_swing_point)

            take_profit = get_take_profit(bullish_bos['Candle Close Price'], last_low_swing_point['Price'], coefficient)
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

def trade(htf, ltf, coefficient):
    pd.set_option('display.max_rows', None)
    entries = get_entries(htf, ltf, coefficient)
    print(entries.to_string(index=False))
    print('----------------------------------------------------------------------------')

    result = 0
    wins = 0
    for i, entry in entries.iterrows():
        if entry['Result'] == 'Win':
            result += coefficient
            wins += 1
        if entry['Result'] == 'Lose':
            result -= 1

    if not entries.empty: 
        print('Ticker: ', TICKER)
        print('Strategy: ', htf, ltf)
        print('TP: ', coefficient)
        print('Winrate: ', round(wins/entries.shape[0] * 100), '%')
        print('Profit: ', result, '%')
        print('Long winrate: ', get_long_winrate(entries), '%')
        print('Short winrate: ', get_short_winrate(entries), '%')
        print('Number of trades: ', entries.shape[0])
        print('Number of wins: ', wins)
        print('Max lose streak: ', get_largest_losestreak(entries))
        print('Max win streak: ', get_largest_winstreak(entries))
    
    print('\n\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n')

if __name__ == "__main__":

    '''trade('1d', '4h', 1)
    trade('1d', '4h', 1.5)
    trade('1d', '4h', 2)
    trade('1d', '4h', 2.5)
    trade('1d', '4h', 3)

    trade('1d', '1h', 1)
    trade('1d', '1h', 1.5)
    trade('1d', '1h', 2)
    trade('1d', '1h', 2.5)
    trade('1d', '1h', 3)'''

    trade('4h', '1h', 1)
    '''trade('4h', '1h', 1.5)
    trade('4h', '1h', 2)
    trade('4h', '1h', 2.5)
    trade('4h', '1h', 3)

    trade('4h', '30m', 1)
    trade('4h', '30m', 1.5)
    trade('4h', '30m', 2)
    trade('4h', '30m', 2.5)
    trade('4h', '30m', 3)

    trade('4h', '15m', 1)
    trade('4h', '15m', 1.5)
    trade('4h', '15m', 2)
    trade('4h', '15m', 2.5)
    trade('4h', '15m', 3)

    trade('1h', '15m', 1)
    trade('1h', '15m', 1.5)
    trade('1h', '15m', 2)
    trade('1h', '15m', 2.5)
    trade('1h', '15m', 3)

    trade('1h', '5m', 1)
    trade('1h', '5m', 1.5)
    trade('1h', '5m', 2)
    trade('1h', '5m', 2.5)
    trade('1h', '5m', 3)

    trade('1h', '1m', 1)
    trade('1h', '1m', 1.5)
    trade('1h', '1m', 2)
    trade('1h', '1m', 2.5)
    trade('1h', '1m', 3)'''