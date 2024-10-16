from trade import *

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