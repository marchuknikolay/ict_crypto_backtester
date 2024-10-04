import pandas as pd

def identify_liquidity_sweeps(df, swing_points):
    sweeps = []
    for i, swing in swing_points.iterrows():
        # Filter once to get all subsequent candles
        subsequent_candles = df[df['Open Time'] > swing['Date']].reset_index(drop=True)
        
        if swing['Type'] == 'Swing High':
            # Calculate the cumulative maximum of High prices seen so far and compare with swing price
            cum_high_below_swing = subsequent_candles['High'].cummax() <= swing['Price']
            first_breach_idx = cum_high_below_swing.idxmin() if not cum_high_below_swing.all() else None
            
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
            # Calculate the cumulative minimum of Low prices seen so far and compare with swing price
            cum_low_above_swing = subsequent_candles['Low'].cummin() >= swing['Price']
            first_breach_idx = cum_low_above_swing.idxmin() if not cum_low_above_swing.all() else None
            
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
