import pandas as pd


def calculate_avg_trip_time(df: pd.DataFrame):
    """
    Calculate average trip duration in minutes.
    """

    if df is None or df.empty:
        return None

    avg_seconds = df["tripduration"].mean()
    return avg_seconds / 60