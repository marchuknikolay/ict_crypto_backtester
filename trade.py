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