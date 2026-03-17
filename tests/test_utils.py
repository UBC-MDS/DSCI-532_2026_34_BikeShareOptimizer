import sys
import os
import pandas as pd

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import calculate_avg_trip_time


def test_calculate_avg_trip_time():
    df = pd.DataFrame({
        "tripduration": [60, 120, 180]
    })

    result = calculate_avg_trip_time(df)

    assert result == 2.0


def test_calculate_avg_trip_time_empty():
    df = pd.DataFrame()

    result = calculate_avg_trip_time(df)

    assert result is None