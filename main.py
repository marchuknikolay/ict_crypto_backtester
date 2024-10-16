from trade import *

if __name__ == "__main__":
    # Get trade combinations
    trade_combinations = get_trade_combinations()

    # Execute trades based on the combinations
    execute_trades_for_combinations(trade_combinations)
